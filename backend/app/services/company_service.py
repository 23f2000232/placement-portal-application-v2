import logging
from pathlib import Path
from uuid import UUID

from app import Company, PlacementDrive
from app.enums import ApprovalStatus, ApplicationStatus
from app.exceptions.admin.company_not_found_exception import (
    CompanyNotFoundException,
)
from app.exceptions.application.application_not_found_exception import (
    ApplicationNotFoundException,
)
from app.exceptions.application.resume_not_found_exception import ResumeNotFoundException
from app.exceptions.application.invalid_application_status_transition_exception import (
    InvalidApplicationStatusTransitionException,
)
from app.exceptions.auth import AccountNotApprovedException
from app.exceptions.placement.placement_drive_access_denied_exception import (
    PlacementDriveAccessDeniedException,
)
from app.exceptions.placement.placement_drive_not_found_exception import (
    PlacementDriveNotFoundException,
)
from app.mappers.application_mapper import ApplicationMapper
from app.mappers.placement_drive_mapper import PlacementDriveMapper
from app.repositories import (
    ApplicationRepository,
    CompanyRepository,
    PlacementDriveRepository,
    InterviewRepository,
)
from app.schemas.common.pagination_request import PaginationRequest
from app.schemas.requests.company.company_application_filter_request import (
    CompanyApplicationFilterRequest,
)
from app.schemas.requests.company.company_application_search_request import (
    CompanyApplicationSearchRequest,
)
from app.schemas.requests.company.company_application_sort_request import (
    CompanyApplicationSortRequest,
)
from app.schemas.response.common.page_response import PageResponse
from app.schemas.response.company.company_application_response import (
    CompanyApplicationResponse,
)
from app.schemas.response.company.company_application_summary_response import (
    CompanyApplicationSummaryResponse,
)
from app.schemas.response.placement.placement_drive_response import (
    PlacementDriveResponse,
)
from app.utils.page_builder import build_page_response
from app.config import Config


