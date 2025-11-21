from todolist.exceptions import DuplicateError, NotFoundError
from todolist.models.project import Project
from todolist.models.task import Task
from todolist.core.constants import TASK_OF_NUMBER_MAX, PROJECT_OF_NUMBER_MAX, ERR_MAX_PROJECTS, ERR_MAX_TASKS, ERR_DUPLICATE_PROJECT, ERR_NOT_FOUND_PROJECT, ERR_NOT_FOUND_TASK, ERR_NO_TASKS_PROJECT

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
        raise NotFoundError(ERR_NOT_FOUND_PROJECT.format(project_id=project_id))

    def add(self, project: Project):
        if len(self._projects) >= PROJECT_OF_NUMBER_MAX:
            raise LimitError(ERR_MAX_PROJECTS)
        if any(p.name.lower() == project.name.lower() for p in self._projects):
            raise DuplicateError(ERR_DUPLICATE_PROJECT.format(name=project.name))
        self._projects.append(project)

    def delete(self, project_id: str):
        for i, project in enumerate(self._projects):
            if project.id == project_id:
                del self._projects[i]
                return
        raise NotFoundError(ERR_NOT_FOUND_PROJECT.format(project_id=project_id))

class TaskRepository:
    """Handles CRUD."""

    def __init__(self):
        self._tasks = {}

    def add_task(self, project_id: str, task: Task):
        if project_id not in self._tasks:
            self._tasks[project_id] = []

        if len(self._tasks[project_id]) >= TASK_OF_NUMBER_MAX:
            raise LimitError(ERR_MAX_TASKS.format(max_tasks=TASK_OF_NUMBER_MAX))
        
        self._tasks[project_id].append(task)

    def get_tasks_by_project(self, project_id: str):
        return self._tasks.get(project_id, [])

    def delete_all_by_project(self, project_id: str):
        if project_id in self._tasks:
            del self._tasks[project_id]
    
    def get_task(self, project_id: str, task_id: str):
        tasks = self._tasks.get(project_id, [])
        for task in tasks:
            if task.id == task_id:
                return task
        raise NotFoundError(ERR_NOT_FOUND_TASK.format(task_id=task_id, project_id=project_id))

    def delete_task(self, project_id: str, task_id: str):
        if project_id not in self._tasks:
            raise NotFoundError(ERR_NO_TASKS_PROJECT.format(project_id=project_id))
        for i, task in enumerate(self._tasks[project_id]):
            if task.id == task_id:
                del self._tasks[project_id][i]
                return
        raise NotFoundError(ERR_NOT_FOUND_TASK.format(task_id=task_id, project_id=project_id))

    def update_task(self, project_id: str, updated_task):
        if project_id not in self._tasks:
            raise NotFoundError(ERR_NO_TASKS_PROJECT.format(project_id=project_id))
        for i, task in enumerate(self._tasks[project_id]):
            if task.id == updated_task.id:
                self._tasks[project_id][i] = updated_task
                return
        raise NotFoundError(ERR_NOT_FOUND_TASK.format(task_id=updated_task.id, project_id=project_id))
