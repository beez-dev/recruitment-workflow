from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from core.dependencies import TokenData, get_current_user, require_reviewer
from database import get_db
from repositories import scores as score_repo
from schemas.candidates import (
    CandidateAdminDetailResponse,
    CandidateAdminResponse,
    CandidateDetailResponse,
    CandidateListResponse,
    CandidateResponse,
)
from schemas.scores import ScoreRequest, ScoreResponse
from services import candidates as candidate_service
from services import scores as score_service

router = APIRouter(prefix="/candidates", tags=["candidates"])


@router.get("", response_model=CandidateListResponse)
def list_candidates(
    status: Annotated[
        Literal["new", "reviewed", "hired", "rejected"] | None, Query()
    ] = None,
    role_applied: Annotated[str | None, Query()] = None,
    skill: Annotated[str | None, Query()] = None,
    keyword: Annotated[str | None, Query()] = None,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=50)] = 20,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(require_reviewer),
):
    items, total = candidate_service.list_candidates(
        db,
        status=status,
        role_applied=role_applied,
        skill=skill,
        keyword=keyword,
        page=page,
        page_size=page_size,
    )
    return CandidateListResponse(
        items=[CandidateResponse.model_validate(c) for c in items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{candidate_id}")
def get_candidate(
    candidate_id: int,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
):
    candidate = candidate_service.get_candidate(db, candidate_id)

    if current_user.role == "admin":
        scores = score_repo.get_by_candidate(db, candidate_id)
    else:
        scores = score_repo.get_by_candidate_and_reviewer(db, candidate_id, current_user.id)

    candidate.scores = scores

    if current_user.role == "admin":
        return CandidateAdminDetailResponse.model_validate(candidate)
    return CandidateDetailResponse.model_validate(candidate)


@router.post("/{candidate_id}/scores", response_model=ScoreResponse, status_code=201)
def submit_score(
    candidate_id: int,
    body: ScoreRequest,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(require_reviewer),
):
    return ScoreResponse.model_validate(
        score_service.submit_score(
            db,
            candidate_id=candidate_id,
            reviewer_id=current_user.id,
            category=body.category,
            score=body.score,
            note=body.note,
        )
    )


@router.post("/{candidate_id}/summary")
async def get_summary(
    candidate_id: int,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(require_reviewer),
):
    candidate = candidate_service.get_candidate(db, candidate_id)
    summary = await score_service.generate_summary(
        candidate_id=candidate.id,
        name=candidate.name,
        role_applied=candidate.role_applied,
    )
    return {"candidate_id": candidate_id, "summary": summary}
