from typing import List

from fastapi import APIRouter, HTTPException, status

from todolist.api.controller_schemas.requests.project_request_schema import (
    ProjectCreateRequest,
    ProjectUpdateRequest,
)
from todolist.api.controller_schemas.responses.project_response_schema import (
    ProjectResponse,
)
from todolist.core.constants import ERR_DUPLICATE_PROJECT
from todolist.exceptions import NotFoundError
from todolist.models.project import Project
from todolist.repositories.project_db import ProjectDBRepository
from todolist.repositories.task_db import TaskDBRepository

router = APIRouter(
    prefix="/api/projects",
    tags=["projects"],
)


def _project_to_response(project: Project) -> ProjectResponse:
    return ProjectResponse(
        id=project.id,
        name=project.name,
        description=project.description,
        created_at=project.created_at,
    )


@router.get(
    "",
    response_model=List[ProjectResponse],
    summary="List all projects",
    description="Returns all projects ordered by ID.",
)
def list_projects() -> List[ProjectResponse]:
    repo = ProjectDBRepository()
    projects = repo.list_all()
    return [_project_to_response(p) for p in projects]


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Get project by ID",
    description="Returns a single project by its ID.",
)
def get_project(project_id: str) -> ProjectResponse:
    repo = ProjectDBRepository()
    try:
        project = repo.get_by_id(project_id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    return _project_to_response(project)


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new project",
    description="Creates a new project with unique name.",
)
def create_project(payload: ProjectCreateRequest) -> ProjectResponse:
    repo = ProjectDBRepository()

    existing_projects = repo.list_all()
    normalized_new_name = payload.name.strip().lower()

    if any(p.name.lower() == normalized_new_name for p in existing_projects):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=ERR_DUPLICATE_PROJECT.format(name=payload.name),
        )

    project = Project(
        name=payload.name,
        description=payload.description,
    )

    created_project = repo.create(project)
    return _project_to_response(created_project)


@router.put(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Update project",
    description=(
        "Updates project name and/or description. "
        "If a field is not provided, its previous value will be kept."
    ),
)
def update_project(project_id: str, payload: ProjectUpdateRequest) -> ProjectResponse:
    repo = ProjectDBRepository()

    try:
        project = repo.get_by_id(project_id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    new_name = payload.name.strip() if payload.name is not None else project.name
    new_description = (
        payload.description.strip()
        if payload.description is not None
        else project.description
    )

    all_projects = repo.list_all()
    if any(
        p.id != project.id and p.name.lower() == new_name.lower()
        for p in all_projects
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=ERR_DUPLICATE_PROJECT.format(name=new_name),
        )

    new_project = Project(
        name=new_name,
        description=new_description,
    )
    new_project.id = project.id
    new_project.created_at = project.created_at

    try:
        updated = repo.update(project_id, new_project)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    return _project_to_response(updated)


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete project",
    description=(
        "Deletes a project and all its tasks. "
        "If project does not exist, returns 404."
    ),
)
def delete_project(project_id: str) -> None:
    project_repo = ProjectDBRepository()
    task_repo = TaskDBRepository()

    try:
        project_repo.delete(project_id)
        task_repo.delete_all_by_project(project_id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    return
