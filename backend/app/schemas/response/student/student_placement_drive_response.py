from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.enums import (
    InterviewMode,
    JobType,
)


class StudentPlacementDriveResponse(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    id: UUID

    company_name: str

    title: str

    description: str

    job_location: str

    is_remote: bool

    salary_package: Decimal

    minimum_cgpa: Decimal

    eligible_branches: list[str]

    maximum_backlogs: int

    experience_required: int

    job_type: JobType

    interview_mode: InterviewMode

    application_deadline: datetime

    interview_date: datetime | None

    vacancies: int