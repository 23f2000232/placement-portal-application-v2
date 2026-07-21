from app.repositories.application_repository import ApplicationRepository
from app.repositories.base_repository import BaseRepository
from app.repositories.company_repository import CompanyRepository
from app.repositories.interview_repository import InterviewRepository
from app.repositories.notification_repository import NotificationRepository
from app.repositories.placement_drive_repository import PlacementDriveRepository
from app.repositories.placement_record_repository import PlacementRecordRepository
from app.repositories.student_repository import StudentRepository
from app.repositories.user_repository import UserRepository

__all__ = [
    "ApplicationRepository",
    "UserRepository",
    "BaseRepository",
    "CompanyRepository",
    "InterviewRepository",
    "NotificationRepository",
    "PlacementDriveRepository",
    "PlacementRecordRepository",
    "StudentRepository",
]