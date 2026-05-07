# API Examples

## Safe SQL
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/ops/safe-sql" ^
  -H "Content-Type: application/json" ^
  -d "{\"sql\":\"SELECT s.store_code, SUM(s.total_amount) AS revenue FROM sales s GROUP BY s.store_code\",\"max_rows\":50}"
```

## NL-to-SQL
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/ops/nl-sql" ^
  -H "Content-Type: application/json" ^
  -d "{\"question\":\"Show revenue by store for the last month\",\"max_rows\":20}"
```

## RAG answer with citations
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/ops/rag/answer" ^
  -H "Content-Type: application/json" ^
  -d "{\"question\":\"How can we reduce stockouts in dairy category?\",\"top_k\":3}"
```

