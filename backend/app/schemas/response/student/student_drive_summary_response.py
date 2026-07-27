from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.enums import JobType


class StudentDriveSummaryResponse(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    id: UUID

    company_name: str

    title: str

    job_location: str

    is_remote: bool

    salary_package: Decimal

    job_type: JobType

    application_deadline: datetime