from pydantic import BaseModel, ConfigDict

from app.enums import (
    CompanyApplicationSortField,
    SortDirection,
)


class CompanyApplicationSortRequest(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    sort_by: CompanyApplicationSortField = CompanyApplicationSortField.APPLIED_AT

    sort_direction: SortDirection = SortDirection.DESC