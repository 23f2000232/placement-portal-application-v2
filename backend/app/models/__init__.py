from app.models.application import Application
from app.models.base_model import BaseModel
from app.models.company import Company
from app.models.interview import Interview
from app.models.notification import Notification
from app.models.placement_drive import PlacementDrive
from app.models.placement_record import PlacementRecord
from app.models.student import Student
from app.models.user import User

__all__ = [
    "BaseModel",
    "User",
    "Application",
    "Company",
    "PlacementDrive",
    "Student",
    "Interview",
    "PlacementRecord",
    "Notification",
]