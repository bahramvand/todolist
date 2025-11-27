from __future__ import annotations
from datetime import date, datetime
from typing import List
from sqlalchemy import and_, select
from todolist.db.models import TaskDB
from todolist.db.session import get_session
from todolist.models.task import Task
from todolist.exceptions import NotFoundError
from todolist.core.constants import ERR_NOT_FOUND_TASK
from todolist.repositories.base import TaskRepository

class TaskDBRepository(TaskRepository):
    @staticmethod
    def _deadline_to_db(deadline) -> date | None:
        if deadline is None:
            return None
        if isinstance(deadline, datetime):
            return deadline.date()
        if isinstance(deadline, date):
            return deadline
        return None

    @staticmethod
    def _to_domain(model: TaskDB) -> Task:
        return Task(
            id=str(model.id),
            title=model.title,
            description=model.description or "",
            status=model.status,
            deadline=model.deadline,
            created_at=model.created_at,
            closed_at=model.closed_at,
            project_id=str(model.project_id),
        )

    def create(self, task: Task) -> Task:
        pid = int(task.project_id)
        with get_session() as session:
            db_task = TaskDB(
                title=task.title,
                description=task.description,
                status=task.status,
                deadline=self._deadline_to_db(task.deadline),
                project_id=pid,
            )
            session.add(db_task)
            session.flush()
            session.refresh(db_task)

            task.id = str(db_task.id)
            task.project_id = str(db_task.project_id)
            task.created_at = db_task.created_at
            task.closed_at = db_task.closed_at
            return task

    def get_by_id(self, task_id: str) -> Task:
        tid = int(task_id)
        with get_session() as session:
            stmt = select(TaskDB).where(TaskDB.id == tid)
            result = session.execute(stmt).scalar_one_or_none()
            if result is None:
                raise NotFoundError(
                    ERR_NOT_FOUND_TASK.format(task_id=task_id, project_id="N/A")
                )
            return self._to_domain(result)

    def list_by_project(self, project_id: str) -> List[Task]:
        pid = int(project_id)
        with get_session() as session:
            stmt = (
                select(TaskDB)
                .where(TaskDB.project_id == pid)
                .order_by(TaskDB.id)
            )
            results = session.execute(stmt).scalars().all()
            return [self._to_domain(t) for t in results]

    def update_task(self, new_task: Task) -> Task:
        if new_task.id is None:
            raise ValueError("Task id is required to update")

        tid = int(new_task.id)
        with get_session() as session:
            stmt = select(TaskDB).where(TaskDB.id == tid)
            db_task = session.execute(stmt).scalar_one_or_none()
            if db_task is None:
                raise NotFoundError(
                    ERR_NOT_FOUND_TASK.format(
                        task_id=new_task.id,
                        project_id=new_task.project_id or "N/A",
                    )
                )

            db_task.title = new_task.title
            db_task.description = new_task.description
            db_task.status = new_task.status
            db_task.deadline = self._deadline_to_db(new_task.deadline)
            db_task.closed_at = new_task.closed_at

            session.add(db_task)
            session.flush()
            session.refresh(db_task)
            return self._to_domain(db_task)

    def delete(self, task_id: str) -> None:
        tid = int(task_id)
        with get_session() as session:
            stmt = select(TaskDB).where(TaskDB.id == tid)
            db_task = session.execute(stmt).scalar_one_or_none()
            if db_task is None:
                raise NotFoundError(
                    ERR_NOT_FOUND_TASK.format(task_id=task_id, project_id="N/A")
                )
            session.delete(db_task)

    def delete_all_by_project(self, project_id: str) -> None:
        pid = int(project_id)
        with get_session() as session:
            stmt = select(TaskDB).where(TaskDB.project_id == pid)
            results = session.execute(stmt).scalars().all()
            for t in results:
                session.delete(t)

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
