from app.rag.retriever import KnowledgeRetriever


def test_retriever_returns_top_contexts():
    retriever = KnowledgeRetriever()
    contexts = retriever.retrieve("How to prevent stockout for dairy products?", top_k=2)
    assert len(contexts) == 2
    assert any(item["source_id"] == "ops-stockout-002" for item in contexts)

