from pydantic import BaseModel, Field


class SQLQueryRequest(BaseModel):
    sql: str = Field(..., min_length=1, max_length=3000)
    max_rows: int = Field(default=200, ge=1, le=1000)


class SQLQueryResponse(BaseModel):
    allowed: bool
    reason: str
    rows: list[dict]
    returned_rows: int

