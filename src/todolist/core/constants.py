import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_OF_NUMBER_MAX = int(os.getenv("PROJECT_OF_NUMBER_MAX", 5))
TASK_OF_NUMBER_MAX = int(os.getenv("TASK_OF_NUMBER_MAX", 10))

VALID_STATUSES_STR = os.getenv("VALID_STATUSES", "todo,doing,done")
VALID_STATUSES = set(VALID_STATUSES_STR.split(","))

ERR_MIN_LENGTH = os.getenv("ERR_MIN_LENGTH", "{field_name} must have at least {min_length} characters.")
ERR_INVALID_DEADLINE = os.getenv("ERR_INVALID_DEADLINE", "Deadline must be in YYYY-MM-DD format.")
ERR_INVALID_STATUS = os.getenv("ERR_INVALID_STATUS", "Invalid status '{status}'. Must be one of {valid_statuses}.")
ERR_MAX_PROJECTS = os.getenv("ERR_MAX_PROJECTS", "Maximum project limit reached.")
ERR_MAX_TASKS = os.getenv("ERR_MAX_TASKS", "Cannot create more than {max_tasks} tasks for this project.")
ERR_DUPLICATE_PROJECT = os.getenv("ERR_DUPLICATE_PROJECT", "Project name '{name}' already exists.")
ERR_NOT_FOUND_PROJECT = os.getenv("ERR_NOT_FOUND_PROJECT", "Project with ID '{project_id}' not found.")
ERR_NOT_FOUND_TASK = os.getenv("ERR_NOT_FOUND_TASK", "Task with ID '{task_id}' not found in project '{project_id}'.")
ERR_NO_TASKS_PROJECT = os.getenv("ERR_NO_TASKS_PROJECT", "No tasks found for project '{project_id}'.")
ERR_INVALID_STATUS_UPDATE = os.getenv("ERR_INVALID_STATUS_UPDATE", "Invalid status. Must be one of: {valid_statuses}.")
ERR_PROJECT_NOT_EXISTS = os.getenv("ERR_PROJECT_NOT_EXISTS", "Project with ID '{project_id}' does not exist.")