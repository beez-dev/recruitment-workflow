from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.dependencies import TokenData, get_current_user
from database import get_db
from schemas.candidates import CandidateAdminResponse, CandidateResponse
from services import candidates as candidate_service

router = APIRouter(prefix="/candidates", tags=["candidates"])

@router.get("/{candidate_id}")
def get_candidate(
    candidate_id: int,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
):
    candidate = candidate_service.get_candidate(db, candidate_id)
    if current_user.role == "admin":
        return CandidateAdminResponse.model_validate(candidate)
    return CandidateResponse.model_validate(candidate)
