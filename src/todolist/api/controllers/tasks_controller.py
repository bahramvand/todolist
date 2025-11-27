from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, status

from todolist.api.controller_schemas.requests.task_request_schema import (
    TaskCreateRequest,
    TaskUpdateRequest,
)
from todolist.api.controller_schemas.responses.task_response_schema import (
    TaskResponse,
)
from todolist.api.dependencies import get_project_repo, get_task_repo
from todolist.core.constants import ERR_NOT_FOUND_TASK
from todolist.exceptions import NotFoundError, ValidationError
from todolist.models.task import Task
from todolist.repositories.project_db import ProjectDBRepository
from todolist.repositories.task_db import TaskDBRepository

router = APIRouter(
    prefix="/api/projects/{project_id}/tasks",
    tags=["tasks"],
)


def _task_to_response(task: Task) -> TaskResponse:
    return TaskResponse(
        id=task.id,
        project_id=task.project_id,
        title=task.title,
        description=task.description,
        status=task.status,
        deadline=task.deadline,
        created_at=task.created_at,
    )


def _ensure_project_exists(
    project_id: str,
    project_repo: ProjectDBRepository,
) -> None:
    try:
        project_repo.get_by_id(project_id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.get(
    "",
    response_model=List[TaskResponse],
    summary="List tasks for a project",
    description="Returns all tasks belonging to the given project.",
)
def list_tasks(
    project_id: str = Path(..., description="ID of the project to list tasks for."),
    project_repo: ProjectDBRepository = Depends(get_project_repo),
    task_repo: TaskDBRepository = Depends(get_task_repo),
) -> List[TaskResponse]:
    _ensure_project_exists(project_id, project_repo)

    tasks = task_repo.list_by_project(project_id)
    return [_task_to_response(t) for t in tasks]


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Get task details",
    description="Returns a single task by its ID within the given project.",
)
def get_task(
    project_id: str = Path(..., description="ID of the project."),
    task_id: str = Path(..., description="ID of the task."),
    project_repo: ProjectDBRepository = Depends(get_project_repo),
    task_repo: TaskDBRepository = Depends(get_task_repo),
) -> TaskResponse:
    _ensure_project_exists(project_id, project_repo)

    try:
        task = task_repo.get_by_id(task_id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    if task.project_id != project_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERR_NOT_FOUND_TASK.format(task_id=task_id, project_id=project_id),
        )

    return _task_to_response(task)


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new task for a project",
    description="Creates a new task under the given project.",
)
def create_task(
    payload: TaskCreateRequest,
    project_id: str = Path(..., description="ID of the project."),
    project_repo: ProjectDBRepository = Depends(get_project_repo),
    task_repo: TaskDBRepository = Depends(get_task_repo),
) -> TaskResponse:
    _ensure_project_exists(project_id, project_repo)

    try:
        task = Task(
            title=payload.title,
            description=payload.description or "",
            project_id=project_id,
            deadline=payload.deadline,
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    created_task = task_repo.create(task)
    return _task_to_response(created_task)


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Update task",
    description=(
        "Updates task fields (title, description, deadline, status). "
        "Only provided fields will be changed."
    ),
)
def update_task(
    payload: TaskUpdateRequest,
    project_id: str = Path(..., description="ID of the project."),
    task_id: str = Path(..., description="ID of the task."),
    project_repo: ProjectDBRepository = Depends(get_project_repo),
    task_repo: TaskDBRepository = Depends(get_task_repo),
) -> TaskResponse:
    _ensure_project_exists(project_id, project_repo)

    try:
        existing_task = task_repo.get_by_id(task_id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    if existing_task.project_id != project_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERR_NOT_FOUND_TASK.format(task_id=task_id, project_id=project_id),
        )

    new_title = payload.title.strip() if payload.title is not None else existing_task.title
    new_description = (
        payload.description.strip()
        if payload.description is not None
        else existing_task.description
    )
    new_deadline = (
        payload.deadline if payload.deadline is not None else existing_task.deadline
    )
    new_status = payload.status if payload.status is not None else existing_task.status

    try:
        updated_task = Task(
            title=new_title,
            description=new_description or "",
            status=new_status,
            deadline=new_deadline,
            project_id=existing_task.project_id,
            id=existing_task.id,
            created_at=existing_task.created_at,
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    saved_task = task_repo.update_task(updated_task)
    return _task_to_response(saved_task)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete task",
    description="Deletes a single task from the project.",
)
def delete_task(
    project_id: str = Path(..., description="ID of the project."),
    task_id: str = Path(..., description="ID of the task."),
    project_repo: ProjectDBRepository = Depends(get_project_repo),
    task_repo: TaskDBRepository = Depends(get_task_repo),
) -> None:
    _ensure_project_exists(project_id, project_repo)

    try:
        task = task_repo.get_by_id(task_id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    if task.project_id != project_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERR_NOT_FOUND_TASK.format(task_id=task_id, project_id=project_id),
        )

    task_repo.delete(task_id)
    return
