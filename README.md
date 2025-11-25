# todolist

1. اجرای دیتابیس:
   docker compose up -d db
   دیتابیس را در پس‌زمینه اجرا می‌کند.

2. خاموش کردن دیتابیس:
   docker compose down
   دیتابیس را متوقف می‌کند.

3. نصب وابستگی‌ها:
   poetry install
   پکیج‌های پایتون را نصب می‌کند.

4. ساخت جداول:
   poetry run alembic upgrade head
   جداول دیتابیس را می‌سازد.

5. اجرای برنامه:
   poetry run todolist
   اجرای اصلی برنامه.

6. بستن تسک‌های منقضی‌شده:
   poetry run todolist tasks:autoclose-overdue
   تسک‌های overdue را می‌بندد.

7. اجرای خودکار در پس‌زمینه:
   poetry run todolist tasks:start-autoclose-scheduler
   بررسی و بستن خودکار تسک‌ها در زمان‌بندی مشخص.
