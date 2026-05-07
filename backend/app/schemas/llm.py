from pydantic import BaseModel, Field


class PromptRunRequest(BaseModel):
    task: str = Field(..., min_length=2, max_length=2000)
    context: str = Field(default="", max_length=8000)
    temperature: float = Field(default=0.2, ge=0.0, le=1.5)


class PromptRunResponse(BaseModel):
    provider: str
    model: str
    prompt: str
    output: str
    used_fallback: bool

