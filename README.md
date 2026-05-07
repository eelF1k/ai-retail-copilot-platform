# AI Retail Copilot Platform

## Назва проєкту
AI Retail Copilot Platform

## Це мій пет проєкт про...
Це мій пет проєкт про AI-помічника для ритейлу: аналітика через LLM, NL-to-SQL, RAG та контроль галюцинацій.

## Технологічний стек
- Python, FastAPI, asyncio
- PostgreSQL + SQLAlchemy
- Redis
- OpenAI/Claude-compatible інтеграції
- Docker Compose, Kubernetes
- GitHub Actions, GitLab CI

## Що реалізовано
- Аналітичні ендпоінти по продажам.
- Безпечне виконання SQL з guardrails.
- LLM промптинг і multi-provider порівняння.
- NL-to-SQL та RAG з цитуванням джерел.
- Hallucination guard і quality gate у CI.

## Структура
- `backend/app/api` — API ендпоінти
- `backend/app/services` — LLM/SQL/RAG сервіси
- `backend/app/db` — робота з PostgreSQL/Redis
- `scripts/` — seed, load-smoke, eval утиліти
- `infra/` — docker/k8s маніфести

## Архітектура
- API отримує бізнес-запит і маршрутизує в NL-to-SQL або RAG.
- SQL guard перевіряє запити перед виконанням.
- LLM сервіс генерує бізнес-відповіді, guard оцінює ризики.
- Метрики і логи відстежують стабільність та якість.

## Що потрібно встановити для тесту
- Python 3.12+
- Docker Desktop
- (опційно) kubectl + локальний k8s

## Як запустити
```bash
docker compose up --build
```
Або локально:
```bash
pip install -r requirements.txt
python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
```

