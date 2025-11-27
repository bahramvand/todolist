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
