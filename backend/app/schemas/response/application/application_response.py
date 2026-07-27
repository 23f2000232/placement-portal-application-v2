from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.enums import ApplicationStatus


class ApplicationResponse(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    id: UUID

    drive_id: UUID

    status: ApplicationStatus

    applied_at: datetime