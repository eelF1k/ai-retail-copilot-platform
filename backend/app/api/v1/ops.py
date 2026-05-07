from fastapi import APIRouter, Query

from app.repositories import RetailAnalyticsRepository, SafeSQLRepository
from app.schemas.llm import PromptRunRequest, PromptRunResponse
from app.schemas.sql_guard import SQLQueryRequest, SQLQueryResponse
from app.services import LLMService, retail_analyst_prompt
from app.services.sql_guard import SQLGuard

router = APIRouter(prefix="/ops", tags=["ops"])


@router.get("/revenue-by-store")
async def revenue_by_store(days: int = Query(30, ge=1, le=365)):
    data = await RetailAnalyticsRepository().revenue_by_store(days=days)
    return {"days": days, "rows": data}


@router.get("/top-skus")
async def top_skus(
    days: int = Query(30, ge=1, le=365),
    limit: int = Query(10, ge=1, le=100),
):
    data = await RetailAnalyticsRepository().top_skus(days=days, limit=limit)
    return {"days": days, "limit": limit, "rows": data}


@router.post("/safe-sql", response_model=SQLQueryResponse)
async def execute_safe_sql(payload: SQLQueryRequest):
    guard = SQLGuard()
    allowed, reason = guard.validate(payload.sql)
    if not allowed:
        return SQLQueryResponse(allowed=False, reason=reason, rows=[], returned_rows=0)

    rows = await SafeSQLRepository().execute_select(sql=payload.sql, max_rows=payload.max_rows)
    return SQLQueryResponse(
        allowed=True,
        reason="ok",
        rows=rows,
        returned_rows=len(rows),
    )


@router.post("/prompt/run", response_model=PromptRunResponse)
async def run_prompt(payload: PromptRunRequest):
    prompt = retail_analyst_prompt(task=payload.task, context=payload.context)
    result = await LLMService().generate(prompt=prompt, temperature=payload.temperature)
    return PromptRunResponse(
        provider=str(result["provider"]),
        model=str(result["model"]),
        prompt=prompt,
        output=str(result["output"]),
        used_fallback=bool(result["used_fallback"]),
    )

