from models.project import Project
from core.constants import PROJECT_OF_NUMBER_MAX
from core.exceptions import LimitError, DuplicateError
from core.utils import print_table

class ProjectManager:
    def __init__(self):
        self.projects = []

    def create_project(self, name: str, description: str):
        if len(self.projects) >= PROJECT_OF_NUMBER_MAX:
            raise LimitError(f"Cannot create more than {PROJECT_OF_NUMBER_MAX} projects.")

        if any(p.name.lower() == name.lower() for p in self.projects):
            raise DuplicateError(f"Project name '{name}' already exists.")

        project = Project(name, description)
        self.projects.append(project)
        print(f"✅ Project '{project.name}' created successfully.")
        return project

    def list_projects(self):
        if not self.projects:
            print("No projects found.")
            return

        sorted_projects = sorted(self.projects, key=lambda x: x.created_at)
        rows = [(p.id[:8], p.name, p.description[:30]) for p in sorted_projects]
        print_table(rows, headers=["ID", "Name", "Description"])
