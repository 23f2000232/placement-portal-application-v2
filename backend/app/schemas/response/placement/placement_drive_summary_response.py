from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.enums import (
    JobType,
    PlacementDriveStatus,
)


class PlacementDriveSummaryResponse(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    id: UUID

    title: str

    job_location: str

    salary_package: Decimal

    job_type: JobType

    status: PlacementDriveStatus

    application_deadline: datetime

    vacancies: int

    created_at: datetime