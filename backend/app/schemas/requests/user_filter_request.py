from pydantic import BaseModel, ConfigDict

from app.enums.account_status import AccountStatus
from app.enums.user_role import UserRole


class UserFilterRequest(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    role: UserRole | None = None
    account_status: AccountStatus | None = None
    is_active: bool | None = None