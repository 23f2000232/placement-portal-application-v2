from pydantic import BaseModel, ConfigDict

from app.enums import SortDirection, StudentSortField


class StudentSortRequest(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    sort_by: StudentSortField = StudentSortField.CREATED_AT
    sort_direction: SortDirection = SortDirection.DESC