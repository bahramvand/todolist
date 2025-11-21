from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from datetime import date

from todolist.models.project import Project
from todolist.models.task import Task


class ProjectRepository(ABC):
    @abstractmethod
    def list_all(self) -> List[Project]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, project_id: str) -> Project:
        raise NotImplementedError

    @abstractmethod
    def create(self, project: Project) -> Project:
        raise NotImplementedError

    @abstractmethod
    def delete(self, project_id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, project_id: str, new_project: Project) -> Project:
        raise NotImplementedError


class TaskRepository(ABC):
    @abstractmethod
    def get_by_id(self, task_id: str) -> Task:
        raise NotImplementedError

    @abstractmethod
    def list_by_project(self, project_id: str) -> List[Task]:
        raise NotImplementedError

    @abstractmethod
    def create(self, task: Task) -> Task:
        raise NotImplementedError

    @abstractmethod
    def update_task(self, task: Task) -> Task:
        raise NotImplementedError
    
    @abstractmethod
    def delete_all_by_project(self, project_id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, task_id: str) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def list_overdue_open_tasks(self, today: date) -> List[Task]:
      raise NotImplementedError
