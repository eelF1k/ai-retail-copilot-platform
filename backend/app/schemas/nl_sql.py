from pydantic import BaseModel, Field


class NL2SQLRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=2000)
    max_rows: int = Field(default=100, ge=1, le=1000)


class NL2SQLResponse(BaseModel):
    question: str
    sql: str
    allowed: bool
    rows: list[dict]
    row_count: int
    summary: str
    confidence: float
    grounding_score: float
    risk_level: str
    warnings: list[str]

