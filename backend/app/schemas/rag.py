from pydantic import BaseModel, Field


class RAGRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=2000)
    top_k: int = Field(default=3, ge=1, le=10)


class Citation(BaseModel):
    source_id: str
    title: str
    snippet: str


class RAGResponse(BaseModel):
    question: str
    answer: str
    citations: list[Citation]
    context_count: int
    confidence: float
    grounding_score: float
    risk_level: str
    warnings: list[str]

