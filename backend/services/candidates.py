from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.candidate import Candidate
from repositories import candidates as candidate_repo


def get_candidate(db: Session, candidate_id: int) -> Candidate:
    candidate = candidate_repo.get_by_id(db, candidate_id)
    if not candidate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Candidate {candidate_id} not found")
    return candidate
