from pydantic import BaseModel, ConfigDict

from app.enums import ApprovalStatus


class StudentFilterRequest(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    approval_status: ApprovalStatus | None = None
    branch: str | None = None
    semester: int | None = None