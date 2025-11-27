from fastapi import APIRouter
from todolist.api.controller_schemas.responses.health_response_schema import (
    HealthResponse,
)

router = APIRouter(
    prefix="/api/health",
    tags=["health"],
)


@router.get(
    "",
    response_model=HealthResponse,
    summary="Health check",
    description="Simple endpoint to check if the API is up and running.",
)
async def health_check() -> HealthResponse:

    return HealthResponse(status="ok")
