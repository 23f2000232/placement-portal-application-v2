from pydantic import BaseModel, ConfigDict

from app.enums import UserSortField, SortDirection


class UserSortRequest(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    sort_by: UserSortField = UserSortField.CREATED_AT
    sort_direction: SortDirection = SortDirection.DESC