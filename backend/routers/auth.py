from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from core.config import COOKIE_SECURE
from database import get_db
from schemas.auth import LoginRequest, RegisterRequest, UserResponse
from services import auth as auth_service

router = APIRouter(prefix="/auth", tags=["auth"])

_ACCESS_COOKIE = "access_token"
_REFRESH_COOKIE = "refresh_token"
_ACCESS_MAX_AGE = 60 * 30        # 30 minutes
_REFRESH_MAX_AGE = 60 * 60 * 24 * 7  # 7 days


def _set_auth_cookies(response: Response, access_token: str, refresh_token: str) -> None:
    response.set_cookie(key=_ACCESS_COOKIE, value=access_token, httponly=True, secure=COOKIE_SECURE, samesite="lax", max_age=_ACCESS_MAX_AGE)
    response.set_cookie(key=_REFRESH_COOKIE, value=refresh_token, httponly=True, secure=COOKIE_SECURE, samesite="lax", max_age=_REFRESH_MAX_AGE)


@router.post("/register", response_model=UserResponse, status_code=201)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    return auth_service.register(db, email=payload.email, password=payload.password)


@router.post("/login", response_model=UserResponse)
def login(payload: LoginRequest, response: Response, db: Session = Depends(get_db)):
    user, access_token, refresh_token = auth_service.login(db, email=payload.email, password=payload.password)
    _set_auth_cookies(response, access_token, refresh_token)
    return user


@router.post("/refresh", response_model=UserResponse)
def refresh(response: Response, db: Session = Depends(get_db), refresh_token: str | None = Cookie(default=None)):
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No refresh token")
    user, access_token, new_refresh_token = auth_service.refresh(db, refresh_token)
    _set_auth_cookies(response, access_token, new_refresh_token)
    return user


@router.post("/logout")
def logout(response: Response, db: Session = Depends(get_db), refresh_token: str | None = Cookie(default=None)):
    auth_service.logout(db, refresh_token)
    response.delete_cookie(key=_ACCESS_COOKIE)
    response.delete_cookie(key=_REFRESH_COOKIE)
    return {"message": "Logged out"}
