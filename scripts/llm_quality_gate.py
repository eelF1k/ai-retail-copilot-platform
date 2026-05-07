import argparse
import asyncio
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.services.hallucination import HallucinationGuard
from app.services.llm import LLMService
from app.services.prompt_templates import retail_analyst_prompt

SCENARIOS = [
    {
        "name": "stockout-prevention",
        "task": "How do we reduce stockouts in dairy next week?",
        "context": "Replenishment trigger is below 2-day forecast. Dairy category is business-critical.",
    },
    {
        "name": "promo-safety",
        "task": "How should we monitor promotion safety for margin control?",
        "context": "Price changes must preserve minimum margin and be approved by pricing lead.",
    },
    {
        "name": "loyalty-prioritization",
        "task": "How should we prioritize loyalty campaigns this month?",
        "context": "Use RFM segmentation and prioritize high-value churn-risk audience first.",
    },
]


async def run_gate(
    provider: str,
    min_avg_confidence: float,
    max_high_risk: int,
    temperature: float,
) -> int:
    service = LLMService()
    guard = HallucinationGuard()
    rows: list[dict] = []

    for scenario in SCENARIOS:
        prompt = retail_analyst_prompt(task=scenario["task"], context=scenario["context"])
        result = await service.generate(prompt=prompt, provider=provider, temperature=temperature)
        quality = guard.evaluate(
            answer=str(result["output"]),
            contexts=[scenario["context"], scenario["task"], prompt],
        )
        rows.append(
            {
                "scenario": scenario["name"],
                "provider": result["provider"],
                "confidence": quality["confidence"],
                "risk_level": quality["risk_level"],
                "used_fallback": result["used_fallback"],
            }
        )

    avg_conf = round(sum(float(row["confidence"]) for row in rows) / max(1, len(rows)), 3)
    high_risk_count = sum(1 for row in rows if row["risk_level"] == "high")
    passed = avg_conf >= min_avg_confidence and high_risk_count <= max_high_risk

    payload = {
        "provider": provider,
        "thresholds": {
            "min_avg_confidence": min_avg_confidence,
            "max_high_risk": max_high_risk,
        },
        "result": {
            "avg_confidence": avg_conf,
            "high_risk_count": high_risk_count,
            "passed": passed,
        },
        "scenarios": rows,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if passed else 1


def main() -> None:
    parser = argparse.ArgumentParser(description="CI quality gate for LLM grounding and hallucination risk.")
    parser.add_argument("--provider", default="mock", help="mock|openai|claude")
    parser.add_argument("--min-avg-confidence", type=float, default=0.25)
    parser.add_argument("--max-high-risk", type=int, default=0)
    parser.add_argument("--temperature", type=float, default=0.2)
    args = parser.parse_args()

    exit_code = asyncio.run(
        run_gate(
            provider=args.provider,
            min_avg_confidence=args.min_avg_confidence,
            max_high_risk=args.max_high_risk,
            temperature=args.temperature,
        )
    )
    raise SystemExit(exit_code)


if __name__ == "__main__":
    main()

