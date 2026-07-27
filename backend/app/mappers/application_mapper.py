from app.models import Application
from app.schemas.response.application.application_response import (
    ApplicationResponse,
)
from app.schemas.response.company.company_application_response import (
    CompanyApplicationResponse,
)
from app.schemas.response.company.company_application_summary_response import (
    CompanyApplicationSummaryResponse,
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

    @staticmethod
    def to_company_summary_response(
        application: Application,
    ) -> CompanyApplicationSummaryResponse:
        student = application.student

        return CompanyApplicationSummaryResponse(
            id=application.id,
            student_name=student.full_name,
            roll_number=student.roll_number,
            branch=student.branch,
            cgpa=student.cgpa,
            application_status=application.status,
            applied_at=application.created_at,
        )

    @staticmethod
    def to_company_response(
        application: Application,
    ) -> CompanyApplicationResponse:
        student = application.student
        user = student.user
        drive = application.placement_drive

        return CompanyApplicationResponse(
            id=application.id,
            application_status=application.status,
            applied_at=application.created_at,
            student_name=student.full_name,
            email=user.email,
            phone_number=student.phone_number,
            roll_number=student.roll_number,
            branch=student.branch,
            semester=student.semester,
            cgpa=student.cgpa,
            current_backlogs=student.current_backlogs,
            resume_path=student.resume_path,
            placement_drive_id=drive.id,
            job_title=drive.title,
            job_location=drive.job_location,
            salary_package=drive.salary_package,
        )