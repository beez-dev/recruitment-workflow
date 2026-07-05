from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr

from schemas.scores import ScoreResponse


class CandidateResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role_applied: str
    status: Literal["new", "reviewed", "hired", "rejected"]
    skills: list[str]
    created_at: datetime

    model_config = {"from_attributes": True}


class CandidateAdminResponse(CandidateResponse):
    internal_notes: str | None


class CandidateDetailResponse(CandidateResponse):
    scores: list[ScoreResponse]


class CandidateAdminDetailResponse(CandidateAdminResponse):
    scores: list[ScoreResponse]


class CandidateListResponse(BaseModel):
    items: list[CandidateResponse]
    total: int
    page: int
    page_size: int
