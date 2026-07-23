from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict

from app.enums import ApprovalStatus


class CompanySummaryResponse(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    id: UUID
    email: str
    company_name: str
    industry: str
    website: str
    approval_status: ApprovalStatus