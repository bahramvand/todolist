from fastapi import FastAPI

from todolist.api.controllers.health_controller import router as health_router


def init_routers(app: FastAPI) -> None:
    app.include_router(health_router)
