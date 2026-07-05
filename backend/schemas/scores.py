from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field


class ScoreRequest(BaseModel):
    category: str
    score: Annotated[int, Field(ge=1, le=5)]
    note: str | None = None


class ScoreResponse(BaseModel):
    id: int
    candidate_id: int
    category: str
    score: int
    reviewer_id: int
    note: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
