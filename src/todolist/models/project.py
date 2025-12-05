from datetime import datetime

from todolist.core.utils import validate_length
from todolist.core.constants import (
    PROJECT_NAME_MIN_LENGTH,
    PROJECT_NAME_MAX_LENGTH,
    PROJECT_DESCRIPTION_MIN_LENGTH,
    PROJECT_DESCRIPTION_MAX_LENGTH,
)


class Project:
    def __init__(
        self,
        name: str,
        description: str,
        id: str | None = None,
        created_at: datetime | None = None,
    ):
        validate_length(
            "Project name",
            name,
            PROJECT_NAME_MIN_LENGTH,
            PROJECT_NAME_MAX_LENGTH,
        )
        validate_length(
            "Project description",
            description,
            PROJECT_DESCRIPTION_MIN_LENGTH,
            PROJECT_DESCRIPTION_MAX_LENGTH,
        )

        self.id = id

        self.name = name.strip()
        self.description = description.strip()
        self.created_at = created_at or datetime.now()

    def __str__(self):
        short_id = self.id[:8] if self.id else "????????"
        return f"[{short_id}] {self.name} - {self.description[:40]}..."
