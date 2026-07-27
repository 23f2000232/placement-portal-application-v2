from pydantic import BaseModel, ConfigDict


class PlacementDriveSearchRequest(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    search: str | None = None