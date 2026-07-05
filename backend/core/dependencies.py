from fastapi import Cookie, Depends, HTTPException, status
from pydantic import BaseModel

from core.security import decode_access_token


class TokenData(BaseModel):
    id: int
    email: str
    role: str


def get_current_user(access_token: str | None = Cookie(default=None)) -> TokenData:
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    payload = decode_access_token(access_token)
    return TokenData(id=payload["id"], email=payload["sub"], role=payload["role"])


def require_admin(current_user: TokenData = Depends(get_current_user)) -> TokenData:
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return current_user


def require_reviewer(current_user: TokenData = Depends(get_current_user)) -> TokenData:
    if current_user.role not in ("admin", "reviewer"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Reviewer access required")
    return current_user
