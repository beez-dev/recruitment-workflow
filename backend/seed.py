from database import SessionLocal
from models.candidate import Candidate
from models.score import Score


def seed():
    db = SessionLocal()
    try:
        if db.query(Candidate).first():
            print("Database already seeded, skipping.")
            return

        candidates = [
            Candidate(
                name="Alice Johnson",
                email="alice@example.com",
                role_applied="Backend Engineer",
                status="new",
                skills=["Python", "FastAPI", "PostgreSQL"],
                internal_notes="Strong systems background.",
            ),
            Candidate(
                name="Bob Smith",
                email="bob@example.com",
                role_applied="Frontend Engineer",
                status="reviewed",
                skills=["React", "TypeScript", "CSS"],
                internal_notes=None,
            ),
            Candidate(
                name="Carol White",
                email="carol@example.com",
                role_applied="Full Stack Engineer",
                status="hired",
                skills=["Python", "React", "Docker"],
                internal_notes="Excellent culture fit.",
            ),
            Candidate(
                name="David Lee",
                email="david@example.com",
                role_applied="Backend Engineer",
                status="rejected",
                skills=["Java", "Spring Boot"],
                internal_notes="Not enough Python experience.",
            ),
        ]

        db.add_all(candidates)
        db.flush()

        scores = [
            Score(candidate_id=candidates[0].id, category="Technical", score=4, reviewer_id=1, note="Solid fundamentals."),
            Score(candidate_id=candidates[0].id, category="Communication", score=3, reviewer_id=1, note="Could be clearer."),
            Score(candidate_id=candidates[1].id, category="Technical", score=5, reviewer_id=2, note="Excellent React knowledge."),
            Score(candidate_id=candidates[2].id, category="Technical", score=5, reviewer_id=1, note="Impressive full stack skills."),
            Score(candidate_id=candidates[2].id, category="Culture Fit", score=5, reviewer_id=2, note="Great team player."),
            Score(candidate_id=candidates[3].id, category="Technical", score=2, reviewer_id=1, note="Weak on required stack."),
        ]

        db.add_all(scores)
        db.commit()
        print(f"Seeded {len(candidates)} candidates and {len(scores)} scores.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
