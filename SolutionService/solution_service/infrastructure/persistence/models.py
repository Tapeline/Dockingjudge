from sqlalchemy import Integer, Enum, String, JSON, UUID
from sqlalchemy.orm import Mapped, mapped_column
import uuid

from solution_service.domain.entities.abstract import TaskType
from solution_service.infrastructure.persistence.database import Base


class SolutionModel(Base):
    __tablename__ = "solutions"

    uuid: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    contest_id: Mapped[int] = mapped_column(Integer)
    task_id: Mapped[int] = mapped_column(Integer)
    task_type: Mapped[str] = mapped_column(Enum(TaskType))
    user_id: Mapped[int] = mapped_column(Integer)
    score: Mapped[int] = mapped_column(Integer)
    short_verdict: Mapped[str] = mapped_column(String)
    answer: Mapped[str] = mapped_column(String)
    group_scores: Mapped[dict] = mapped_column(
        JSON,
        nullable=True,
        default=None
    )
    detailed_verdict: Mapped[str] = mapped_column(
        String,
        nullable=True,
        default=None
    )
