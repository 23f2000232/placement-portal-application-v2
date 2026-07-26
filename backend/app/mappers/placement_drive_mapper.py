from app.schemas.response.placement_drive import PlacementDriveResponse

from app.models import PlacementDrive


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