from datetime import datetime
from todolist.core.utils import validate_length


class Project:
    def __init__(
        self,
        name: str,
        description: str,
        id: str | None = None,
        created_at: datetime | None = None,
    ):
        validate_length("Project name", name, 3)
        validate_length("Project description", description, 10)

        self.id = id

        self.name = name.strip()
        self.description = description.strip()
        self.created_at = created_at or datetime.now()

    def __str__(self):
        short_id = self.id[:8] if self.id else "????????"
        return f"[{short_id}] {self.name} - {self.description[:40]}..."
