from pydantic import BaseModel, ConfigDict

from app.enums import CompanySortField, SortDirection


class CompanySortRequest(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    sort_by: CompanySortField = CompanySortField.CREATED_AT
    sort_direction: SortDirection = SortDirection.DESC