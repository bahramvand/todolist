from core.exceptions import NotFoundError, DuplicateError, LimitError
from models.project import Project
from core.constants import PROJECT_OF_NUMBER_MAX


class ProjectRepository:
    """Handles CRUD."""

    def __init__(self):
        self._projects = []

    def get_all(self):
        return list(self._projects)

    def get_by_id(self, project_id: str):
        for project in self._projects:
            if project.id == project_id:
                return project
        raise NotFoundError(f"Project with ID '{project_id}' not found.")

    def add(self, project: Project):
        if len(self._projects) >= PROJECT_OF_NUMBER_MAX:
            raise LimitError("Maximum project limit reached.")
        if any(p.name.lower() == project.name.lower() for p in self._projects):
            raise DuplicateError(f"Project name '{project.name}' already exists.")
        self._projects.append(project)

    def delete(self, project_id: str):
        for i, project in enumerate(self._projects):
            if project.id == project_id:
                del self._projects[i]
                return
        raise NotFoundError(f"Project with ID '{project_id}' not found.")
