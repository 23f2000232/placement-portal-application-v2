from app.models import Application
from app.schemas.response.application.application_response import (
    ApplicationResponse,
)
from app.schemas.response.student.student_application_summary_response import (
    StudentApplicationSummaryResponse,
)


class ApplicationMapper:

    @staticmethod
    def to_response(
        application: Application,
    ) -> ApplicationResponse:
        return ApplicationResponse(
            id=application.id,
            drive_id=application.placement_drive_id,
            status=application.status,
            applied_at=application.created_at,
        )

    @staticmethod
    def to_student_summary_response(
        application: Application,
    ) -> StudentApplicationSummaryResponse:
        drive = application.placement_drive

        return StudentApplicationSummaryResponse(
            id=application.id,
            placement_drive_id=drive.id,
            company_name=drive.company.company_name,
            job_title=drive.title,
            job_location=drive.job_location,
            salary_package=drive.salary_package,
            application_status=application.status,
            applied_at=application.created_at,
        )