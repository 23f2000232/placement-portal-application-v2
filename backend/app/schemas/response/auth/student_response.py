from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.enums import ApprovalStatus, UserRole


class StudentResponse(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    id: UUID
    email: str
    full_name: str
    roll_number: str
    phone_number: str
    branch: str
    semester: int
    cgpa: float
    current_backlogs: int
    skills: list[str]
    approval_status: ApprovalStatus
    role: UserRole
