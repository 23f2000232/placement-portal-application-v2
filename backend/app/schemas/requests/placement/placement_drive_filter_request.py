from pydantic import BaseModel, ConfigDict

from app.enums import (
    JobType,
    PlacementDriveStatus,
)


class PlacementDriveFilterRequest(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    status: PlacementDriveStatus | None = None

    job_type: JobType | None = None

    is_remote: bool | None = None