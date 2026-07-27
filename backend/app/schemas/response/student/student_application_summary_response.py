from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.enums import ApplicationStatus


class StudentApplicationSummaryResponse(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    id: UUID

    placement_drive_id: UUID

    company_name: str

    job_title: str

    job_location: str

    salary_package: Decimal

    application_status: ApplicationStatus

    applied_at: datetime