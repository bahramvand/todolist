from __future__ import annotations

from datetime import date, datetime
from typing import List, Optional

from sqlalchemy import and_, select

from todolist.db.models import TaskDB
from todolist.db.session import get_session
from todolist.models.task import Task 


class TaskDBRepository:
    @staticmethod
    def _to_domain(model: TaskDB) -> Task:
        return Task(
            id=model.id,
            title=model.title,
            description=getattr(model, "description", None),
            status=model.status,
            deadline=model.deadline,
            created_at=model.created_at,
            closed_at=model.closed_at,
            project_id=model.project_id,
        )

    def create(self, task: Task) -> Task:
        with get_session() as session:
            db_task = TaskDB(
                title=task.title,
                description=getattr(task, "description", None),
                status=task.status,
                deadline=task.deadline,
                project_id=task.project_id,
            )
            session.add(db_task)
            session.flush()
            session.refresh(db_task)
            return self._to_domain(db_task)

    def get_by_id(self, task_id: int) -> Optional[Task]:
        with get_session() as session:
            stmt = select(TaskDB).where(TaskDB.id == task_id)
            result = session.execute(stmt).scalar_one_or_none()
            if result is None:
                return None
            return self._to_domain(result)

    def list_by_project(self, project_id: int) -> List[Task]:
        with get_session() as session:
            stmt = (
                select(TaskDB)
                .where(TaskDB.project_id == project_id)
                .order_by(TaskDB.id)
            )
            results = session.execute(stmt).scalars().all()
            return [self._to_domain(t) for t in results]

    def update_status(
        self,
        task_id: int,
        new_status: str,
        closed_at: Optional[datetime] = None,
    ) -> Optional[Task]:
        with get_session() as session:
            stmt = select(TaskDB).where(TaskDB.id == task_id)
            db_task = session.execute(stmt).scalar_one_or_none()
            if db_task is None:
                return None

            db_task.status = new_status
            db_task.closed_at = closed_at
            session.add(db_task)
            session.flush()
            session.refresh(db_task)
            return self._to_domain(db_task)

    def delete(self, task_id: int) -> None:
        with get_session() as session:
            stmt = select(TaskDB).where(TaskDB.id == task_id)
            db_task = session.execute(stmt).scalar_one_or_none()
            if db_task:
                session.delete(db_task)

    def list_overdue_open_tasks(self, today: date) -> List[Task]:
        with get_session() as session:
            stmt = select(TaskDB).where(
                and_(
                    TaskDB.deadline != None,  # noqa: E711
                    TaskDB.deadline < today,
                    TaskDB.status != "done",
                )
            )
            results = session.execute(stmt).scalars().all()
            return [self._to_domain(t) for t in results]
