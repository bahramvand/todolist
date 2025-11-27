from pydantic import BaseModel, Field


class ProjectCreateRequest(BaseModel):
    name: str = Field(
        ...,
        min_length=3,
        max_length=255,
        description="Project name (must be at least 3 characters).",
        examples=["My Project"],
    )
    description: str = Field(
        ...,
        min_length=10,
        description="Project description (must be at least 10 characters).",
        examples=["This is my awesome todo project."],
    )


class ProjectUpdateRequest(BaseModel):
    name: str | None = Field(
        None,
        min_length=3,
        max_length=255,
        description="New project name (optional).",
        examples=["Updated Project Name"],
    )
    description: str | None = Field(
        None,
        min_length=10,
        description="New project description (optional).",
        examples=["Updated description for this project."],
    )
