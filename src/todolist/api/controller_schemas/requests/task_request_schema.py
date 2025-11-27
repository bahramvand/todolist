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
    deadline: Optional[str] = Field(
        None,
        description="Optional deadline in YYYY-MM-DD format.",
        examples=["2025-01-01"],
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
    deadline: Optional[str] = Field(
        None,
        description="New deadline in YYYY-MM-DD format (optional).",
        examples=["2025-02-01"],
    )
    status: Optional[str] = Field(
        None,
        description="New status of the task (e.g. todo,doing,done).",
        examples=["doing"],
    )
