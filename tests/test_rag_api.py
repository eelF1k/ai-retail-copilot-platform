from fastapi.testclient import TestClient

from app.main import app


def test_rag_answer_returns_citations(monkeypatch):
    async def fake_generate(self, prompt: str, temperature: float = 0.2):
        _ = (self, prompt, temperature)
        return {
            "provider": "mock",
            "model": "mock-retail-v1",
            "output": "Use stockout prevention playbook and enforce daily review.",
            "used_fallback": False,
        }

    monkeypatch.setattr("app.services.llm.LLMService.generate", fake_generate)

    with TestClient(app) as client:
        response = client.post(
            "/api/v1/ops/rag/answer",
            json={"question": "How to reduce stockouts?", "top_k": 2},
        )

    assert response.status_code == 200
    payload = response.json()
    assert payload["context_count"] == 2
    assert len(payload["citations"]) == 2
    assert "answer" in payload
    assert "confidence" in payload
    assert "risk_level" in payload

