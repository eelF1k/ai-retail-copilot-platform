from collections import Counter
from typing import Any

from app.rag.knowledge_base import KNOWLEDGE_BASE


class KnowledgeRetriever:
    def retrieve(self, question: str, top_k: int = 3) -> list[dict[str, Any]]:
        q_tokens = self._tokens(question)
        q_counter = Counter(q_tokens)
        scored: list[tuple[float, dict[str, Any]]] = []

        for doc in KNOWLEDGE_BASE:
            text = str(doc["text"])
            t_tokens = self._tokens(text)
            t_counter = Counter(t_tokens)
            overlap = sum(min(q_counter[token], t_counter[token]) for token in q_counter)
            density = overlap / max(1, len(t_tokens))
            score = overlap + density
            scored.append((score, doc))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [doc for _, doc in scored[:top_k]]

    @staticmethod
    def _tokens(text: str) -> list[str]:
        normalized = "".join(ch.lower() if ch.isalnum() else " " for ch in text)
        return [token for token in normalized.split() if token]

