from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.enums import ApplicationStatus


class CompanyApplicationSummaryResponse(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    id: UUID

    student_name: str

    roll_number: str

    branch: str

    cgpa: Decimal

    application_status: ApplicationStatus

    applied_at: datetime