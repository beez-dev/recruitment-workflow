import random

from database import SessionLocal
from models.candidate import Candidate

FIRST_NAMES = [
    "Alice", "Bob", "Carol", "David", "Eve", "Frank", "Grace", "Hank",
    "Iris", "Jack", "Karen", "Liam", "Mia", "Noah", "Olivia", "Paul",
    "Quinn", "Rachel", "Sam", "Tara", "Uma", "Victor", "Wendy", "Xander",
    "Yara", "Zoe", "Aaron", "Beth", "Carlos", "Diana", "Ethan", "Fiona",
    "George", "Hannah", "Ivan", "Julia", "Kevin", "Laura", "Marcus", "Nina",
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Wilson", "Taylor", "Anderson", "Thomas", "Jackson", "White",
    "Harris", "Martin", "Thompson", "Young", "Walker", "Hall", "Allen",
    "King", "Wright", "Scott", "Green", "Baker", "Adams", "Nelson", "Carter",
    "Mitchell", "Roberts", "Turner", "Phillips", "Campbell", "Parker",
]

ROLES = [
    "Backend Engineer",
    "Frontend Engineer",
    "Full Stack Engineer",
    "DevOps Engineer",
    "Data Engineer",
    "ML Engineer",
    "Mobile Engineer",
    "Platform Engineer",
    "Security Engineer",
    "QA Engineer",
]

SKILLS_BY_ROLE = {
    "Backend Engineer":   ["Python", "FastAPI", "PostgreSQL", "Redis", "Docker", "Go", "Node.js", "SQL"],
    "Frontend Engineer":  ["React", "TypeScript", "CSS", "Tailwind", "Next.js", "Vue", "GraphQL", "Webpack"],
    "Full Stack Engineer":["Python", "React", "Docker", "TypeScript", "Node.js", "PostgreSQL", "REST APIs"],
    "DevOps Engineer":    ["Kubernetes", "Docker", "Terraform", "AWS", "CI/CD", "Linux", "Helm", "Ansible"],
    "Data Engineer":      ["Python", "Spark", "Airflow", "SQL", "dbt", "Kafka", "Redshift", "Snowflake"],
    "ML Engineer":        ["Python", "PyTorch", "TensorFlow", "scikit-learn", "MLflow", "Pandas", "Kubernetes"],
    "Mobile Engineer":    ["React Native", "Swift", "Kotlin", "Flutter", "iOS", "Android", "TypeScript"],
    "Platform Engineer":  ["Kubernetes", "Go", "Terraform", "AWS", "GCP", "Docker", "gRPC", "Linux"],
    "Security Engineer":  ["Python", "Penetration Testing", "SIEM", "IAM", "AWS", "Splunk", "Network Security"],
    "QA Engineer":        ["Selenium", "Cypress", "Python", "Jest", "Playwright", "REST APIs", "CI/CD"],
}

STATUSES = ["new", "reviewed", "hired", "rejected"]

INTERNAL_NOTES = [
    "Strong communication skills, good culture fit.",
    "Impressive portfolio, recommend for next round.",
    "Needs more experience with distributed systems.",
    "Excellent problem-solving demonstrated in interview.",
    "Strong fundamentals but lacks specific stack experience.",
    "Outstanding technical assessment submission.",
    "Good candidate, follow up in 3 months.",
    None, None, None,  # some candidates have no notes
]


def seed():
    db = SessionLocal()
    try:
        existing = db.query(Candidate).count()
        if existing > 0:
            print(f"Clearing {existing} existing candidates…")
            db.query(Candidate).delete()
            db.commit()

        random.seed(42)
        used_emails: set[str] = set()
        candidates = []

        for i in range(120):
            first = FIRST_NAMES[i % len(FIRST_NAMES)]
            last = LAST_NAMES[i % len(LAST_NAMES)]
            # ensure unique emails by appending index when needed
            base_email = f"{first.lower()}.{last.lower()}"
            email = f"{base_email}@example.com"
            if email in used_emails:
                email = f"{base_email}{i}@example.com"
            used_emails.add(email)

            role = ROLES[i % len(ROLES)]
            all_skills = SKILLS_BY_ROLE[role]
            skills = random.sample(all_skills, k=random.randint(2, min(4, len(all_skills))))
            status = STATUSES[i % len(STATUSES)]
            note = INTERNAL_NOTES[i % len(INTERNAL_NOTES)]

            candidates.append(Candidate(
                name=f"{first} {last}",
                email=email,
                role_applied=role,
                status=status,
                skills=skills,
                internal_notes=note,
            ))

        db.add_all(candidates)
        db.commit()
        print(f"Seeded {len(candidates)} candidates.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
