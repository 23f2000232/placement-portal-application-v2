o off
title MAD 2 Project

echo Starting Redis CLI...
start "Redis CLI" cmd /k "wsl redis-cli"

echo Starting Celery Worker...
start "Celery Worker" cmd /k "cd /d %~dp0backend && uv run celery -A celery_worker.celery worker --loglevel=info --pool=solo"

echo Starting Celery Beat...
start "Celery Beat" cmd /k "cd /d %~dp0backend && uv run celery -A celery_worker.celery beat --loglevel=info"

echo Starting Flask Backend...
start "Flask Backend" cmd /k "cd /d %~dp0backend && uv run run.py"

echo Starting Vue Frontend...
start "Vue Frontend" cmd /k "cd /d %~dp0frontend\frontend && npm run dev"

echo.
echo All services have been started.
pause
