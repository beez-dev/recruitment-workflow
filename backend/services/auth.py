from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from core.config import ADMIN_EMAIL, REFRESH_TOKEN_EXPIRE_DAYS
from core.security import create_access_token, generate_refresh_token, hash_password, verify_password
from models.user import User
from repositories import refresh_tokens as refresh_token_repo
from repositories import users as user_repo


def register(db: Session, email: str, password: str) -> User:
    if user_repo.get_by_email(db, email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    role = "admin" if email == ADMIN_EMAIL else "reviewer" #admin identified by env variable setup ( only 1 admin )
    return user_repo.create(db, email=email, hashed_password=hash_password(password), role=role)


def login(db: Session, email: str, password: str) -> tuple[User, str, str]:
    user = user_repo.get_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token({"sub": user.email, "id": user.id, "role": user.role})
    refresh_token = generate_refresh_token()
    expires_at = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token_repo.upsert(db, token=refresh_token, user_id=user.id, expires_at=expires_at)

    return user, access_token, refresh_token


def refresh(db: Session, refresh_token: str) -> tuple[User, str, str]:
    record = refresh_token_repo.get_by_token(db, refresh_token)
    if not record or record.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token")

    user = db.get(User, record.user_id)

    new_access_token = create_access_token({"sub": user.email, "id": user.id, "role": user.role})
    new_refresh_token = generate_refresh_token()
    expires_at = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token_repo.rotate(db, old_token=refresh_token, new_token=new_refresh_token, expires_at=expires_at)

    return user, new_access_token, new_refresh_token


def logout(db: Session, refresh_token: str | None) -> None:
    if refresh_token:
        refresh_token_repo.delete_by_token(db, refresh_token)
