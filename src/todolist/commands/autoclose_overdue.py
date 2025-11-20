from datetime import date, datetime
from todolist.repositories.task_db import TaskDBRepository


def run() -> None:
    """
    Close all overdue, non-done tasks.

    Overdue = deadline < today AND status != "done"
    """
    repo = TaskDBRepository()
    today = date.today()

    overdue_tasks = repo.list_overdue_open_tasks(today)

    if not overdue_tasks:
        print(f"[INFO] No overdue tasks found for {today}.")
        return

    print(f"[INFO] Found {len(overdue_tasks)} overdue tasks. Closing them...")

    closed_count = 0
    now = datetime.now()

    for task in overdue_tasks:
        task.status = "done"
        task.closed_at = now

        repo.update_task(task)
        closed_count += 1

    print(
        f"[INFO] Auto-closed {closed_count} tasks with deadline before {today} "
        f"and status != 'done'."
    )
