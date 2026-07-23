from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.enums import AccountStatus, UserRole


class UserSummaryResponse(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    id: UUID
    email: str
    role: UserRole
    account_status: AccountStatus
    is_active: bool