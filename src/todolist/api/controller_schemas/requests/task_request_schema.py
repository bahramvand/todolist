from typing import Optional

from pydantic import BaseModel, Field

from todolist.core.constants import (
    TASK_TITLE_MIN_LENGTH,
    TASK_TITLE_MAX_LENGTH,
    TASK_DESCRIPTION_MIN_LENGTH,
    TASK_DESCRIPTION_MAX_LENGTH,
)



class TaskCreateRequest(BaseModel):
    title: str = Field(
        ...,
        min_length=TASK_TITLE_MIN_LENGTH,
        max_length=TASK_TITLE_MAX_LENGTH,
        description="Task title.",
        examples=["Buy milk"],
    )
    description: Optional[str] = Field(
        None,
        min_length=TASK_DESCRIPTION_MIN_LENGTH,
        max_length=TASK_DESCRIPTION_MAX_LENGTH,
        description="Optional task description.",
        examples=["Buy 2L of milk from the supermarket."],
    )
    deadline: Optional[str] = Field(
        None,
        description="Optional deadline in YYYY-MM-DD format.",
        examples=["2025-01-01"],
    )


class TaskUpdateRequest(BaseModel):
    title: str = Field(
        ...,
        min_length=TASK_TITLE_MIN_LENGTH,
        max_length=TASK_TITLE_MAX_LENGTH,
        description="Task title.",
        examples=["Buy milk"],
    )
    description: Optional[str] = Field(
        None,
        min_length=TASK_DESCRIPTION_MIN_LENGTH,
        max_length=TASK_DESCRIPTION_MAX_LENGTH,
        description="Optional task description.",
        examples=["Buy 2L of milk from the supermarket."],
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
