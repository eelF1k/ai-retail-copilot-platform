from typing import Any

import httpx

from app.core.settings import settings


class LLMService:
    async def generate(
        self,
        prompt: str,
        temperature: float = 0.2,
        provider: str | None = None,
        model: str | None = None,
    ) -> dict[str, Any]:
        selected_provider = provider or settings.llm_provider
        selected_model = model or settings.llm_model

        if selected_provider == "mock":
            return {
                "provider": "mock",
                "model": "mock-retail-v1",
                "output": self._mock_output(prompt),
                "used_fallback": False,
            }

        if selected_provider == "claude":
            try:
                output = await self._call_claude(prompt=prompt, temperature=temperature, model=selected_model)
                return {
                    "provider": "claude",
                    "model": selected_model,
                    "output": output,
                    "used_fallback": False,
                }
            except Exception:
                return self._fallback(prompt, selected_provider)

        try:
            output = await self._call_openai_compatible(
                prompt=prompt,
                temperature=temperature,
                model=selected_model,
            )
            return {
                "provider": selected_provider,
                "model": selected_model,
                "output": output,
                "used_fallback": False,
            }
        except Exception:
            return self._fallback(prompt, selected_provider)

    async def _call_openai_compatible(self, prompt: str, temperature: float, model: str) -> str:
        if not settings.llm_api_base or not settings.llm_api_key:
            raise RuntimeError("LLM api base/key are not configured")

        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": "You are a concise retail analytics assistant."},
                {"role": "user", "content": prompt},
            ],
            "temperature": temperature,
        }
        headers = {"Authorization": f"Bearer {settings.llm_api_key}"}

        async with httpx.AsyncClient(timeout=settings.llm_timeout_s) as client:
            response = await client.post(
                f"{settings.llm_api_base.rstrip('/')}/chat/completions",
                json=payload,
                headers=headers,
            )
            response.raise_for_status()
            data = response.json()
        return data["choices"][0]["message"]["content"]

    async def _call_claude(self, prompt: str, temperature: float, model: str) -> str:
        if not settings.llm_api_base or not settings.llm_api_key:
            raise RuntimeError("Claude api base/key are not configured")

        payload = {
            "model": model,
            "max_tokens": 512,
            "temperature": temperature,
            "messages": [{"role": "user", "content": prompt}],
        }
        headers = {
            "x-api-key": settings.llm_api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }

        async with httpx.AsyncClient(timeout=settings.llm_timeout_s) as client:
            response = await client.post(
                f"{settings.llm_api_base.rstrip('/')}/messages",
                json=payload,
                headers=headers,
            )
            response.raise_for_status()
            data = response.json()

        content = data.get("content", [])
        if content and isinstance(content, list):
            first = content[0]
            return str(first.get("text", ""))
        raise RuntimeError("Unexpected Claude response format")

    def _fallback(self, prompt: str, provider: str) -> dict[str, Any]:
        return {
            "provider": f"{provider}-fallback",
            "model": "mock-retail-v1",
            "output": self._mock_output(prompt),
            "used_fallback": True,
        }

    @staticmethod
    def _mock_output(prompt: str) -> str:
        short = prompt.strip().replace("\n", " ")[:220]
        return (
            f"Mock retail insight based on prompt: {short}. "
            "Key recommendation: review top-3 SKUs and low-margin categories this week."
        )

