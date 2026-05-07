# Runbook

## Local Python run
1. Install dependencies:
```bash
python -m pip install -r requirements.txt
```
2. Start API:
```bash
python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
```

## Docker run
```bash
docker compose up --build
```

## Health checks
- `GET /api/v1/health`
- `GET /api/v1/ready`
- `GET /api/v1/metrics`

## Seed demo data
Make sure Postgres is available and `POSTGRES_DSN` is configured:
```bash
python scripts/seed_postgres.py
```

## Smoke load
```bash
python scripts/load_smoke.py --base-url http://127.0.0.1:8000 --requests 30 --concurrency 10
```

