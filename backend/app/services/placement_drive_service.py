import logging
from datetime import UTC, datetime
from uuid import UUID

from app.enums import ApprovalStatus, PlacementDriveStatus
from app.exceptions.admin.company_not_found_exception import (
    CompanyNotFoundException,
)
from app.exceptions.auth import AccountNotApprovedException
from app.exceptions.placement.invalid_application_deadline_exception import (
    InvalidApplicationDeadlineException,
)
from app.exceptions.placement.invalid_interview_date_exception import (
    InvalidInterviewDateException,
)
from app.exceptions.placement.placement_drive_access_denied_exception import (
    PlacementDriveAccessDeniedException,
)
from app.exceptions.placement.placement_drive_not_cancellable_exception import (
    PlacementDriveNotCancellableException,
)
from app.exceptions.placement.placement_drive_not_closable_exception import (
    PlacementDriveNotClosableException,
)
from app.exceptions.placement.placement_drive_not_deletable_exception import (
    PlacementDriveNotDeletableException,
)
from app.exceptions.placement.placement_drive_not_editable_exception import (
    PlacementDriveNotEditableException,
)
from app.exceptions.placement.placement_drive_not_found_exception import (
    PlacementDriveNotFoundException,
)
from app.mappers.placement_drive_mapper import PlacementDriveMapper
from app.models import PlacementDrive
from app.repositories import (
    CompanyRepository,
    PlacementDriveRepository,
)
from app.schemas.common.pagination_request import PaginationRequest
from app.schemas.requests.placement.create_placement_drive_request import (
    CreatePlacementDriveRequest,
)
from app.schemas.requests.placement.placement_drive_filter_request import (
    PlacementDriveFilterRequest,
)
from app.schemas.requests.placement.placement_drive_search_request import (
    PlacementDriveSearchRequest,
)
from app.schemas.requests.placement.placement_drive_sort_request import (
    PlacementDriveSortRequest,
)
from app.schemas.requests.placement.update_placement_drive_request import (
    UpdatePlacementDriveRequest,
)
from app.schemas.response.common.page_response import PageResponse
from app.schemas.response.placement.placement_drive_response import (
    PlacementDriveResponse,
)
from app.schemas.response.placement.placement_drive_summary_response import (
    PlacementDriveSummaryResponse,
)
from app.utils.page_builder import build_page_response


