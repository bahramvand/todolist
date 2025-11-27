from todolist.repositories.project_db import ProjectDBRepository
from todolist.repositories.task_db import TaskDBRepository


def get_project_repo() -> ProjectDBRepository:
    return ProjectDBRepository()


def get_task_repo() -> TaskDBRepository:
    return TaskDBRepository()
