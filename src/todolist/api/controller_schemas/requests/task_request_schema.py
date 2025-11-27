from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TaskCreateRequest(BaseModel):
    title: str = Field(
        ...,
        min_length=3,
        max_length=255,
        description="Task title (at least 3 characters).",
        examples=["Buy milk"],
    )
    description: Optional[str] = Field(
        None,
        description="Optional task description.",
        examples=["Buy 2 liters of milk from the store."],
    )
    due_date: Optional[datetime] = Field(
        None,
        description="Optional due date for the task.",
        examples=["2025-01-01T12:00:00"],
    )


class TaskUpdateRequest(BaseModel):
    title: Optional[str] = Field(
        None,
        min_length=3,
        max_length=255,
        description="New task title (optional).",
        examples=["Buy bread instead of milk"],
    )
    description: Optional[str] = Field(
        None,
        description="New task description (optional).",
    )
    due_date: Optional[datetime] = Field(
        None,
        description="New due date (optional).",
        examples=["2025-02-01T09:00:00"],
    )
    status: Optional[str] = Field(
        None,
        description="New status of the task (e.g. todo, in_progress, done).",
        examples=["in_progress"],
    )
