from app.enums import UserRole
from app.models.company import Company
from app.schemas.response.auth.company_response import CompanyResponse


class CompanyMapper:

    @staticmethod
    def to_response(company: Company) -> CompanyResponse:
        return CompanyResponse(
            id=company.id,
            email=company.user.email,
            company_name=company.company_name,
            website=company.website,
            industry=company.industry,
            contact_person=company.contact_person,
            contact_email=company.contact_email,
            approval_status=company.approval_status,
            role=UserRole.COMPANY,
        )