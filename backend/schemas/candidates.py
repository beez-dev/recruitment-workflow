from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr


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
