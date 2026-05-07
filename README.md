# AI Retail Copilot Platform

Backend-first pet-проєкт під роль AI Developer у ритейлі.

## Мета
Побудувати внутрішню AI-платформу, яка допомагає retail-командам:
- відповідати на операційні та аналітичні питання через LLM,
- безпечно працювати з PostgreSQL через перевірені SQL-потоки,
- зменшувати галюцинації через retrieval і валідаційні шари,
- стабільно працювати в Docker та Kubernetes.

## Заплановані модулі
- `backend/app/api` - REST ендпоінти
- `backend/app/core` - конфігурація та спільні налаштування
- `backend/app/services` - LLM, SQL, RAG, guardrails
- `backend/app/db` - інтеграція з PostgreSQL
- `backend/app/observability` - логи, метрики, hooks для трасування
- `docs/` - архітектура та runbook
- `infra/` - docker і k8s маніфести

## Стек (цільовий)
- Python, FastAPI, asyncio
- PostgreSQL + SQLAlchemy
- OpenAI/Claude-compatible адаптери
- Redis (cache/queue)
- Docker Compose + Kubernetes
- Prometheus метрики + structured logs

## Roadmap (коміт за комітом)
0. Ініціалізація репозиторію та каркасу архітектури
1. FastAPI scaffold + config + health ендпоінти
2. PostgreSQL схема + seed + аналітичні SQL-запити
3. Шар безпечного виконання SQL + guardrails
4. LLM адаптери + prompt templates
5. NL-to-SQL ендпоінт + summarization
6. RAG шар + цитати
7. Перевірки галюцинацій + confidence scoring
8. Docker + docker-compose стек
9. Kubernetes маніфести
10. Observability (метрики/логування)
11. Тести (unit + integration + smoke)
12. CI/CD (GitHub Actions + gitlab-ci)
13. Полірування документації та runbook

## Крок 2 (готово)
- Async-шар PostgreSQL (`SQLAlchemy + asyncpg`)
- Схема продажів/позицій замовлень для retail-аналітики
- Seed-скрипт: `python scripts/seed_postgres.py`
- Аналітичні ендпоінти:
  - `GET /api/v1/ops/revenue-by-store`
  - `GET /api/v1/ops/top-skus`

## Крок 3 (готово)
- Ендпоінт безпечного SQL: `POST /api/v1/ops/safe-sql`
- Guardrails:
  - лише `SELECT`
  - заборона DDL/DML ключових слів
  - allowlist таблиць-джерел
  - примусове обмеження кількості рядків

## Крок 4 (готово)
- LLM адаптери:
  - OpenAI-compatible chat completions
  - Claude messages API
  - mock provider fallback
- Prompt templates для retail analyst задач
- Ендпоінт: `POST /api/v1/ops/prompt/run`

## Крок 5 (готово)
- NL-to-SQL потік:
  - питання -> deterministic SQL translation
  - валідація SQL guardrails
  - безпечне read-only виконання
  - LLM-підсумок для бізнесу
- Ендпоінт: `POST /api/v1/ops/nl-sql`

## Крок 6 (готово)
- Локальний RAG retrieval над внутрішніми retail knowledge snippets
- Ендпоінт відповіді з цитатами: `POST /api/v1/ops/rag/answer`
- Метадані джерел у відповіді (`source_id`, title, snippet)

## Крок 7 (готово)
- Перевірки галюцинацій для NL-SQL і RAG результатів
- Confidence і grounding scores у відповідях API
- Прапорці ризику (`low`, `medium`, `high`) з warning-повідомленнями

## Крок 8 (готово)
- `backend/Dockerfile` для API контейнера
- `docker-compose.yml` стек:
  - `api`
  - `postgres`
  - `redis`
- `.env.example` для локального налаштування середовища

## Запуск через Docker
```bash
docker compose up --build
```

## Швидкі перевірки
- `GET /api/v1/health`
- `GET /api/v1/ready`
- `GET /api/v1/ops/revenue-by-store`
- `POST /api/v1/ops/nl-sql`

## Крок 9 (готово)
- Kubernetes маніфести в `infra/k8s/`:
  - `config.yaml` (ConfigMap + Secret)
  - `workloads.yaml` (Deployments: api, postgres, redis)
  - `services.yaml` (ClusterIP services)
  - `kustomization.yaml`

## Запуск у Kubernetes (локальний кластер)
```bash
kubectl apply -k infra/k8s
kubectl get pods
kubectl get svc
kubectl port-forward svc/api 8000:8000
```

## Крок 10 (готово)
- Structured request logging middleware
- Ендпоінт метрик Prometheus: `GET /api/v1/metrics`
- Метрики latency та errors для ключових ops-ендпоінтів

## Крок 11 (готово)
- Розширені API integration тести:
  - `tests/test_system_api.py`
  - `tests/test_safe_sql_api.py`
- Smoke load утиліта:
  - `python scripts/load_smoke.py --base-url http://127.0.0.1:8000 --requests 30 --concurrency 10`

## Крок 12 (готово)
- GitHub Actions pipeline: `.github/workflows/ci.yml`
- GitLab CI pipeline: `gitlab-ci.yml`
- Автоматичні перевірки:
  - тести
  - compile validation
  - docker image build

## Крок 13 (готово)
- Полірування документації:
  - `docs/architecture.md`
  - `docs/runbook.md`
  - `docs/api-examples.md`
  - `docs/troubleshooting.md`

## Крок 14 (advanced AI operations)
- Multi-provider comparison ендпоінт:
  - `POST /api/v1/ops/prompt/compare`
  - порівнює відповіді `mock/openai/claude` для однієї бізнес-задачі
- Скрипт prompt evaluation для реальних retail-сценаріїв:
  - `python scripts/prompt_eval.py --provider mock`
- Скрипт SQL performance tuning report (на базі PostgreSQL `EXPLAIN`):
  - `python scripts/sql_tune_report.py`

## Крок 15 (AI quality gate в CI)
- Автоматизований скрипт LLM quality gate:
  - `python scripts/llm_quality_gate.py --provider mock --min-avg-confidence 0.25 --max-high-risk 0`
- Інтеграція в CI:
  - GitHub Actions запускає gate у `.github/workflows/ci.yml`
  - GitLab CI запускає gate у `gitlab-ci.yml`
- Політика gate:
  - pipeline падає, якщо середній confidence нижче порогу
  - pipeline падає, якщо кількість high-risk сценаріїв перевищує ліміт

## Індекс документації
- Architecture: `docs/architecture.md`
- Runbook: `docs/runbook.md`
- API examples: `docs/api-examples.md`
- Troubleshooting: `docs/troubleshooting.md`

