from pydantic import BaseModel, Field


class LLMCompareRequest(BaseModel):
    task: str = Field(..., min_length=3, max_length=2000)
    context: str = Field(default="", max_length=8000)
    providers: list[str] = Field(default_factory=lambda: ["mock", "openai", "claude"])
    temperature: float = Field(default=0.2, ge=0.0, le=1.5)


class LLMCompareItem(BaseModel):
    provider: str
    model: str
    output: str
    used_fallback: bool


class LLMCompareResponse(BaseModel):
    prompt: str
    results: list[LLMCompareItem]

