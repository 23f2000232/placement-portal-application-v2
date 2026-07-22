from app.models import Company
from app.schemas.response.admin import CompanySummaryResponse


class CompanyMapper:

    @staticmethod
    def to_summary_response(
        company: Company,
    ) -> CompanySummaryResponse:
        return CompanySummaryResponse(
            id=company.id,
            email=company.user.email,
            company_name=company.company_name,
            industry=company.industry,
            website=company.website,
            approval_status=company.approval_status,
        )