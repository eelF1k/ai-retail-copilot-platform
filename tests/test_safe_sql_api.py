from fastapi.testclient import TestClient

from app.main import app


def test_safe_sql_blocks_forbidden_statement():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/ops/safe-sql",
            json={"sql": "DELETE FROM sales", "max_rows": 10},
        )

    assert response.status_code == 200
    payload = response.json()
    assert payload["allowed"] is False
    assert "Only SELECT" in payload["reason"]
    assert payload["returned_rows"] == 0


def test_safe_sql_executes_allowed_select(monkeypatch):
    async def fake_execute_select(self, sql: str, max_rows: int = 200):
        _ = (self, sql, max_rows)
        return [{"sku": "SKU-1001", "units": 50}]

    monkeypatch.setattr("app.repositories.safe_sql.SafeSQLRepository.execute_select", fake_execute_select)

    with TestClient(app) as client:
        response = client.post(
            "/api/v1/ops/safe-sql",
            json={"sql": "SELECT sku, 50 AS units FROM sale_items", "max_rows": 10},
        )

    assert response.status_code == 200
    payload = response.json()
    assert payload["allowed"] is True
    assert payload["returned_rows"] == 1

