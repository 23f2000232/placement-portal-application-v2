from pydantic import BaseModel, ConfigDict

from app.enums import ApplicationStatus


class CompanyApplicationFilterRequest(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    status: ApplicationStatus | None = None