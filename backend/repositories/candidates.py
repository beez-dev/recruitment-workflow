from sqlalchemy import func
from sqlalchemy.orm import Session

from models.candidate import Candidate


def get_by_id(db: Session, candidate_id: int) -> Candidate | None:
    return db.query(Candidate).filter(Candidate.id == candidate_id).first()


def get_list(
    db: Session,
    *,
    status: str | None,
    role_applied: str | None,
    skill: str | None,
    keyword: str | None,
    page: int,
    page_size: int,
) -> tuple[list[Candidate], int]:
    # using a query builder; .all() sends the full
    # SELECT ... WHERE ... ORDER BY ... LIMIT ... OFFSET ...
    q = db.query(Candidate)

    if status:
        q = q.filter(Candidate.status == status)
    if role_applied:
        q = q.filter(Candidate.role_applied.ilike(f"%{role_applied}%"))
    if skill:
        q = q.filter(Candidate.skills.contains(skill))
    if keyword:
        q = q.filter(
            Candidate.name.ilike(f"%{keyword}%") | Candidate.email.ilike(f"%{keyword}%")
        )

    total = q.with_entities(func.count(Candidate.id)).scalar()
    items = q.order_by(Candidate.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return items, total
