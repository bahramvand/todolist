from typing import List, Optional
from sqlalchemy import select
from todolist.db.models import ProjectDB
from todolist.db.session import get_session
from todolist.models.project import Project
from todolist.exceptions import NotFoundError
from todolist.core.constants import ERR_NOT_FOUND_PROJECT


class ProjectDBRepository:
    @staticmethod
    def _to_domain(model: ProjectDB) -> Project:
        return Project(
            id=str(model.id),
            name=model.name,
            description=model.description or "",
            created_at=model.created_at,
        )

    def create(self, project: Project) -> Project:
        with get_session() as session:
            db_project = ProjectDB(
                name=project.name,
                description=project.description,
            )
            session.add(db_project)
            session.flush()
            session.refresh(db_project)

            project.id = str(db_project.id)
            project.created_at = db_project.created_at
            return project

    def get_by_id(self, project_id: str) -> Project:
        pid = int(project_id)
        with get_session() as session:
            stmt = select(ProjectDB).where(ProjectDB.id == pid)
            result = session.execute(stmt).scalar_one_or_none()
            if result is None:
                raise NotFoundError(
                    ERR_NOT_FOUND_PROJECT.format(project_id=project_id)
                )
            return self._to_domain(result)

    def get_by_name(self, name: str) -> Optional[Project]:
        with get_session() as session:
            stmt = select(ProjectDB).where(ProjectDB.name == name)
            result = session.execute(stmt).scalar_one_or_none()
            if result is None:
                return None
            return self._to_domain(result)

    def list_all(self) -> List[Project]:
        with get_session() as session:
            stmt = select(ProjectDB).order_by(ProjectDB.id)
            results = session.execute(stmt).scalars().all()
            return [self._to_domain(p) for p in results]

    def delete(self, project_id: str) -> None:
        pid = int(project_id)
        with get_session() as session:
            stmt = select(ProjectDB).where(ProjectDB.id == pid)
            project = session.execute(stmt).scalar_one_or_none()
            if project is None:
                raise NotFoundError(
                    ERR_NOT_FOUND_PROJECT.format(project_id=project_id)
                )
            session.delete(project)

    def update(self, project_id: str, new_project: Project) -> Project:
        pid = int(project_id)
        with get_session() as session:
            stmt = select(ProjectDB).where(ProjectDB.id == pid)
            db_project = session.execute(stmt).scalar_one_or_none()
            if db_project is None:
                raise NotFoundError(
                    ERR_NOT_FOUND_PROJECT.format(project_id=project_id)
                )

            db_project.name = new_project.name
            db_project.description = new_project.description
            session.add(db_project)
            session.flush()
            session.refresh(db_project)
            return self._to_domain(db_project)
