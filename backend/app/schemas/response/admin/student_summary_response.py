from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.enums import AccountStatus, ApprovalStatus


class StudentSummaryResponse(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    id: UUID
    user_id: UUID
    email: str
    full_name: str
    roll_number: str
    branch: str
    semester: int
    cgpa: float
    approval_status: ApprovalStatus
    account_status: AccountStatus
