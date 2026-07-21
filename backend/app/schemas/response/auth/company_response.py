from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.enums import ApprovalStatus


class CompanyResponse(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    id: UUID
    email: str
    company_name: str
    website: str
    industry: str
    contact_person: str
    contact_email: str
    approval_status: ApprovalStatus