from app.models import PlacementDrive
from app.schemas.response.placement.placement_drive_response import (
    PlacementDriveResponse,
)
from app.schemas.response.placement.placement_drive_summary_response import (
    PlacementDriveSummaryResponse,
)
from app.schemas.response.student.student_drive_summary_response import (
    StudentDriveSummaryResponse,
)
from app.schemas.response.student.student_placement_drive_response import (
    StudentPlacementDriveResponse,
)


class PlacementDriveMapper:

    @staticmethod
    def to_response(
        drive: PlacementDrive,
    ) -> PlacementDriveResponse:
        return PlacementDriveResponse(
            id=drive.id,
            company_id=drive.company_id,
            title=drive.title,
            description=drive.description,
            job_location=drive.job_location,
            is_remote=drive.is_remote,
            salary_package=drive.salary_package,
            minimum_cgpa=drive.minimum_cgpa,
            eligible_branches=drive.eligible_branches,
            maximum_backlogs=drive.maximum_backlogs,
            experience_required=drive.experience_required,
            vacancies=drive.vacancies,
            application_deadline=drive.application_deadline,
            interview_date=drive.interview_date,
            job_type=drive.job_type,
            interview_mode=drive.interview_mode,
            status=drive.status,
            created_at=drive.created_at,
            updated_at=drive.updated_at,
        )

    @staticmethod
    def to_summary_response(
        drive: PlacementDrive,
    ) -> PlacementDriveSummaryResponse:
        return PlacementDriveSummaryResponse(
            id=drive.id,
            company_name=drive.company.company_name if drive.company else None,
            title=drive.title,
            job_location=drive.job_location,
            salary_package=drive.salary_package,
            job_type=drive.job_type,
            status=drive.status,
            application_deadline=drive.application_deadline,
            vacancies=drive.vacancies,
            created_at=drive.created_at,
        )

    @staticmethod
    def to_student_summary_response(
        drive: PlacementDrive,
    ) -> StudentDriveSummaryResponse:
        return StudentDriveSummaryResponse(
            id=drive.id,
            company_name=drive.company.company_name,
            title=drive.title,
            job_location=drive.job_location,
            is_remote=drive.is_remote,
            salary_package=drive.salary_package,
            job_type=drive.job_type,
            application_deadline=drive.application_deadline,
        )

    @staticmethod
    def to_student_response(
        drive: PlacementDrive,
    ) -> StudentPlacementDriveResponse:
        return StudentPlacementDriveResponse(
            id=drive.id,
            company_name=drive.company.company_name,
            title=drive.title,
            description=drive.description,
            job_location=drive.job_location,
            is_remote=drive.is_remote,
            salary_package=drive.salary_package,
            minimum_cgpa=drive.minimum_cgpa,
            eligible_branches=drive.eligible_branches,
            maximum_backlogs=drive.maximum_backlogs,
            experience_required=drive.experience_required,
            job_type=drive.job_type,
            interview_mode=drive.interview_mode,
            application_deadline=drive.application_deadline,
            interview_date=drive.interview_date,
            vacancies=drive.vacancies,
        )
