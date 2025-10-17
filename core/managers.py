from models.project import Project
from core.repository import ProjectRepository
from core.exceptions import DuplicateError, ValidationError, NotFoundError
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
