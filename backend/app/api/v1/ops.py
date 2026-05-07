import json
from time import perf_counter

from fastapi import APIRouter, Query

from app.observability.metrics import increment_error, observe_latency
from app.repositories import RetailAnalyticsRepository, SafeSQLRepository
from app.schemas.llm import PromptRunRequest, PromptRunResponse
from app.schemas.llm_compare import LLMCompareItem, LLMCompareRequest, LLMCompareResponse
from app.schemas.nl_sql import NL2SQLRequest, NL2SQLResponse
from app.schemas.rag import Citation, RAGRequest, RAGResponse
from app.schemas.sql_guard import SQLQueryRequest, SQLQueryResponse
from app.services import HallucinationGuard, LLMService, NL2SQLService, retail_analyst_prompt
from app.services.sql_guard import SQLGuard
from app.rag import KnowledgeRetriever

router = APIRouter(prefix="/ops", tags=["ops"])


@router.get("/revenue-by-store")
async def revenue_by_store(days: int = Query(30, ge=1, le=365)):
    started_at = perf_counter()
    try:
        data = await RetailAnalyticsRepository().revenue_by_store(days=days)
    except Exception:
        increment_error("revenue_by_store")
        raise
    finally:
        observe_latency("revenue_by_store", started_at)
    return {"days": days, "rows": data}


@router.get("/top-skus")
async def top_skus(
    days: int = Query(30, ge=1, le=365),
    limit: int = Query(10, ge=1, le=100),
):
    started_at = perf_counter()
    try:
        data = await RetailAnalyticsRepository().top_skus(days=days, limit=limit)
    except Exception:
        increment_error("top_skus")
        raise
    finally:
        observe_latency("top_skus", started_at)
    return {"days": days, "limit": limit, "rows": data}


@router.post("/safe-sql", response_model=SQLQueryResponse)
async def execute_safe_sql(payload: SQLQueryRequest):
    started_at = perf_counter()
    guard = SQLGuard()
    allowed, reason = guard.validate(payload.sql)
    if not allowed:
        observe_latency("safe_sql", started_at)
        return SQLQueryResponse(allowed=False, reason=reason, rows=[], returned_rows=0)

    try:
        rows = await SafeSQLRepository().execute_select(sql=payload.sql, max_rows=payload.max_rows)
    except Exception:
        increment_error("safe_sql")
        raise
    finally:
        observe_latency("safe_sql", started_at)
    return SQLQueryResponse(
        allowed=True,
        reason="ok",
        rows=rows,
        returned_rows=len(rows),
    )


@router.post("/prompt/run", response_model=PromptRunResponse)
async def run_prompt(payload: PromptRunRequest):
    started_at = perf_counter()
    prompt = retail_analyst_prompt(task=payload.task, context=payload.context)
    try:
        result = await LLMService().generate(prompt=prompt, temperature=payload.temperature)
    except Exception:
        increment_error("prompt_run")
        raise
    finally:
        observe_latency("prompt_run", started_at)
    return PromptRunResponse(
        provider=str(result["provider"]),
        model=str(result["model"]),
        prompt=prompt,
        output=str(result["output"]),
        used_fallback=bool(result["used_fallback"]),
    )


@router.post("/prompt/compare", response_model=LLMCompareResponse)
async def compare_prompt(payload: LLMCompareRequest):
    prompt = retail_analyst_prompt(task=payload.task, context=payload.context)
    results: list[LLMCompareItem] = []

    for provider in payload.providers:
        result = await LLMService().generate(
            prompt=prompt,
            temperature=payload.temperature,
            provider=provider,
        )
        results.append(
            LLMCompareItem(
                provider=str(result["provider"]),
                model=str(result["model"]),
                output=str(result["output"]),
                used_fallback=bool(result["used_fallback"]),
            )
        )

    return LLMCompareResponse(prompt=prompt, results=results)


@router.post("/nl-sql", response_model=NL2SQLResponse)
async def run_nl_to_sql(payload: NL2SQLRequest):
    started_at = perf_counter()
    sql = NL2SQLService().translate(payload.question)
    allowed, reason = SQLGuard().validate(sql)
    if not allowed:
        observe_latency("nl_sql", started_at)
        return NL2SQLResponse(
            question=payload.question,
            sql=sql,
            allowed=False,
            rows=[],
            row_count=0,
            summary=f"Query blocked by guardrails: {reason}",
            confidence=0.0,
            grounding_score=0.0,
            risk_level="high",
            warnings=["SQL blocked by guardrails before execution."],
        )

    try:
        rows = await SafeSQLRepository().execute_select(sql=sql, max_rows=payload.max_rows)
        summary_prompt = (
            f"User question: {payload.question}\n"
            f"Executed SQL: {sql}\n"
            f"Rows (json): {json.dumps(rows, ensure_ascii=True)[:6000]}\n"
            "Provide a short business summary in 3-5 bullet points."
        )
        llm_result = await LLMService().generate(prompt=summary_prompt, temperature=0.1)
        guard_result = HallucinationGuard().evaluate(
            answer=str(llm_result["output"]),
            contexts=[json.dumps(row, ensure_ascii=True) for row in rows],
        )
    except Exception:
        increment_error("nl_sql")
        raise
    finally:
        observe_latency("nl_sql", started_at)

    return NL2SQLResponse(
        question=payload.question,
        sql=sql,
        allowed=True,
        rows=rows,
        row_count=len(rows),
        summary=str(llm_result["output"]),
        confidence=float(guard_result["confidence"]),
        grounding_score=float(guard_result["grounding_score"]),
        risk_level=str(guard_result["risk_level"]),
        warnings=list(guard_result["warnings"]),
    )


@router.post("/rag/answer", response_model=RAGResponse)
async def rag_answer(payload: RAGRequest):
    started_at = perf_counter()
    try:
        contexts = KnowledgeRetriever().retrieve(question=payload.question, top_k=payload.top_k)
        context_text = "\n\n".join(
            f"[{idx + 1}] {item['title']}: {item['text']}" for idx, item in enumerate(contexts)
        )
        prompt = (
            f"Question: {payload.question}\n\n"
            f"Knowledge context:\n{context_text}\n\n"
            "Answer concisely, rely only on provided context, and mention key constraints."
        )
        llm_result = await LLMService().generate(prompt=prompt, temperature=0.1)
        guard_result = HallucinationGuard().evaluate(
            answer=str(llm_result["output"]),
            contexts=[str(item["text"]) for item in contexts],
        )
    except Exception:
        increment_error("rag_answer")
        raise
    finally:
        observe_latency("rag_answer", started_at)

    citations = [
        Citation(
            source_id=str(item["source_id"]),
            title=str(item["title"]),
            snippet=str(item["text"])[:220],
        )
        for item in contexts
    ]
    return RAGResponse(
        question=payload.question,
        answer=str(llm_result["output"]),
        citations=citations,
        context_count=len(citations),
        confidence=float(guard_result["confidence"]),
        grounding_score=float(guard_result["grounding_score"]),
        risk_level=str(guard_result["risk_level"]),
        warnings=list(guard_result["warnings"]),
    )

