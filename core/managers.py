from models.project import Project
from models.task import Task, VALID_STATUSES
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

    def _get_all_projects(self):
        return self.repo.get_all()

    def list_projects(self):
        projects = self._get_all_projects()
        if not projects:
            print("No projects found.")
            return
        rows = [(p.id, p.name, p.description[:30]) for p in sorted(projects, key=lambda x: x.created_at)]
        print_table(rows, ["ID", "Name", "Description"])

    def list_projects_with_tasks(self, task_manager: 'TaskManager'):
        projects = self._get_all_projects() 
        if not projects:
            print("No projects found.")
            return

        for project in sorted(projects, key=lambda x: x.created_at):
            print(f"\n[{project.id[:8]}] {project.name}: {project.description[:50]}...")
            tasks = task_manager.repo.get_tasks_by_project(project.id)
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

        # Check duplicataion
        all_projects = self.repo.get_all()
        for p in all_projects:
            if p.id != project.id and p.name.lower() == new_name.lower():
                raise DuplicateError(f"Project name '{new_name}' already exists.")

        project.name = new_name.strip()
        project.description = new_description.strip()
        print(f"Project '{project_id}' updated successfully.")
        return project

    def delete_project(self, project_id: str, task_manager: 'TaskManager'):
        self.repo.delete(project_id)
        task_manager.repo.delete_all_by_project(project_id)
        print(f"Project '{project_id}' and all its tasks deleted successfully.")
    
    def validate_project_exists(self, project_id: str):
        try:
            self.repo.get_by_id(project_id)
        except NotFoundError:
            raise ValidationError(f"Project with ID '{project_id}' does not exist.")    
    
class TaskManager:
    """Manages tasks inside projects."""

    def __init__(self, project_manager: ProjectManager):
        self.repo = TaskRepository()
        self.project_manager = project_manager  
        
    def create_task(self, project_id: str, title: str, description: str, status: str = "todo", deadline: str | None = None):
        self.project_manager.validate_project_exists(project_id)

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
        
    def update_task(self, project_id: str, task_id: str, new_title: str, new_desc: str, new_status: str, new_deadline: str | None):
        task = self.repo.get_task(project_id, task_id)

        validate_length("Task title", new_title, 3)
        validate_length("Task description", new_desc, 10)

        if new_status not in VALID_STATUSES:
            raise ValidationError("Invalid status. Must be one of: todo, doing, done.")

        task.title = new_title.strip()
        task.description = new_desc.strip()
        task.status = new_status
        if new_deadline:
            task.deadline = task._validate_deadline(new_deadline)

        self.repo.update_task(project_id, task)
        print(f"Task '{task_id}' updated successfully.")

    def change_status(self, project_id: str, task_id: str, new_status: str):
        if new_status not in {"todo", "doing", "done"}:
            raise ValidationError("Invalid status. Must be one of: todo, doing, done.")
        task = self.repo.get_task(project_id, task_id)
        task.status = new_status
        self.repo.update_task(project_id, task)
        print(f"Task '{task_id}' status updated to '{new_status}'.")

    def delete_task(self, project_id: str, task_id: str):
        self.repo.delete_task(project_id, task_id)
        print(f"Task '{task_id}' deleted successfully.")