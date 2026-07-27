from pydantic import BaseModel, ConfigDict

from app.enums import (
    SortDirection,
    StudentApplicationSortField,
)


class StudentApplicationSortRequest(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    sort_by: StudentApplicationSortField = StudentApplicationSortField.APPLIED_AT

    sort_direction: SortDirection = SortDirection.DESC