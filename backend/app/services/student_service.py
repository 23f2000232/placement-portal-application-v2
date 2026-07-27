import logging
from uuid import UUID

from app import Student, Application
from app.enums import ApprovalStatus
from app.exceptions.admin import StudentNotFoundException
from app.exceptions.application.already_applied_exception import AlreadyAppliedException
from app.exceptions.application.resume_not_uploaded_exception import (
    ResumeNotUploadedException,
)
from app.exceptions.auth import AccountNotApprovedException
from app.exceptions.placement.placement_drive_not_found_exception import (
    PlacementDriveNotFoundException,
)
from app.mappers.application_mapper import ApplicationMapper
from app.mappers.placement_drive_mapper import PlacementDriveMapper
from app.repositories import (
    PlacementDriveRepository,
    CompanyRepository,
    StudentRepository,
    ApplicationRepository,
)
from app.schemas.common.pagination_request import PaginationRequest
from app.schemas.requests.student.student_drive_filter_request import (
    StudentDriveFilterRequest,
)
from app.schemas.requests.student.student_drive_search_request import (
    StudentDriveSearchRequest,
)
from app.schemas.requests.student.student_drive_sort_request import (
    StudentDriveSortRequest,
)
from app.schemas.response.application.application_response import ApplicationResponse
from app.schemas.response.common.page_response import PageResponse
from app.schemas.response.student.student_drive_summary_response import (
    StudentDriveSummaryResponse,
)
from app.schemas.response.student.student_placement_drive_response import (
    StudentPlacementDriveResponse,
)
from app.utils.page_builder import build_page_response


class StudentService:

    def __init__(
        self,
        student_repository: StudentRepository,
        placement_drive_repository: PlacementDriveRepository,
        company_repository: CompanyRepository,
        application_repository: ApplicationRepository,
    ):
        self.logger = logging.getLogger(__name__)
        self.student_repository = student_repository
        self.placement_drive_repository = placement_drive_repository
        self.company_repository = company_repository
        self.application_repository = application_repository

    def _get_approved_student(
        self,
        student_user_id: UUID,
    ) -> Student:
        student = self.student_repository.get_by_user_id(
            student_user_id,
        )

        if student is None:
            raise StudentNotFoundException(student_user_id)

        if student.approval_status != ApprovalStatus.APPROVED:
            raise AccountNotApprovedException()

        return student

    def get_available_drives(
        self,
        student_user_id: UUID,
        pagination: PaginationRequest,
        filters: StudentDriveFilterRequest,
        sorting: StudentDriveSortRequest,
        search: StudentDriveSearchRequest,
    ) -> PageResponse[StudentDriveSummaryResponse]:
        self.logger.info(
            "Fetching available drives (page=%d, size=%d)",
            pagination.page,
            pagination.size,
        )

        student = self._get_approved_student(
            student_user_id,
        )

        total_items = self.placement_drive_repository.count_available_drives(
            student=student,
            filters=filters,
            search=search,
        )

        drives = self.placement_drive_repository.get_available_drives_page(
            student=student,
            page=pagination.page,
            size=pagination.size,
            filters=filters,
            sorting=sorting,
            search=search,
        )

        self.logger.info(
            "Fetched %d of %d available drives",
            len(drives),
            total_items,
        )

        return build_page_response(
            items=drives,
            mapper=PlacementDriveMapper.to_student_summary_response,
            page=pagination.page,
            size=pagination.size,
            total_items=total_items,
        )

    def get_available_drive(
        self,
        student_user_id: UUID,
        drive_id: UUID,
    ) -> StudentPlacementDriveResponse:
        self.logger.info(
            "Fetching placement drive %s",
            drive_id,
        )

        student = self._get_approved_student(
            student_user_id,
        )

        drive = self.placement_drive_repository.get_available_drive(
            student=student,
            drive_id=drive_id,
        )

        if drive is None:
            raise PlacementDriveNotFoundException(
                drive_id,
            )

        return PlacementDriveMapper.to_student_response(
            drive,
        )

    def apply_to_drive(
        self,
        student_user_id: UUID,
        drive_id: UUID,
    ) -> ApplicationResponse:
        self.logger.info(
            "Student %s applying to drive %s",
            student_user_id,
            drive_id,
        )

        student = self._get_approved_student(
            student_user_id,
        )

        if not student.resume_path:
            raise ResumeNotUploadedException()

        drive = self.placement_drive_repository.get_drive_for_application(
            student=student,
            drive_id=drive_id,
        )

        if drive is None:
            raise PlacementDriveNotFoundException(
                drive_id,
            )

        if self.application_repository.exists_by_student_and_drive(
            student.id,
            drive.id,
        ):
            raise AlreadyAppliedException()

        application = Application(
            student=student,
            placement_drive=drive,
        )

        try:
            self.application_repository.create(
                application,
            )

            self.application_repository.save()

            self.logger.info(
                "Student %s successfully applied to drive %s",
                student.id,
                drive.id,
            )

            return ApplicationMapper.to_response(
                application,
            )

        except Exception:
            self.application_repository.rollback()

            self.logger.exception(
                "Failed to apply student %s to drive %s",
                student.id,
                drive.id,
            )

            raise