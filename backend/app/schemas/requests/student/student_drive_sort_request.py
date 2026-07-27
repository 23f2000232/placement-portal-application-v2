from pydantic import BaseModel, ConfigDict

from app.enums import (
    SortDirection,
    StudentDriveSortField,
)


class StudentDriveSortRequest(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    sort_by: StudentDriveSortField = StudentDriveSortField.APPLICATION_DEADLINE

    sort_direction: SortDirection = SortDirection.ASC