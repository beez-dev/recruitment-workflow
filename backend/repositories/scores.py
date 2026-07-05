from sqlalchemy.orm import Session

from models.score import Score


def create(
    db: Session,
    *,
    candidate_id: int,
    reviewer_id: int,
    category: str,
    score: int,
    note: str | None,
) -> Score:
    record = Score(
        candidate_id=candidate_id,
        reviewer_id=reviewer_id,
        category=category,
        score=score,
        note=note,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_by_candidate(db: Session, candidate_id: int) -> list[Score]:
    return db.query(Score).filter(Score.candidate_id == candidate_id).all()


def get_by_candidate_and_reviewer(
    db: Session, candidate_id: int, reviewer_id: int
) -> list[Score]:
    return (
        db.query(Score)
        .filter(Score.candidate_id == candidate_id, Score.reviewer_id == reviewer_id)
        .all()
    )
