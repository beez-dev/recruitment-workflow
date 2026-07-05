from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.candidate import Candidate
from repositories import candidates as candidate_repo


def get_candidate(db: Session, candidate_id: int) -> Candidate:
    candidate = candidate_repo.get_by_id(db, candidate_id)
    if not candidate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Candidate {candidate_id} not found")
    return candidate


def list_candidates(
    db: Session,
    *,
    status: str | None = None,
    role_applied: str | None = None,
    skill: str | None = None,
    keyword: str | None = None,
    page: int = 1,
    page_size: int = 20,
) -> tuple[list[Candidate], int]:
    return candidate_repo.get_list(
        db,
        status=status,
        role_applied=role_applied,
        skill=skill,
        keyword=keyword,
        page=page,
        page_size=page_size,
    )
