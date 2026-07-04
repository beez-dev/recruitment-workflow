from sqlalchemy.orm import Session

from models.candidate import Candidate


def get_by_id(db: Session, candidate_id: int) -> Candidate | None:
    return db.query(Candidate).filter(Candidate.id == candidate_id).first()
