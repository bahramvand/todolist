from models.project import Project
from models.task import Task
from core.repository import ProjectRepository
from core.exceptions import DuplicateError, ValidationError, NotFoundError
from core.repository import TaskRepository
from core.utils import print_table, validate_length

class ProjectManager:
    def __init__(self):
        self.repo = ProjectRepository()

    def create_project(self, name: str, description: str):
        validate_length("Project name", name, 3)
        validate_length("Project description", description, 10)

        project = Project(name, description)
        self.repo.add(project)
        print(f"Project '{project.name}' created successfully.")
        return project

    def list_projects(self):
        projects = self.repo.get_all()
        if not projects:
            print("No projects found.")
            return
        rows = [(p.id, p.name, p.description[:30]) for p in sorted(projects, key=lambda x: x.created_at)]
        print_table(rows, ["ID", "Name", "Description"])

    def edit_project(self, project_id: str, new_name: str, new_description: str):
        project = self.repo.get_by_id(project_id)
        validate_length("Project name", new_name, 3)
        validate_length("Project description", new_description, 10)

        # Check duplicataion
        all_projects = self.repo.get_all()
        for p in all_projects:
            if p.id != project.id and p.name.lower() == new_name.lower():
                raise DuplicateError(f"Project name '{new_name}' already exists.")

        project.name = new_name.strip()
        project.description = new_description.strip()
        print(f"Project '{project_id}' updated successfully.")
        return project

    def delete_project(self, project_id: str):
        self.repo.delete(project_id)
        # TODO cascade delete 
        print(f"Project '{project_id}' deleted successfully.")

class TaskManager:
    """Manages tasks inside projects."""

    def __init__(self):
        self.repo = TaskRepository()

    def create_task(self, project_id: str, title: str, description: str, status: str = "todo", deadline: str | None = None):
        
        task = Task(title, description, status, deadline)
        self.repo.add_task(project_id, task)
        print(f"Task '{task.title}' added successfully to project '{project_id}'.")
        return task

    def list_tasks(self, project_id: str):
        tasks = self.repo.get_tasks_by_project(project_id)
        if not tasks:
            print("No tasks found for this project.")
            return
        rows = [
            (t.id, t.title[:20], t.status, t.deadline.strftime("%Y-%m-%d") if t.deadline else "-")
            for t in tasks
        ]
        print_table(rows, ["ID", "Title", "Status", "Deadline"])