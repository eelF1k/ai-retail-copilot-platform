from collections import Counter


class HallucinationGuard:
    def evaluate(self, answer: str, contexts: list[str]) -> dict:
        answer_tokens = self._tokens(answer)
        answer_counter = Counter(answer_tokens)
        context_tokens = self._tokens(" ".join(contexts))
        context_counter = Counter(context_tokens)

        overlap = sum(min(answer_counter[token], context_counter[token]) for token in answer_counter)
        grounding_score = overlap / max(1, len(answer_tokens))

        confidence = min(1.0, max(0.0, grounding_score * 1.25))
        risk_level = "low"
        warnings: list[str] = []

        if confidence < 0.3:
            risk_level = "high"
            warnings.append("Low grounding confidence: answer may include unsupported claims.")
        elif confidence < 0.55:
            risk_level = "medium"
            warnings.append("Partial grounding: validate key numbers before business action.")

        return {
            "confidence": round(confidence, 3),
            "grounding_score": round(grounding_score, 3),
            "risk_level": risk_level,
            "warnings": warnings,
        }

    @staticmethod
    def _tokens(text: str) -> list[str]:
        normalized = "".join(ch.lower() if ch.isalnum() else " " for ch in text)
        return [token for token in normalized.split() if token]

