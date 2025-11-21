from __future__ import annotations 

from todolist.models.project import Project
from todolist.repositories.project_db import ProjectDBRepository
from todolist.exceptions import DuplicateError, ValidationError, NotFoundError
from todolist.core.utils import print_table, validate_length
from todolist.core.constants import ERR_DUPLICATE_PROJECT, ERR_PROJECT_NOT_EXISTS

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from todolist.services.task_service import TaskService


class ProjectService:
    def __init__(self, project_repo: ProjectDBRepository):
        self.repo = project_repo

    def create_project(self, name: str, description: str):
        project = Project(name, description)
        self.repo.create(project)
        print(f"Project '{project.name}' created successfully.")
        return project

    def _get_all_projects(self):
        return self.repo.list_all()

    def list_projects(self):
        projects = self._get_all_projects()
        if not projects:
            print("No projects found.")
            return
        rows = [(p.id, p.name, p.description[:30]) for p in sorted(projects, key=lambda x: x.created_at)]
        print_table(rows, ["ID", "Name", "Description"])

    def list_projects_with_tasks(self, task_service: TaskService):
        projects = self._get_all_projects()
        if not projects:
            print("No projects found.")
            return

        for project in sorted(projects, key=lambda x: x.created_at):
            print(f"\n[{project.id[:8]}] {project.name}: {project.description[:50]}...")
            tasks = task_service.repo.list_by_project(project.id)
            if not tasks:
                print("  No tasks found for this project.")
            else:
                for t in tasks:
                    deadline = t.deadline.strftime("%Y-%m-%d") if t.deadline else "-"
                    print(f"  - [{t.id[:8]}] {t.title[:30]} ({t.status}) - Deadline: {deadline}")

    def edit_project(self, project_id: str, new_name: str, new_description: str):
        project = self.repo.get_by_id(project_id)
        validate_length("Project name", new_name, 3)
        validate_length("Project description", new_description, 10)

        # Check duplication
        all_projects = self.repo.list_all()
        for p in all_projects:
            if p.id != project.id and p.name.lower() == new_name.lower():
                raise DuplicateError(ERR_DUPLICATE_PROJECT.format(name=new_name))

        project.name = new_name.strip()
        project.description = new_description.strip()
        newProject = Project(new_name, new_description)
        self.repo.update(project_id ,newProject)
        print(f"Project '{project_id}' updated successfully.")
        return project

    def delete_project(self, project_id: str, task_service: TaskService):
        self.repo.delete(project_id)
        task_service.repo.delete_all_by_project(project_id)
        print(f"Project '{project_id}' and all its tasks deleted successfully.")

    def validate_project_exists(self, project_id: str):
        try:
            self.repo.get_by_id(project_id)
        except NotFoundError:
            raise ValidationError(ERR_PROJECT_NOT_EXISTS.format(project_id=project_id))
