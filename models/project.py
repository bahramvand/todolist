import uuid
from datetime import datetime
from core.constants import PROJECT_OF_NUMBER_MAX
from core.exceptions import ValidationError, LimitError
from core.utils import validate_length


class Project:
    def __init__(self, name: str, description: str):
        validate_length("Project name", name, 3)
        validate_length("Project description", description, 10)
        self.id = str(uuid.uuid4())
        self.name = name.strip()
        self.description = description.strip()
        self.created_at = datetime.now()

    def __str__(self):
        return f"[{self.id}] {self.name} - {self.description[:40]}..."
