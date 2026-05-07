import argparse
import asyncio
import json

from app.services.hallucination import HallucinationGuard
from app.services.llm import LLMService
from app.services.prompt_templates import retail_analyst_prompt

SCENARIOS = [
    {
        "task": "How to reduce stockouts in dairy category next week?",
        "context": "Critical categories include dairy. Replenishment trigger is below 2-day forecast.",
    },
    {
        "task": "What should we monitor for promo pricing safety?",
        "context": "Promotions must keep margin above category threshold and require pricing lead approval.",
    },
    {
        "task": "How to prioritize loyalty campaigns this month?",
        "context": "Use recency-frequency-monetary segmentation and focus high-value churn-risk segment.",
    },
]


async def run_eval(provider: str, temperature: float) -> None:
    guard = HallucinationGuard()
    service = LLMService()
    rows = []

    for idx, scenario in enumerate(SCENARIOS, start=1):
        prompt = retail_analyst_prompt(task=scenario["task"], context=scenario["context"])
        result = await service.generate(prompt=prompt, temperature=temperature, provider=provider)
        quality = guard.evaluate(answer=str(result["output"]), contexts=[scenario["context"]])
        rows.append(
            {
                "scenario": idx,
                "provider": result["provider"],
                "used_fallback": result["used_fallback"],
                "confidence": quality["confidence"],
                "risk_level": quality["risk_level"],
                "output_preview": str(result["output"])[:180],
            }
        )

    print(json.dumps(rows, ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Prompt quality smoke-eval for retail AI scenarios.")
    parser.add_argument("--provider", default="mock", help="mock|openai|claude")
    parser.add_argument("--temperature", type=float, default=0.2)
    args = parser.parse_args()
    asyncio.run(run_eval(provider=args.provider, temperature=args.temperature))


if __name__ == "__main__":
    main()

