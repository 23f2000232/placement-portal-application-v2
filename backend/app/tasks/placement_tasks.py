import csv
import smtplib
import json
from uuid import UUID
from urllib.request import Request, urlopen
from datetime import UTC, datetime, timedelta
from email.message import EmailMessage

from app.celery_app import celery
from app.config import Config
from app.enums import ApplicationStatus, NotificationType, PlacementDriveStatus
from app.extensions import db
from app.models import Application, Notification, PlacementDrive, Student, User


@celery.task(name="app.tasks.placement_tasks.close_expired_placement_drives")
def close_expired_placement_drives():
    """Close open drives whose application deadline has elapsed."""
    closed = PlacementDrive.query.filter(
        PlacementDrive.status == PlacementDriveStatus.OPEN,
        PlacementDrive.application_deadline <= datetime.now(UTC),
    ).update({PlacementDrive.status: PlacementDriveStatus.CLOSED}, synchronize_session=False)
    db.session.commit()
    return {"drives_closed": closed}


def _send_email(recipient: str, subject: str, html: str) -> bool:
    """Send email only when SMTP credentials have been configured."""
    if not all((Config.SMTP_HOST, Config.SMTP_USERNAME, Config.SMTP_PASSWORD, Config.SMTP_FROM_EMAIL)):
        return False
    message = EmailMessage()
    message["From"] = Config.SMTP_FROM_EMAIL
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(html, subtype="html")
    with smtplib.SMTP(Config.SMTP_HOST, Config.SMTP_PORT) as client:
        client.starttls()
        client.login(Config.SMTP_USERNAME, Config.SMTP_PASSWORD)
        client.send_message(message)
    return True


def _send_google_chat_message(text: str) -> bool:
    if not Config.GOOGLE_CHAT_WEBHOOK_URL:
        return False
    request = Request(
        Config.GOOGLE_CHAT_WEBHOOK_URL,
        data=json.dumps({"text": text}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=10):
        pass
    return True


@celery.task(name="app.tasks.placement_tasks.send_deadline_reminders")
def send_deadline_reminders():
    deadline = datetime.now(UTC) + timedelta(days=1)
    drives = PlacementDrive.query.filter(
        PlacementDrive.status == PlacementDriveStatus.OPEN,
        PlacementDrive.application_deadline <= deadline,
        PlacementDrive.application_deadline > datetime.now(UTC),
    ).all()
    recipients = Student.query.join(User).filter(User.is_active.is_(True)).all()
    for student in recipients:
        titles = [drive.title for drive in drives if drive.eligible_branches and student.branch in drive.eligible_branches]
        if titles:
            _send_email(student.user.email, "Placement application deadline reminder", "<p>Upcoming deadlines: " + ", ".join(titles) + "</p>")
    if drives:
        _send_google_chat_message("Placement deadline reminder: " + ", ".join(drive.title for drive in drives))
    return {"drives": len(drives), "students_checked": len(recipients)}


@celery.task(name="app.tasks.placement_tasks.send_monthly_activity_report")
def send_monthly_activity_report():
    now = datetime.now(UTC)
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    previous_month = (month_start - timedelta(days=1)).replace(day=1)
    drives = PlacementDrive.query.filter(PlacementDrive.created_at >= previous_month, PlacementDrive.created_at < month_start).count()
    applied = Application.query.filter(Application.created_at >= previous_month, Application.created_at < month_start).count()
    selected = Application.query.filter(Application.status == ApplicationStatus.SELECTED, Application.status_updated_at >= previous_month, Application.status_updated_at < month_start).count()
    html = f"<h1>Monthly Placement Activity Report</h1><ul><li>Drives conducted: {drives}</li><li>Students applied: {applied}</li><li>Students selected: {selected}</li></ul>"
    _send_email(Config.ADMIN_EMAIL, "Monthly Placement Activity Report", html)
    return {"drives": drives, "applied": applied, "selected": selected}


@celery.task(name="app.tasks.placement_tasks.export_student_applications")
def export_student_applications(student_user_id: str, task_id: str):
    # Celery JSON serialization turns UUIDs into strings; SQLAlchemy's UUID
    # columns require the value to be restored before filtering.
    student = Student.query.filter_by(user_id=UUID(student_user_id)).first()
    if student is None:
        raise ValueError("Student no longer exists")
    Config.EXPORT_DIRECTORY.mkdir(parents=True, exist_ok=True)
    filename = f"{student.id}_{task_id}.csv"
    destination = Config.EXPORT_DIRECTORY / filename
    with destination.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["Student ID", "Company Name", "Drive Title", "Application Status", "Application Date"])
        for application in Application.query.filter_by(student_id=student.id).all():
            writer.writerow([student.id, application.placement_drive.company.company_name, application.placement_drive.title, application.status.value, application.created_at.isoformat()])
    db.session.add(Notification(user_id=student.user_id, title="Application history export ready", message="Your CSV export is ready to download.", notification_type=NotificationType.SYSTEM))
    db.session.commit()
    _send_email(student.user.email, "Placement history export ready", "<p>Your placement application history export is ready.</p>")
    return {"filename": filename}
