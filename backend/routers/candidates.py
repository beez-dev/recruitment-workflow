from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas.candidates import CandidateResponse
from services import candidates as candidate_service

router = APIRouter(prefix="/candidates", tags=["candidates"])


@router.get("/{candidate_id}", response_model=CandidateResponse)
def get_candidate(candidate_id: int, db: Session = Depends(get_db)):
    return candidate_service.get_candidate(db, candidate_id)
