from app.services.hallucination import HallucinationGuard


def test_hallucination_guard_high_confidence_when_grounded():
    guard = HallucinationGuard()
    result = guard.evaluate(
        answer="Stockout prevention requires daily review and replenishment requests.",
        contexts=[
            "If SKU stock drops below forecast coverage, trigger replenishment request.",
            "Store manager reviews exceptions daily.",
        ],
    )
    assert result["confidence"] >= 0.3
    assert result["risk_level"] in {"low", "medium"}


def test_hallucination_guard_high_risk_when_not_grounded():
    guard = HallucinationGuard()
    result = guard.evaluate(
        answer="Quantum pricing simulation guarantees 300 percent sales uplift.",
        contexts=["Promotion duration usually 7-14 days."],
    )
    assert result["risk_level"] == "high"
    assert result["confidence"] < 0.35

