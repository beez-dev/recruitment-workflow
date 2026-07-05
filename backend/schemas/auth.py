from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: Literal["admin", "reviewer"]
    created_at: datetime

    model_config = {"from_attributes": True}
