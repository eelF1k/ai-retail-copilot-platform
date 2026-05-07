from fastapi.testclient import TestClient

from app.main import app


def test_health_endpoint():
    with TestClient(app) as client:
        response = client.get("/api/v1/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"


def test_metrics_endpoint():
    with TestClient(app) as client:
        response = client.get("/api/v1/metrics")
    assert response.status_code == 200
    assert "retail_ops_request_latency_seconds" in response.text

