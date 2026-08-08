from app import create_app
from app.celery_app import celery
import app.tasks.placement_tasks  # Registers placement background jobs.

create_app()


if __name__ == "__main__":
    # `solo` is required on Windows: its prefork pool can fail with WinError 5.
    celery.worker_main(["worker", "--loglevel=info", "--pool=solo"])
