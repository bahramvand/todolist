from typing import List, Optional

from sqlalchemy import select

from todolist.db.models import ProjectDB
from todolist.db.session import get_session
from todolist.models.project import Project  


class ProjectDBRepository:
    """PostgreSQL-backed repository for projects."""

    @staticmethod
    def _to_domain(model: ProjectDB) -> Project:
        return Project(
            id=model.id,
            name=model.name,
            description=getattr(model, "description", None),
            created_at=model.created_at,
        )

    def create(self, project: Project) -> Project:
        """Persist a new project and return it with DB-generated id."""
        with get_session() as session:
            db_project = ProjectDB(
                name=project.name,
                description=getattr(project, "description", None),
            )
            session.add(db_project)
            session.flush()
            session.refresh(db_project)
            return self._to_domain(db_project)

    def get_by_id(self, project_id: int) -> Optional[Project]:
        with get_session() as session:
            stmt = select(ProjectDB).where(ProjectDB.id == project_id)
            result = session.execute(stmt).scalar_one_or_none()
            if result is None:
                return None
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

    def delete(self, project_id: int) -> None:
        with get_session() as session:
            stmt = select(ProjectDB).where(ProjectDB.id == project_id)
            project = session.execute(stmt).scalar_one_or_none()
            if project:
                session.delete(project)
                # TODO