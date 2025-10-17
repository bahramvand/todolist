import uuid
from datetime import datetime
from core.constants import TASK_OF_NUMBER_MAX
from core.exceptions import ValidationError
from core.utils import validate_length

VALID_STATUSES = {"todo", "doing", "done"}


class Task:
    """Represents a task belonging to a project."""

    def __init__(self, title: str, description: str, status: str = "todo", deadline: str | None = None):
        validate_length("Task title", title, 3)
        validate_length("Task description", description, 10)

        if status not in VALID_STATUSES:
            raise ValidationError(f"Invalid status '{status}'. Must be one of {VALID_STATUSES}.")

        self.id = str(uuid.uuid4())
        self.title = title.strip()
        self.description = description.strip()
        self.status = status
        self.deadline = self._validate_deadline(deadline)
        self.created_at = datetime.now()

    def _validate_deadline(self, deadline: str | None):
        if not deadline:
            return None
        try:
            return datetime.strptime(deadline, "%Y-%m-%d")
        except ValueError:
            raise ValidationError("Deadline must be in YYYY-MM-DD format.")

    def __str__(self):
        return f"[{self.id[:8]}] {self.title} ({self.status})"
