from app import create_app
from app.celery_app import celery
import app.tasks.placement_tasks  # Registers placement background jobs.

create_app()
