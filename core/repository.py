from core.exceptions import NotFoundError, DuplicateError, LimitError
from models.project import Project
from models.task import Task
from core.constants import TASK_OF_NUMBER_MAX
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

class TaskRepository:
    """Handles CRUD."""

    def __init__(self):
        self._tasks = {}

    def add_task(self, project_id: str, task: Task):
        if project_id not in self._tasks:
            self._tasks[project_id] = []

        if len(self._tasks[project_id]) >= TASK_OF_NUMBER_MAX:
            raise LimitError(f"Cannot create more than {TASK_OF_NUMBER_MAX} tasks for this project.")

        self._tasks[project_id].append(task)

    def get_tasks_by_project(self, project_id: str):
        return self._tasks.get(project_id, [])

    def delete_all_by_project(self, project_id: str):
        if project_id in self._tasks:
            del self._tasks[project_id]