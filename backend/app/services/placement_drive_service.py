import logging
from datetime import UTC, datetime
from uuid import UUID

from app.enums import ApprovalStatus
from app.exceptions.admin.company_not_found_exception import (
    CompanyNotFoundException,
)
from app.exceptions.auth import AccountNotApprovedException
from app.exceptions.placement.InvalidApplicationDeadlineException import (
    InvalidApplicationDeadlineException,
)
from app.exceptions.placement.invalid_interview_date_exception import (
    InvalidInterviewDateException,
)
from app.mappers.placement_drive_mapper import PlacementDriveMapper
from app.models import PlacementDrive
from app.repositories import (
    CompanyRepository,
    PlacementDriveRepository,
)
from app.schemas.requests.create_placement_drive_request import (
    CreatePlacementDriveRequest,
)
from app.schemas.response.placement_drive_response import (
    PlacementDriveResponse,
)

logger = logging.getLogger(__name__)


class PlacementDriveService:

    def __init__(
        self,
        placement_drive_repository: PlacementDriveRepository,
        company_repository: CompanyRepository,
    ):
        self.placement_drive_repository = placement_drive_repository
        self.company_repository = company_repository

    def create_drive(
        self,
        company_user_id: UUID,
        request: CreatePlacementDriveRequest,
    ) -> PlacementDriveResponse:

        logger.info(
            "Creating placement drive '%s'",
            request.title,
        )

        company = self.company_repository.get_by_user_id(
            company_user_id,
        )

        if company is None:
            raise CompanyNotFoundException(company_user_id)

        if company.approval_status != ApprovalStatus.APPROVED:
            raise AccountNotApprovedException()

        now = datetime.now(UTC)

        if request.application_deadline <= now:
            raise InvalidApplicationDeadlineException()

        if (
            request.interview_date is not None
            and request.interview_date < request.application_deadline
        ):
            raise InvalidInterviewDateException()

        drive = PlacementDrive(
            title=request.title,
            description=request.description,
            job_location=request.job_location,
            is_remote=request.is_remote,
            salary_package=request.salary_package,
            minimum_cgpa=request.minimum_cgpa,
            eligible_branches=request.eligible_branches,
            maximum_backlogs=request.maximum_backlogs,
            experience_required=request.experience_required,
            application_deadline=request.application_deadline,
            interview_date=request.interview_date,
            vacancies=request.vacancies,
            job_type=request.job_type,
            interview_mode=request.interview_mode,
        )

        drive.company = company

        try:
            self.placement_drive_repository.create(drive)
            self.placement_drive_repository.save()

            logger.info(
                "Placement drive '%s' created successfully",
                drive.title,
            )

            return PlacementDriveMapper.to_response(drive)

        except Exception:
            self.placement_drive_repository.rollback()

            logger.exception(
                "Failed to create placement drive '%s'",
                request.title,
            )

            raise