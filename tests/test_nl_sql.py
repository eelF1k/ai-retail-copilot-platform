import pytest

from app.services.nl_sql import NL2SQLService


def test_nl_sql_translator_revenue_query():
    sql = NL2SQLService().translate("Show revenue by store for last month")
    assert "from sales" in sql.lower()
    assert "group by s.store_code" in sql.lower()


@pytest.mark.asyncio
async def test_nl_sql_endpoint_flow(monkeypatch):
    from fastapi.testclient import TestClient

    from app.main import app

    async def fake_execute_select(self, sql: str, max_rows: int = 200):
        _ = (self, sql, max_rows)
        return [{"store_code": "VELMART_KYIV", "revenue": 12345.0, "orders": 99}]

    async def fake_generate(self, prompt: str, temperature: float = 0.2):
        _ = (self, prompt, temperature)
        return {
            "provider": "mock",
            "model": "mock-retail-v1",
            "output": "Revenue is concentrated in VELMART_KYIV.",
            "used_fallback": False,
        }

    monkeypatch.setattr("app.repositories.safe_sql.SafeSQLRepository.execute_select", fake_execute_select)
    monkeypatch.setattr("app.services.llm.LLMService.generate", fake_generate)

    with TestClient(app) as client:
        response = client.post(
            "/api/v1/ops/nl-sql",
            json={"question": "Show revenue by store", "max_rows": 10},
        )

    assert response.status_code == 200
    payload = response.json()
    assert payload["allowed"] is True
    assert payload["row_count"] == 1
    assert "VELMART_KYIV" in payload["summary"]

