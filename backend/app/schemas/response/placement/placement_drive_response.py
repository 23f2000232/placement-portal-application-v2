from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.enums import (
    InterviewMode,
    JobType,
    PlacementDriveStatus,
)


class PlacementDriveResponse(BaseModel):
    model_config = ConfigDict(
        frozen=True,
    )

    id: UUID

    company_id: UUID

    title: str

    description: str

    job_location: str

    is_remote: bool

    salary_package: Decimal

    minimum_cgpa: Decimal

    eligible_branches: list[str]

    maximum_backlogs: int

    experience_required: int

    vacancies: int

    application_deadline: datetime

    interview_date: datetime | None

    job_type: JobType

    interview_mode: InterviewMode

    status: PlacementDriveStatus

    created_at: datetime

    updated_at: datetime