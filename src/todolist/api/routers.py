from fastapi import FastAPI

from todolist.api.controllers.health_controller import router as health_router
from todolist.api.controllers.projects_controller import router as projects_router
from todolist.api.controllers.tasks_controller import router as tasks_router


def init_routers(app: FastAPI) -> None:
    app.include_router(health_router)
    app.include_router(projects_router)
    app.include_router(tasks_router)
