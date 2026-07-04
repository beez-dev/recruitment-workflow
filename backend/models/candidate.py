from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

if TYPE_CHECKING:
    from models.score import Score


class Candidate(Base):
    __tablename__ = "candidates"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    role_applied: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(
        Enum("new", "reviewed", "hired", "rejected", name="candidate_status"),
        default="new",
    )
    skills: Mapped[list] = mapped_column(JSON, default=list)
    internal_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    scores: Mapped[list["Score"]] = relationship(back_populates="candidate")