class PlacementDriveService:

    def __init__(
        self,
        placement_drive_repository: PlacementDriveRepository,
        company_repository: CompanyRepository,
    ):
        self.placement_drive_repository = placement_drive_repository
        self.company_repository = company_repository
        self.logger = logging.getLogger(__name__)

    def create_drive(
        self,
        company_user_id: UUID,
        request: CreatePlacementDriveRequest,
    ) -> PlacementDriveResponse:

        self.logger.info(
            "Creating placement drive '%s'",
            request.title,
        )

        company = self._get_approved_company(
            company_user_id,
        )

        self._validate_drive_dates(
            request.application_deadline,
            request.interview_date,
        )

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
            self.placement_drive_repository.create(
                drive,
            )
            self.placement_drive_repository.save()

            self.logger.info(
                "Placement drive '%s' created successfully",
                drive.title,
            )

            return PlacementDriveMapper.to_response(
                drive,
            )

        except Exception:
            self.placement_drive_repository.rollback()

            self.logger.exception(
                "Failed to create placement drive '%s'",
                request.title,
            )

            raise

    def update_drive(
        self,
        company_user_id: UUID,
        drive_id: UUID,
        request: UpdatePlacementDriveRequest,
    ) -> PlacementDriveResponse:

        self.logger.info(
            "Updating placement drive %s",
            drive_id,
        )

        company = self._get_approved_company(
            company_user_id,
        )

        drive = self._get_drive(
            drive_id,
        )

        self._validate_drive_ownership(
            company.id,
            drive,
        )

        if drive.status != PlacementDriveStatus.DRAFT:
            raise PlacementDriveNotEditableException(
                drive.id,
            )

        self._validate_drive_dates(
            request.application_deadline,
            request.interview_date,
        )

        drive.title = request.title
        drive.description = request.description
        drive.job_location = request.job_location
        drive.is_remote = request.is_remote
        drive.salary_package = request.salary_package
        drive.minimum_cgpa = request.minimum_cgpa
        drive.eligible_branches = request.eligible_branches
        drive.maximum_backlogs = request.maximum_backlogs
        drive.experience_required = request.experience_required
        drive.application_deadline = request.application_deadline
        drive.interview_date = request.interview_date
        drive.job_type = request.job_type
        drive.interview_mode = request.interview_mode
        drive.vacancies = request.vacancies

        try:
            self.placement_drive_repository.save()

            self.logger.info(
                "Placement drive %s updated successfully",
                drive.id,
            )

            return PlacementDriveMapper.to_response(
                drive,
            )

        except Exception:
            self.placement_drive_repository.rollback()

            self.logger.exception(
                "Failed to update placement drive %s",
                drive.id,
            )

            raise

    def _validate_drive_dates(
        self,
        application_deadline: datetime,
        interview_date: datetime | None,
    ) -> None:
        if application_deadline.tzinfo is None:
            application_deadline = application_deadline.replace(tzinfo=UTC)

        if interview_date is not None and interview_date.tzinfo is None:
            interview_date = interview_date.replace(tzinfo=UTC)

        now = datetime.now(UTC)

        if application_deadline <= now:
            raise InvalidApplicationDeadlineException()

        if interview_date is not None and interview_date < application_deadline:
            raise InvalidInterviewDateException()

    def _get_approved_company(
        self,
        company_user_id: UUID,
    ):
        company = self.company_repository.get_by_user_id(
            company_user_id,
        )

        if company is None:
            raise CompanyNotFoundException(
                company_user_id,
            )

        if company.approval_status != ApprovalStatus.APPROVED:
            raise AccountNotApprovedException()

        return company

    def _get_drive(
        self,
        drive_id: UUID,
    ) -> PlacementDrive:

        drive = self.placement_drive_repository.get_by_id(
            drive_id,
        )

        if drive is None:
            raise PlacementDriveNotFoundException(
                drive_id,
            )

        return drive

    def _validate_drive_ownership(
        self,
        company_id: UUID,
        drive: PlacementDrive,
    ) -> None:

        if drive.company_id != company_id:
            raise PlacementDriveAccessDeniedException(
                drive.id,
            )

    def open_drive(
        self,
        company_user_id: UUID,
        drive_id: UUID,
    ) -> PlacementDriveResponse:

        self.logger.info(
            "Opening placement drive %s",
            drive_id,
        )

        company = self._get_approved_company(
            company_user_id,
        )

        drive = self._get_drive(
            drive_id,
        )

        self._validate_drive_ownership(
            company.id,
            drive,
        )

        if drive.status != PlacementDriveStatus.DRAFT:
            raise PlacementDriveNotEditableException(
                drive.id,
            )

        # A company submits a completed draft; only an administrator can
        # approve it before it becomes visible to students.
        drive.status = PlacementDriveStatus.PENDING

        try:
            self.placement_drive_repository.save()

            self.logger.info(
                "Placement drive %s opened successfully",
                drive.id,
            )

            return PlacementDriveMapper.to_response(
                drive,
            )

        except Exception:
            self.placement_drive_repository.rollback()

            self.logger.exception(
                "Failed to open placement drive %s",
                drive.id,
            )

            raise

    def close_drive(
        self,
        company_user_id: UUID,
        drive_id: UUID,
    ) -> PlacementDriveResponse:

        self.logger.info(
            "Closing placement drive %s",
            drive_id,
        )

        company = self._get_approved_company(
            company_user_id,
        )

        drive = self._get_drive(
            drive_id,
        )

        self._validate_drive_ownership(
            company.id,
            drive,
        )

        if drive.status != PlacementDriveStatus.OPEN:
            raise PlacementDriveNotClosableException(
                drive.id,
            )

        drive.status = PlacementDriveStatus.CLOSED

        try:
            self.placement_drive_repository.save()

            self.logger.info(
                "Placement drive %s closed successfully",
                drive.id,
            )

            return PlacementDriveMapper.to_response(
                drive,
            )

        except Exception:
            self.placement_drive_repository.rollback()

            self.logger.exception(
                "Failed to close placement drive %s",
                drive.id,
            )

            raise

    def cancel_drive(
        self,
        company_user_id: UUID,
        drive_id: UUID,
    ) -> PlacementDriveResponse:

        self.logger.info(
            "Cancelling placement drive %s",
            drive_id,
        )

        company = self._get_approved_company(
            company_user_id,
        )

        drive = self._get_drive(
            drive_id,
        )

        self._validate_drive_ownership(
            company.id,
            drive,
        )

        if drive.status in (
            PlacementDriveStatus.CLOSED,
            PlacementDriveStatus.CANCELLED,
        ):
            raise PlacementDriveNotCancellableException(
                drive.id,
            )

        drive.status = PlacementDriveStatus.CANCELLED

        try:
            self.placement_drive_repository.save()

            self.logger.info(
                "Placement drive %s cancelled successfully",
                drive.id,
            )

            return PlacementDriveMapper.to_response(
                drive,
            )

        except Exception:
            self.placement_drive_repository.rollback()

            self.logger.exception(
                "Failed to cancel placement drive %s",
                drive.id,
            )

            raise

    def delete_drive(
        self,
        company_user_id: UUID,
        drive_id: UUID,
    ) -> None:

        self.logger.info(
            "Deleting placement drive %s",
            drive_id,
        )

        company = self._get_approved_company(
            company_user_id,
        )

        drive = self._get_drive(
            drive_id,
        )

        self._validate_drive_ownership(
            company.id,
            drive,
        )

        if drive.status != PlacementDriveStatus.DRAFT:
            raise PlacementDriveNotDeletableException(
                drive.id,
            )

        try:
            self.placement_drive_repository.delete(
                drive,
            )

            self.placement_drive_repository.save()

            self.logger.info(
                "Placement drive %s deleted successfully",
                drive.id,
            )

        except Exception:
            self.placement_drive_repository.rollback()

            self.logger.exception(
                "Failed to delete placement drive %s",
                drive.id,
            )

            raise

    def get_company_drives(
        self,
        company_user_id: UUID,
        pagination: PaginationRequest,
        filters: PlacementDriveFilterRequest,
        sorting: PlacementDriveSortRequest,
        search: PlacementDriveSearchRequest,
    ) -> PageResponse[PlacementDriveSummaryResponse]:
        self.logger.info(
            "Fetching placement drives (page=%d, size=%d)",
            pagination.page,
            pagination.size,
        )

        company = self._get_approved_company(
            company_user_id,
        )

        total_items = self.placement_drive_repository.count(
            company_id=company.id,
            filters=filters,
            search=search,
        )

        drives = self.placement_drive_repository.get_page(
            company_id=company.id,
            page=pagination.page,
            size=pagination.size,
            filters=filters,
            sorting=sorting,
            search=search,
        )

        self.logger.info(
            "Fetched %d of %d placement drives (page=%d, size=%d)",
            len(drives),
            total_items,
            pagination.page,
            pagination.size,
        )

        return build_page_response(
            items=drives,
            mapper=PlacementDriveMapper.to_summary_response,
            page=pagination.page,
            size=pagination.size,
            total_items=total_items,
        )
