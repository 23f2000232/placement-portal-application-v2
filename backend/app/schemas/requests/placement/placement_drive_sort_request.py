from pydantic import BaseModel, ConfigDict

from app.enums import (
    PlacementDriveSortField,
    SortDirection,
)


class PlacementDriveSortRequest(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    sort_by: PlacementDriveSortField = PlacementDriveSortField.CREATED_AT

    sort_direction: SortDirection = SortDirection.DESC