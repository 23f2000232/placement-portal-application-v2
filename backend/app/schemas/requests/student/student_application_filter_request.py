from pydantic import BaseModel, ConfigDict

from app.enums import ApplicationStatus


class StudentApplicationFilterRequest(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    status: ApplicationStatus | None = None