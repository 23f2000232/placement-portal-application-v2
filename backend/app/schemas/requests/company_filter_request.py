from pydantic import BaseModel, ConfigDict

from app.enums import ApprovalStatus


class CompanyFilterRequest(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    approval_status: ApprovalStatus | None = None
    industry: str | None = None