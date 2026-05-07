import pytest

from app.services.llm import LLMService


@pytest.mark.asyncio
async def test_llm_service_uses_mock_provider(monkeypatch):
    monkeypatch.setattr("app.services.llm.settings.llm_provider", "mock")

    result = await LLMService().generate("Summarize sales trend for store A")

    assert result["provider"] == "mock"
    assert result["used_fallback"] is False
    assert "Mock retail insight" in result["output"]


@pytest.mark.asyncio
async def test_llm_service_fallback_on_openai_failure(monkeypatch):
    async def broken_call(self, prompt: str, temperature: float):
        _ = (self, prompt, temperature)
        raise RuntimeError("provider down")

    monkeypatch.setattr("app.services.llm.settings.llm_provider", "openai")
    monkeypatch.setattr("app.services.llm.LLMService._call_openai_compatible", broken_call)

    result = await LLMService().generate("Need category margin summary")

    assert result["used_fallback"] is True
    assert "fallback" in result["provider"]

