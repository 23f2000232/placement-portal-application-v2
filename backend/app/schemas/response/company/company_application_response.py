from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.enums import ApplicationStatus


class CompanyApplicationResponse(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    id: UUID

    application_status: ApplicationStatus

    applied_at: datetime

    student_name: str

    email: str

    phone_number: str

    roll_number: str

    branch: str

    semester: int

    cgpa: Decimal

    current_backlogs: int

    resume_path: str | None

    placement_drive_id: UUID

    job_title: str

    job_location: str

    salary_package: Decimal