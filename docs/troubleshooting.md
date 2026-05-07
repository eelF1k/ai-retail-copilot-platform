# Troubleshooting

## `500` on SQL-based endpoints
Possible causes:
- Postgres is not running
- Tables are not created yet
- `POSTGRES_DSN` points to wrong host/port

Actions:
1. Check container status: `docker compose ps`
2. Restart stack: `docker compose down && docker compose up --build`
3. Verify health: `GET /api/v1/health`

## `safe-sql` returns blocked query
Reason:
- SQL guardrails allow only `SELECT`
- unknown tables are blocked
- multiple statements (`;`) are blocked

Action:
- rewrite query to read-only `SELECT` and use allowed tables (`sales`, `sale_items`).

## LLM output quality is weak
Possible causes:
- insufficient context
- overly broad task
- provider fallback to mock mode

Actions:
1. enrich prompt context (`/prompt/run`)
2. use narrower business question
3. check provider config: `LLM_PROVIDER`, `LLM_API_BASE`, `LLM_API_KEY`

