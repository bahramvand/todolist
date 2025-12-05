from pydantic import BaseModel, Field
from todolist.core.constants import (
    PROJECT_NAME_MIN_LENGTH,
    PROJECT_NAME_MAX_LENGTH,
    PROJECT_DESCRIPTION_MIN_LENGTH,
    PROJECT_DESCRIPTION_MAX_LENGTH,
)

class ProjectCreateRequest(BaseModel):
    name: str = Field(
        ...,
        min_length=PROJECT_NAME_MIN_LENGTH,
        max_length=PROJECT_NAME_MAX_LENGTH,
        description=f"Project name (between {PROJECT_NAME_MIN_LENGTH} and {PROJECT_NAME_MAX_LENGTH} characters).",
        examples=["My Project"],
    )
    description: str = Field(
        ...,
        min_length=PROJECT_DESCRIPTION_MIN_LENGTH,
        max_length=PROJECT_DESCRIPTION_MAX_LENGTH,
        description=f"Project description (between {PROJECT_DESCRIPTION_MIN_LENGTH} and {PROJECT_DESCRIPTION_MAX_LENGTH} characters).",
        examples=["This is my awesome todo project."],
    )


class ProjectUpdateRequest(BaseModel):
    name: str | None = Field(
        None,
        min_length=PROJECT_NAME_MIN_LENGTH,
        max_length=PROJECT_NAME_MAX_LENGTH,
        description="New project name (optional).",
        examples=["Updated Project Name"],
    )
    description: str | None = Field(
        None,
        min_length=PROJECT_DESCRIPTION_MIN_LENGTH,
        max_length=PROJECT_DESCRIPTION_MAX_LENGTH,
        description="New project description (optional).",
        examples=["Updated description for this project."],
    )
