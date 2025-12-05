from __future__ import annotations

from datetime import date, datetime
from typing import List, Optional

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from todolist.db.base import Base

from todolist.core.constants import (
    TASK_TITLE_MAX_LENGTH,
    PROJECT_NAME_MAX_LENGTH,
    TASK_DESCRIPTION_MAX_LENGTH,
    PROJECT_DESCRIPTION_MAX_LENGTH,
)

class ProjectDB(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(PROJECT_NAME_MAX_LENGTH), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(PROJECT_DESCRIPTION_MAX_LENGTH), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )

    tasks: Mapped[List["TaskDB"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
    )


class TaskDB(Base):
    """ORM model for tasks table."""

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    title: Mapped[str] = mapped_column(String(TASK_TITLE_MAX_LENGTH), nullable=False)

    description: Mapped[Optional[str]] = mapped_column(String(TASK_DESCRIPTION_MAX_LENGTH), nullable=True)

    status: Mapped[str] = mapped_column(String(32), nullable=False, default="todo")
    deadline: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    closed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
    )

    project: Mapped[ProjectDB] = relationship(back_populates="tasks")