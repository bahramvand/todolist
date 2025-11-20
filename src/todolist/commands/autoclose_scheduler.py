import time

import schedule

from todolist.commands.autoclose_overdue import run as run_autoclose_overdue


def run() -> None:
    """
    Run a simple scheduler that calls the auto-close command every day.

    By default: every day at 01:00 local time.
    """

    schedule.every().day.at("01:00").do(run_autoclose_overdue)

    print("[INFO] Auto-close scheduler started.")
    print("[INFO] It will run tasks:autoclose-overdue every day at 01:00.")

    while True:
        schedule.run_pending()
        time.sleep(60) # 1h = 60*60*24
