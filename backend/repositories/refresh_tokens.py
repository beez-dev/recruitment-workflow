from datetime import datetime

from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import Session

from core.security import hash_refresh_token
from models.refresh_token import RefreshToken


def upsert(db: Session, token: str, user_id: int, expires_at: datetime) -> None:
    stmt = insert(RefreshToken).values(
        token_hash=hash_refresh_token(token),
        user_id=user_id,
        expires_at=expires_at,
        created_at=datetime.utcnow(),
    ).on_conflict_do_update(
        index_elements=["user_id"],
        set_={"token_hash": hash_refresh_token(token), "expires_at": expires_at},
    )
    db.execute(stmt)
    db.commit()


def get_by_token(db: Session, token: str) -> RefreshToken | None:
    return db.query(RefreshToken).filter(RefreshToken.token_hash == hash_refresh_token(token)).first()


def rotate(db: Session, old_token: str, new_token: str, expires_at: datetime) -> None:
    db.query(RefreshToken).filter(RefreshToken.token_hash == hash_refresh_token(old_token)).update({
        "token_hash": hash_refresh_token(new_token),
        "expires_at": expires_at,
    })
    db.commit()


def delete_by_token(db: Session, token: str) -> None:
    db.query(RefreshToken).filter(RefreshToken.token_hash == hash_refresh_token(token)).delete()
    db.commit()