class CompanyService:

    logger = logging.getLogger(__name__)

    def __init__(
        self,
        company_repository: CompanyRepository,
        placement_drive_repository: PlacementDriveRepository,
        application_repository: ApplicationRepository,
        interview_repository: InterviewRepository,
    ):
        self.company_repository = company_repository
        self.placement_drive_repository = placement_drive_repository
        self.application_repository = application_repository
        self.interview_repository = interview_repository

    def _get_approved_company(
        self,
        company_user_id: UUID,
    ) -> Company:
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

    def get_company_drive(
        self,
        user_id: UUID,
        drive_id: UUID,
    ) -> PlacementDriveResponse:
        drive = self.placement_drive_repository.get_by_id(
            drive_id,
        )
        company_id = self.company_repository.get_by_user_id(user_id).id

        if drive is None:
            raise PlacementDriveNotFoundException(
                drive_id,
            )

        if drive.company_id != company_id:
            raise PlacementDriveAccessDeniedException(
                drive_id,
            )

        return PlacementDriveMapper.to_response(drive)

    def _get_company_drive(
        self,
        company_id: UUID,
        drive_id: UUID,
    ) -> PlacementDrive:
        drive = self.placement_drive_repository.get_by_id(
            drive_id,
        )

        if drive is None:
            raise PlacementDriveNotFoundException(
                drive_id,
            )
        if drive.company_id != company_id:
            raise PlacementDriveAccessDeniedException(
                drive_id,
            )

        return drive

    def get_drive_applications(
        self,
        company_user_id: UUID,
        drive_id: UUID,
        pagination: PaginationRequest,
        filters: CompanyApplicationFilterRequest,
        sorting: CompanyApplicationSortRequest,
        search: CompanyApplicationSearchRequest,
    ) -> PageResponse[CompanyApplicationSummaryResponse]:

        self.logger.info(
            "Fetching applications for drive %s (page=%d, size=%d)",
            drive_id,
            pagination.page,
            pagination.size,
        )

        company = self._get_approved_company(
            company_user_id,
        )

        drive = self._get_company_drive(
            company.id,
            drive_id,
        )

        total_items = self.application_repository.count_company_drive_applications(
            company_id=company.id,
            drive_id=drive.id,
            filters=filters,
            search=search,
        )

        applications = self.application_repository.get_company_drive_applications_page(
            company_id=company.id,
            drive_id=drive.id,
            page=pagination.page,
            size=pagination.size,
            filters=filters,
            sorting=sorting,
            search=search,
        )

        self.logger.info(
            "Fetched %d of %d applications for drive %s",
            len(applications),
            total_items,
            drive.id,
        )

        return build_page_response(
            items=applications,
            mapper=ApplicationMapper.to_company_summary_response,
            page=pagination.page,
            size=pagination.size,
            total_items=total_items,
        )

    def get_application_resume_path(self, company_user_id: UUID, application_id: UUID) -> str:
        company = self._get_approved_company(company_user_id)
        application = self.application_repository.get_company_application(company.id, application_id)
        if application is None:
            raise ApplicationNotFoundException(application_id)
        stored_path = application.student.resume_path or application.resume_path
        resume_path = self._resolve_resume_path(stored_path)
        if resume_path is None:
            raise ResumeNotFoundException()
        return resume_path

    @staticmethod
    def _resolve_resume_path(stored_path: str | None) -> str | None:
        """Resolve both new absolute paths and legacy cwd-dependent resume paths."""
        if not stored_path:
            return None
        path = Path(stored_path)
        candidates = [path]
        if not path.is_absolute():
            candidates.append(Config.BASE_DIR / path)
        # Older records sometimes contain an absolute path rooted at backend/app.
        # The file itself is stored in backend/uploads/resumes, so recover by name.
        candidates.append(Path(Config.UPLOAD_DIRECTORY) / path.name)
        for candidate in candidates:
            if candidate.is_file():
                return str(candidate.resolve())
        return None

    def get_application(
        self,
        company_user_id: UUID,
        application_id: UUID,
    ) -> CompanyApplicationResponse:

        self.logger.info(
            "Fetching application %s",
            application_id,
        )

        company = self._get_approved_company(
            company_user_id,
        )

        application = self.application_repository.get_company_application(
            company_id=company.id,
            application_id=application_id,
        )

        if application is None:
            raise ApplicationNotFoundException(
                application_id,
            )

        self.logger.info(
            "Fetched application %s successfully",
            application.id,
        )

        return ApplicationMapper.to_company_response(
            application,
        )

    def _update_application_status(
        self,
        company_user_id: UUID,
        application_id: UUID,
        expected_status: ApplicationStatus,
        new_status: ApplicationStatus,
    ) -> CompanyApplicationResponse:
        company = self._get_approved_company(
            company_user_id,
        )

        application = self.application_repository.get_company_application(
            company_id=company.id,
            application_id=application_id,
        )

        if application is None:
            raise ApplicationNotFoundException(
                application_id,
            )

        if application.status != expected_status:
            raise InvalidApplicationStatusTransitionException(
                current_status=application.status,
                expected_status=expected_status,
            )

        try:
            application.status = new_status

            self.application_repository.save()

            self.logger.info(
                "Application %s moved from %s to %s",
                application.id,
                expected_status.value,
                new_status.value,
            )

            return ApplicationMapper.to_company_response(
                application,
            )

        except Exception:
            self.application_repository.rollback()

            self.logger.exception(
                "Failed to update application %s",
                application.id,
            )

            raise

    def mark_under_review(
        self,
        company_user_id: UUID,
        application_id: UUID,
    ) -> CompanyApplicationResponse:
        return self._update_application_status(
            company_user_id,
            application_id,
            ApplicationStatus.APPLIED,
            ApplicationStatus.UNDER_REVIEW,
        )

    def shortlist_application(
        self,
        company_user_id: UUID,
        application_id: UUID,
    ) -> CompanyApplicationResponse:
        return self._update_application_status(
            company_user_id,
            application_id,
            ApplicationStatus.UNDER_REVIEW,
            ApplicationStatus.SHORTLISTED,
        )

    def schedule_interview(
        self,
        company_user_id: UUID,
        application_id: UUID,
    ) -> CompanyApplicationResponse:
        return self._update_application_status(
            company_user_id,
            application_id,
            ApplicationStatus.SHORTLISTED,
            ApplicationStatus.INTERVIEW_SCHEDULED,
        )

    def select_application(
        self,
        company_user_id: UUID,
        application_id: UUID,
    ) -> CompanyApplicationResponse:
        application = self.application_repository.get_company_application(
            company_id=self._get_approved_company(company_user_id).id,
            application_id=application_id,
        )
        if application is None:
            raise ApplicationNotFoundException(application_id)
        latest_interview = self.interview_repository.get_latest_by_application(application.id)
        if latest_interview is None or latest_interview.status.value != "COMPLETED":
            raise InvalidApplicationStatusTransitionException(
                current_status=application.status,
                expected_status=ApplicationStatus.INTERVIEW_SCHEDULED,
            )
        return self._update_application_status(
            company_user_id,
            application_id,
            ApplicationStatus.INTERVIEW_SCHEDULED,
            ApplicationStatus.SELECTED,
        )

    def reject_application(
        self,
        company_user_id: UUID,
        application_id: UUID,
    ) -> CompanyApplicationResponse:
        company = self._get_approved_company(
            company_user_id,
        )

        application = self.application_repository.get_company_application(
            company_id=company.id,
            application_id=application_id,
        )

        if application is None:
            raise ApplicationNotFoundException(
                application_id,
            )

        allowed_statuses = {
            ApplicationStatus.APPLIED,
            ApplicationStatus.UNDER_REVIEW,
            ApplicationStatus.SHORTLISTED,
            ApplicationStatus.INTERVIEW_SCHEDULED,
        }

        if application.status not in allowed_statuses:
            raise InvalidApplicationStatusTransitionException(
                current_status=application.status,
                expected_status=ApplicationStatus.APPLIED,
            )

        try:
            application.status = ApplicationStatus.REJECTED

            self.application_repository.save()

            self.logger.info(
                "Application %s rejected successfully",
                application.id,
            )

            return ApplicationMapper.to_company_response(
                application,
            )

        except Exception:
            self.application_repository.rollback()

            self.logger.exception(
                "Failed to reject application %s",
                application.id,
            )

            raise
