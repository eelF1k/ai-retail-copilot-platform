# Architecture Overview

## Purpose
`AI Retail Copilot Platform` is an internal AI backend for retail operations and analytics.

## Core flows
1. **NL-to-SQL**
   - Input question -> deterministic SQL translation
   - SQL guardrails validation
   - Read-only SQL execution
   - LLM summarization + hallucination confidence scoring

2. **RAG answer**
   - Input question -> local knowledge retrieval (`top_k`)
   - LLM answer generation from retrieved context
   - Citation output + hallucination confidence scoring

## Components
- **API layer**: `backend/app/api/v1/ops.py`, `system.py`
- **Core config**: `backend/app/core/settings.py`
- **DB layer**: `backend/app/db/sql.py`
- **Repositories**:
  - `analytics.py` (analytical SQL)
  - `safe_sql.py` (safe query execution)
- **Services**:
  - `nl_sql.py` (question -> SQL)
  - `sql_guard.py` (deny unsafe SQL)
  - `llm.py` (OpenAI/Claude/mock adapters)
  - `hallucination.py` (grounding/confidence/risk)
- **RAG**:
  - `rag/knowledge_base.py`
  - `rag/retriever.py`
- **Observability**:
  - `observability/logging.py`
  - `observability/metrics.py`

## Runtime topology
- **Docker Compose**:
  - `api`
  - `postgres`
  - `redis`
- **Kubernetes**:
  - deployments/services in `infra/k8s`

## Reliability and safety
- Read-only SQL path for AI queries
- Table allowlist + forbidden keyword checks
- Hallucination risk signal (`confidence`, `grounding_score`, `risk_level`)
- Request logs + Prometheus metrics

