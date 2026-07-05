import asyncio

from sqlalchemy.orm import Session

from models.score import Score
from repositories import scores as score_repo
from services.candidates import get_candidate


def submit_score(
    db: Session,
    *,
    candidate_id: int,
    reviewer_id: int,
    category: str,
    score: int,
    note: str | None,
) -> Score:
    get_candidate(db, candidate_id)  # 404 if not found
    return score_repo.create(
        db,
        candidate_id=candidate_id,
        reviewer_id=reviewer_id,
        category=category,
        score=score,
        note=note,
    )


async def generate_summary(candidate_id: int, name: str, role_applied: str) -> str:
    await asyncio.sleep(2)
    return (
        f"{name} is a strong candidate for the {role_applied} role. "
        "Based on the submitted scores, they demonstrate solid technical skills "
        "and good communication. Recommended for next-stage interview."
    )
