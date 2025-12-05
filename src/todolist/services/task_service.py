from __future__ import annotations

from todolist.models.task import Task, VALID_STATUSES
from todolist.repositories.task_db import TaskDBRepository
from todolist.exceptions import ValidationError, LimitError
from todolist.core.utils import print_table, validate_length
from todolist.core.constants import (
    ERR_INVALID_STATUS_UPDATE,
    TASK_OF_NUMBER_MAX,
    ERR_MAX_TASKS,
    TASK_TITLE_MIN_LENGTH,
    TASK_TITLE_MAX_LENGTH,
    TASK_DESCRIPTION_MIN_LENGTH,
    TASK_DESCRIPTION_MAX_LENGTH,
)

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from todolist.services.project_service import ProjectService



class TaskService:
    def __init__(self, task_repo: TaskDBRepository, project_service: ProjectService):
        self.repo = task_repo
        self.project_manager = project_service
    
    def create_task(
        self,
        project_id: str,
        title: str,
        description: str,
        status: str = "todo",
        deadline: str | None = None,
    ):
        self.project_manager.validate_project_exists(project_id)

        existing_tasks = self.repo.list_by_project(project_id)
        if len(existing_tasks) >= TASK_OF_NUMBER_MAX:
            raise LimitError(ERR_MAX_TASKS.format(max_tasks=TASK_OF_NUMBER_MAX))

        validate_length(
            "Task title",
            title,
            TASK_TITLE_MIN_LENGTH,
            TASK_TITLE_MAX_LENGTH,
        )
        validate_length(
            "Task description",
            description,
            TASK_DESCRIPTION_MIN_LENGTH,
            TASK_DESCRIPTION_MAX_LENGTH,
        )

        task = Task(title, description, status, deadline, project_id=project_id)
        self.repo.create(task)
        print(f"Task '{task.title}' added successfully to project '{project_id}'.")
        return task

    def list_tasks(self, project_id: str):
        tasks = self.repo.list_by_project(project_id)
        if not tasks:
            print("No tasks found for this project.")
            return
        rows = [
            (t.id, t.title[:20], t.status, t.deadline.strftime("%Y-%m-%d") if t.deadline else "-")
            for t in tasks
        ]
        print_table(rows, ["ID", "Title", "Status", "Deadline"])

    def update_task(self, task_id: str, new_title: str, new_desc: str, new_status: str, new_deadline: str | None):
        new_task = self.repo.get_by_id(task_id)

        validate_length(
            "Task title",
            new_title,
            TASK_TITLE_MIN_LENGTH,
            TASK_TITLE_MAX_LENGTH,
        )
        validate_length(
            "Task description",
            new_desc,
            TASK_DESCRIPTION_MIN_LENGTH,
            TASK_DESCRIPTION_MAX_LENGTH,
        )

        if new_status not in VALID_STATUSES:
            raise ValidationError(ERR_INVALID_STATUS_UPDATE.format(valid_statuses=", ".join(VALID_STATUSES)))

        new_task.title = new_title.strip()
        new_task.description = new_desc.strip()
        new_task.status = new_status
        if new_deadline:
            new_task.deadline = new_task._validate_deadline(new_deadline)

        self.repo.update_task(new_task)
        print(f"Task '{task_id}' updated successfully.")

    def change_status(self, task_id: str, new_status: str):
        if new_status not in VALID_STATUSES:
            raise ValidationError(ERR_INVALID_STATUS_UPDATE.format(valid_statuses=", ".join(VALID_STATUSES)))
        task = self.repo.get_by_id(task_id)
        task.status = new_status
        self.repo.update_task(task)
        print(f"Task '{task_id}' status updated to '{new_status}'.")

    def delete_task(self, task_id: str):
        self.repo.delete(task_id)
        print(f"Task '{task_id}' deleted successfully.")
