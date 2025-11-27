from fastapi import FastAPI

from todolist.api.routers import init_routers


def create_app() -> FastAPI:
    app = FastAPI(
        title="ToDoList API",
        version="0.1.0",
        description="Web API for ToDoList project.",
    )

    init_routers(app)

    return app


app = create_app()
