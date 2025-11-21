import sys

from todolist.services import ProjectService, TaskService
from todolist.repositories.project_db import ProjectDBRepository
from todolist.repositories.task_db import TaskDBRepository
from todolist.commands.autoclose_overdue import run as run_autoclose_overdue
from todolist.commands.autoclose_scheduler import run as run_autoclose_scheduler

def main():
    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "tasks:autoclose-overdue":
            run_autoclose_overdue()
            return

        if command == "tasks:start-autoclose-scheduler":
            run_autoclose_scheduler()
            return
    
    project_repo = ProjectDBRepository()
    task_repo = TaskDBRepository()

    project_service = ProjectService(project_repo)
    task_service = TaskService(task_repo, project_service)

    while True:
        print("\n=== ToDoList CLI ===")
        print("1.  Create new project")
        print("2.  List projects")
        print("3.  Edit project")
        print("4.  Delete project")
        print("5.  Create new task")
        print("6.  List tasks of a project")
        print("7.  Edit task")
        print("8.  Change task status")
        print("9.  Delete task")
        print("10. List all projects with tasks")
        print("11. Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            name = input("Enter project name: ")
            desc = input("Enter project description: ")
            try:
                project_service.create_project(name, desc)
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "2":
            project_service.list_projects()

        elif choice == "3":
            """
            Why don't I validate the ID here?
            Because I want my classes to follow the Single Responsibility Principle (SRP) and only handle their own core responsibilities—classes shouldn't receive or manipulate user input directly.
            Instead, I perform validation and input handling in the CLI layer (here in main.py) to maintain separation of concerns and keep the code cleaner.
            If the ID is invalid, the edit_project method will raise its own Exception, which gets caught here.
            """
            pid = input("Enter project ID to edit: ")
            new_name = input("Enter new name: ")
            new_desc = input("Enter new description: ")
            try:
                project_service.edit_project(pid, new_name, new_desc)
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "4":
            pid = input("Enter project ID to delete: ")
            try:
                project_service.delete_project(pid, task_service)
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "5":
            """
            Why don't I validate the ID here?
            Because I want my classes to follow the Single Responsibility Principle (SRP) and only handle their own core responsibilities—classes shouldn't receive or manipulate user input directly.
            Instead, I perform validation and input handling in the CLI layer (here in main.py) to maintain separation of concerns and keep the code cleaner.
            If the ID is invalid, the edit_project method will raise its own Exception, which gets caught here.
            """
            pid = input("Enter project ID: ")
            title = input("Enter task title: ")
            desc = input("Enter task description: ")
            status = input("Enter status (todo/doing/done) [default: todo]: ") or "todo"
            deadline = input("Enter deadline (YYYY-MM-DD) [optional]: ") or None
            try:
                task_service.create_task(pid, title, desc, status, deadline)
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "6":
            pid = input("Enter project ID: ")
            task_service.list_tasks(pid)

        elif choice == "7":
            tid = input("Enter task ID to edit: ")
            title = input("Enter new title: ")
            desc = input("Enter new description: ")
            status = input("Enter new status (todo/doing/done): ")
            deadline = input("Enter new deadline (YYYY-MM-DD) [optional]: ") or None
            try:
                task_service.update_task(tid, title, desc, status, deadline)
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "8":
            tid = input("Enter task ID: ")
            status = input("Enter new status (todo/doing/done): ")
            try:
                task_service.change_status(tid, status)
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "9":
            tid = input("Enter task ID to delete: ")
            try:
                task_service.delete_task(tid)
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "10":
            try:
                project_service.list_projects_with_tasks(task_service)
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "11":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
