import sys

from todolist.cli.console import run_console
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
    run_console()

if __name__ == "__main__":
    main()
