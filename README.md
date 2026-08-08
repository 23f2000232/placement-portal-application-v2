# Placement Portal

Copy `backend/.env.example` to `backend/.env` and replace every placeholder before running the application.

Background jobs require Redis and a Celery worker:

```powershell
cd backend
uv sync
uv run celery -A celery_worker.celery worker --loglevel=info --pool=solo
uv run celery -A celery_worker.celery beat --loglevel=info
```

The worker sends deadline reminders, creates monthly activity reports, and prepares student CSV exports. SMTP and Google Chat are optional; leave their variables unset to run without those integrations.
# placement-portal-application-v2
This is the second version of placement portal application of the MAD-II course.
