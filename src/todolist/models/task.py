from datetime import datetime, date
from todolist.exceptions import ValidationError
from todolist.core.utils import validate_length
from todolist.core.constants import (
    VALID_STATUSES,
    ERR_INVALID_STATUS,
    ERR_INVALID_DEADLINE,
)


class Task:
    def __init__(
        self,
        title: str,
        description: str,
        status: str = "todo",
        deadline: str | date | datetime | None = None,
        id: str | None = None,
        created_at: datetime | None = None,
        closed_at: datetime | None = None,
        project_id: str | None = None,
    ):
        validate_length("Task title", title, 3)
        validate_length("Task description", description, 10)

        if status not in VALID_STATUSES:
            raise ValidationError(
                ERR_INVALID_STATUS.format(
                    status=status,
                    valid_statuses=", ".join(VALID_STATUSES),
                )
            )

        self.id = id

        self.title = title.strip()
        self.description = description.strip()
        self.status = status
        self.deadline = self._validate_deadline(deadline)
        self.created_at = created_at or datetime.now()
        self.closed_at = closed_at
        self.project_id = project_id

    def _validate_deadline(self, deadline):
        if not deadline:
            return None

        if isinstance(deadline, (datetime, date)):
            return deadline

        try:
            return datetime.strptime(deadline, "%Y-%m-%d")
        except ValueError:
            raise ValidationError(ERR_INVALID_DEADLINE)

    def __str__(self):
        short_id = self.id[:8] if self.id else "????????"
        return f"[{short_id}] {self.title} ({self.status})"
