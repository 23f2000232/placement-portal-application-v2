from pydantic import BaseModel, ConfigDict

from app.enums import JobType


class StudentDriveFilterRequest(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    job_type: JobType | None = None

    is_remote: bool | None = None