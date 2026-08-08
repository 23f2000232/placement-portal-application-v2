import os

from celery import Celery
from celery.schedules import crontab


celery = Celery("placement_portal")


def init_celery(app) -> Celery:
    """Configure the shared Celery application from Flask configuration."""
    celery.conf.update(
        broker_url=app.config["CELERY_BROKER_URL"],
        result_backend=app.config["CELERY_RESULT_BACKEND"],
        timezone="Asia/Kolkata",
        task_serializer="json",
        result_serializer="json",
        accept_content=["json"],
        # Celery's prefork pool uses Windows synchronization primitives that
        # commonly fail with WinError 5. Run one in-process worker on Windows;
        # Linux/macOS deployments retain Celery's normal prefork default.
        worker_pool="solo" if os.name == "nt" else "prefork",
        worker_prefetch_multiplier=1,
        beat_schedule={
            "daily-deadline-reminders": {
                "task": "app.tasks.placement_tasks.send_deadline_reminders",
                "schedule": crontab(
                    hour=app.config["DAILY_REMINDER_HOUR"],
                    minute=app.config["DAILY_REMINDER_MINUTE"],
                ),
            },
            "monthly-placement-activity-report": {
                "task": "app.tasks.placement_tasks.send_monthly_activity_report",
                "schedule": crontab(
                    day_of_month=app.config["MONTHLY_REPORT_DAY"],
                    hour=app.config["MONTHLY_REPORT_HOUR"],
                    minute=app.config["MONTHLY_REPORT_MINUTE"],
                ),
            },
        },
    )

    if os.name == "nt":
        celery.conf.worker_concurrency = 1

    class FlaskTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = FlaskTask
    return celery
