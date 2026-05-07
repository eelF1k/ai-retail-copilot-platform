# AI Retail Copilot Platform

Backend-first pet project tailored for the AI Developer role in retail.

## Goal
Build an internal AI platform that helps retail teams:
- answer operational and analytics questions with LLMs,
- query PostgreSQL safely with grounded SQL flows,
- reduce hallucinations with retrieval and validation layers,
- run reliably in Docker and Kubernetes.

## Planned modules
- `backend/app/api` - REST endpoints
- `backend/app/core` - config and shared settings
- `backend/app/services` - LLM, SQL, RAG, guardrails
- `backend/app/db` - PostgreSQL integration
- `backend/app/observability` - logs, metrics, tracing hooks
- `docs/` - architecture and runbook
- `infra/` - docker and k8s manifests

## Stack (target)
- Python, FastAPI, asyncio
- PostgreSQL + SQLAlchemy
- OpenAI/Claude-compatible adapters
- Redis (cache/queue)
- Docker Compose + Kubernetes
- Prometheus metrics + structured logs

## Roadmap (commit by commit)
0. Init repository and architecture skeleton
1. FastAPI scaffold + config + health endpoints
2. PostgreSQL schema + seed + analytical SQL queries
3. Safe SQL execution layer + guardrails
4. LLM adapters + prompt templates
5. NL-to-SQL endpoint + summarization
6. RAG layer + citations
7. Hallucination checks + confidence scoring
8. Docker + docker-compose stack
9. Kubernetes manifests
10. Observability (metrics/logging)
11. Tests (unit + integration + smoke)
12. CI/CD (GitHub Actions + gitlab-ci)
13. Docs polish and runbook

## Step 2 deliverables
- PostgreSQL async layer (`SQLAlchemy + asyncpg`)
- Sales/order-item schema for retail analytics
- Seed script: `python scripts/seed_postgres.py`
- Analytical endpoints:
  - `GET /api/v1/ops/revenue-by-store`
  - `GET /api/v1/ops/top-skus`

## Step 3 deliverables
- Safe SQL endpoint: `POST /api/v1/ops/safe-sql`
- Guardrails:
  - only `SELECT`
  - deny DDL/DML keywords
  - allowlist of source tables
  - enforced result row limit

## Step 4 deliverables
- LLM adapters:
  - OpenAI-compatible chat completions
  - Claude messages API
  - mock provider fallback
- Prompt templates for retail analyst tasks
- Endpoint: `POST /api/v1/ops/prompt/run`

## Step 5 deliverables
- NL-to-SQL flow:
  - question -> deterministic SQL translation
  - SQL guardrails validation
  - safe read-only execution
  - LLM-based business summary
- Endpoint: `POST /api/v1/ops/nl-sql`

