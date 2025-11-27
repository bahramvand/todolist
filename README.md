# todolist

## Run Database

```bash
docker compose up -d db
```

## Stop Everything

```bash
docker compose down
```

## Install Dependencies

```bash
poetry install
```

## Run Migrations

```bash
poetry run alembic upgrade head
```

## Run CLI

```bash
poetry run todolist
```

## Run FastAPI Server

```bash
poetry run uvicorn todolist.web_app:app
```

## Autoclose Overdue Tasks (once)

```bash
poetry run todolist tasks:autoclose-overdue
```

## Start Autoclose Scheduler

```bash
poetry run todolist tasks:start-autoclose-scheduler
```

----------

## Environment configuration (.env)

This project uses a `.env` file for configuration.
Most limits, statuses, and error messages are configurable there and are loaded via
`python-dotenv` and the `todolist.core.settings` / `todolist.core.constants` modules.

Typical usage:

```bash
cp .env.example .env
```

In the `.env` file you can configure for example:

- **Database settings**: `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`

- **Business rules**:

  - `PROJECT_OF_NUMBER_MAX`, `TASK_OF_NUMBER_MAX`

  - `VALID_STATUSES` for tasks

- **Error messages** (all `ERR_...` variables), e.g.:

  - `ERR_MIN_LENGTH`

  - `ERR_INVALID_STATUS`

  - `ERR_INVALID_DEADLINE`

  - `ERR_NOT_FOUND_PROJECT`, `ERR_NOT_FOUND_TASK`

  - `ERR_DUPLICATE_PROJECT`

All these values are used by the domain layer and the Web API, so changing them in `.env`
will change the behavior and messages without modifying the code.

----------

## API Endpoints (overview)

In addition to the CLI commands above, the project exposes a RESTful Web API.

### Base URL

By default (when running locally):

- `http://127.0.0.1:8000`

### Documentation

- Swagger UI: `http://127.0.0.1:8000/docs`

- ReDoc: `http://127.0.0.1:8000/redoc`

### Health

- `GET /api/health`

### Projects

- `GET /api/projects` – list all projects

- `GET /api/projects/{project_id}` – get a single project

- `POST /api/projects` – create a new project

- `PUT /api/projects/{project_id}` – update an existing project

- `DELETE /api/projects/{project_id}` – delete a project and its tasks

### Tasks

- `GET /api/projects/{project_id}/tasks` – list tasks of a project

- `GET /api/projects/{project_id}/tasks/{task_id}` – get a single task

- `POST /api/projects/{project_id}/tasks` – create a new task in a project

- `PUT /api/projects/{project_id}/tasks/{task_id}` – update a task (status, title, etc.)

- `DELETE /api/projects/{project_id}/tasks/{task_id}` – delete a task

All validations (lengths, valid statuses, deadline format, etc.) and error messages are
handled by the domain layer and use the texts defined in `.env`.

----------

## API Test Commands

### List Projects

**_Bash_**

```bash
curl http://127.0.0.1:8000/api/projects
```

**_PowerShell_**

```powershell
iwr http://127.0.0.1:8000/api/projects | Select -Expand Content
```

### Create Project

**_Bash_**

```bash
curl -X POST http://127.0.0.1:8000/api/projects -H "Content-Type: application/json" -d '{"name":"My Project","description":"Created via API"}'
```

**_PowerShell_**

```powershell
iwr -Uri http://127.0.0.1:8000/api/projects -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"name":"My Project","description":"Created via API"}'
```

### Get Project (id=1)

**_Bash_**

```bash
curl http://127.0.0.1:8000/api/projects/1
```

**_PowerShell_**

```powershell
iwr http://127.0.0.1:8000/api/projects/1 | Select -Expand Content
```

### Update Project (id=1)

**_Bash_**

```bash
curl -X PUT http://127.0.0.1:8000/api/projects/1 -H "Content-Type: application/json" -d '{"name":"Updated Name","description":"New description"}'
```

**_PowerShell_**

```powershell
iwr -Uri http://127.0.0.1:8000/api/projects/1 -Method PUT -Headers @{"Content-Type"="application/json"} -Body '{"name":"Updated Name","description":"New description"}'
```

### Delete Project (id=1)

**_Bash_**

```bash
curl -X DELETE http://127.0.0.1:8000/api/projects/1
```

**_PowerShell_**

```powershell
iwr -Uri http://127.0.0.1:8000/api/projects/1 -Method DELETE
```

### List Tasks (project id=1)

**_Bash_**

```bash
curl http://127.0.0.1:8000/api/projects/1/tasks
```

**_PowerShell_**

```powershell
iwr http://127.0.0.1:8000/api/projects/1/tasks | Select -Expand Content
```

### Create Task (project id=1)

**_Bash_**

```bash
curl -X POST http://127.0.0.1:8000/api/projects/1/tasks -H "Content-Type: application/json" -d '{"title":"First task","description":"Do something important"}'
```

**_PowerShell_**

```powershell
iwr -Uri http://127.0.0.1:8000/api/projects/1/tasks -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"title":"First task","description":"Do something important"}'
```

### Get Task (project id=1, task id=1)

**_Bash_**

```bash
curl http://127.0.0.1:8000/api/projects/1/tasks/1
```

**_PowerShell_**

```powershell
iwr http://127.0.0.1:8000/api/projects/1/tasks/1 | Select -Expand Content
```

### Update Task (project id=1, task id=1)

**_Bash_**

```bash
curl -X PUT http://127.0.0.1:8000/api/projects/1/tasks/1 -H "Content-Type: application/json" -d '{"status":"done"}'
```

**_PowerShell_**

```powershell
iwr -Uri http://127.0.0.1:8000/api/projects/1/tasks/1 -Method PUT -Headers @{"Content-Type"="application/json"} -Body '{"status":"done"}'
```

### Delete Task (project id=1, task id=1)

**_Bash_**

```bash
curl -X DELETE http://127.0.0.1:8000/api/projects/1/tasks/1
```

**_PowerShell_**

```powershell
iwr -Uri http://127.0.0.1:8000/api/projects/1/tasks/1 -Method DELETE
```
