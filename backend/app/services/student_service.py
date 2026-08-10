import logging
from datetime import UTC, datetime
from uuid import UUID

from werkzeug.datastructures import FileStorage

from app import Student, Application
from app.enums import ApprovalStatus, ApplicationStatus, PlacementDriveStatus
from app.exceptions.admin import StudentNotFoundException
from app.exceptions.application.already_applied_exception import AlreadyAppliedException
from app.exceptions.application.application_not_found_exception import (
    ApplicationNotFoundException,
)
from app.exceptions.application.application_not_withdrawable_exception import (
    ApplicationNotWithdrawableException,
)
from app.exceptions.application.application_deadline_passed_exception import (
    ApplicationDeadlinePassedException,
)
from app.exceptions.application.invalid_resume_exception import InvalidResumeException
from app.exceptions.application.resume_not_found_exception import (
    ResumeNotFoundException,
)
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
from app.schemas.requests.student.student_application_filter_request import (
    StudentApplicationFilterRequest,
)
from app.schemas.requests.student.student_application_search_request import (
    StudentApplicationSearchRequest,
)
from app.schemas.requests.student.student_application_sort_request import (
    StudentApplicationSortRequest,
)
from app.schemas.requests.student.student_drive_filter_request import (
    StudentDriveFilterRequest,
)
from app.schemas.requests.student.student_drive_search_request import (
    StudentDriveSearchRequest,
)
from app.schemas.requests.student.student_drive_sort_request import (
    StudentDriveSortRequest,
)
from app.schemas.requests.student.update_student_profile_request import UpdateStudentProfileRequest
from app.mappers.auth.student_mapper import StudentMapper
from app.schemas.response.auth.student_response import StudentResponse
from app.schemas.response.application.application_response import ApplicationResponse
from app.schemas.response.common.page_response import PageResponse
from app.schemas.response.student.resume_response import ResumeResponse
from app.schemas.response.student.student_application_summary_response import (
    StudentApplicationSummaryResponse,
)
from app.schemas.response.student.student_drive_summary_response import (
    StudentDriveSummaryResponse,
)
from app.schemas.response.student.student_placement_drive_response import (
    StudentPlacementDriveResponse,
)
from app.services.storage.storage_service import StorageService
from app.utils.page_builder import build_page_response


class StudentService:

    def __init__(
        self,
        student_repository: StudentRepository,
        placement_drive_repository: PlacementDriveRepository,
        company_repository: CompanyRepository,
        application_repository: ApplicationRepository,
        storage_service: StorageService,
    ):
        self.storage_service = storage_service
        self.logger = logging.getLogger(__name__)
        self.student_repository = student_repository
        self.placement_drive_repository = placement_drive_repository
        self.company_repository = company_repository
        self.application_repository = application_repository

    def update_profile(self, student_user_id: UUID, request: UpdateStudentProfileRequest) -> StudentResponse:
        student = self._get_approved_student(student_user_id)
        student.full_name = request.full_name
        student.phone_number = request.phone_number
        student.branch = request.branch
        student.semester = request.semester
        student.cgpa = request.cgpa
        student.current_backlogs = request.current_backlogs
        student.skills = request.skills
        self.student_repository.save()
        return StudentMapper.to_response(student)

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

        # Enforce the deadline here as well as in the availability query. This
        # prevents direct API requests and race conditions from creating an
        # application after a deadline has elapsed.
        requested_drive = self.placement_drive_repository.get_by_id(drive_id)
        if requested_drive is not None and requested_drive.status == PlacementDriveStatus.OPEN:
            deadline = requested_drive.application_deadline
            if deadline.tzinfo is None:
                deadline = deadline.replace(tzinfo=UTC)
            if deadline <= datetime.now(UTC):
                requested_drive.status = PlacementDriveStatus.CLOSED
                self.placement_drive_repository.save()
                raise ApplicationDeadlinePassedException()

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

    def get_my_applications(
        self,
        student_user_id: UUID,
        pagination: PaginationRequest,
        filters: StudentApplicationFilterRequest,
        sorting: StudentApplicationSortRequest,
        search: StudentApplicationSearchRequest,
    ) -> PageResponse[StudentApplicationSummaryResponse]:
        self.logger.info(
            "Fetching student applications (page=%d, size=%d)",
            pagination.page,
            pagination.size,
        )

        student = self._get_approved_student(
            student_user_id,
        )

        total_items = self.application_repository.count_student_applications(
            student=student,
            filters=filters,
            search=search,
        )

        applications = self.application_repository.get_student_applications_page(
            student=student,
            page=pagination.page,
            size=pagination.size,
            filters=filters,
            sorting=sorting,
            search=search,
        )

        self.logger.info(
            "Fetched %d of %d applications",
            len(applications),
            total_items,
        )

        return build_page_response(
            items=applications,
            mapper=ApplicationMapper.to_student_summary_response,
            page=pagination.page,
            size=pagination.size,
            total_items=total_items,
        )

    def withdraw_application(
        self,
        student_user_id: UUID,
        application_id: UUID,
    ) -> None:
        self.logger.info(
            "Student %s withdrawing application %s",
            student_user_id,
            application_id,
        )

        student = self._get_approved_student(
            student_user_id,
        )

        application = self.application_repository.get_by_student_and_id(
            student.id,
            application_id,
        )

        if application is None:
            raise ApplicationNotFoundException(
                application_id,
            )

        if application.status not in (
            ApplicationStatus.APPLIED,
            ApplicationStatus.UNDER_REVIEW,
        ):
            raise ApplicationNotWithdrawableException()

        try:
            application.status = ApplicationStatus.WITHDRAWN

            self.application_repository.save()

            self.logger.info(
                "Application %s withdrawn successfully",
                application.id,
            )

        except Exception:
            self.application_repository.rollback()

            self.logger.exception(
                "Failed to withdraw application %s",
                application.id,
            )

            raise

    def upload_resume(
        self,
        student_user_id: UUID,
        file: FileStorage,
    ) -> ResumeResponse:
        self.logger.info(
            "Uploading resume for student %s",
            student_user_id,
        )

        student = self._get_approved_student(
            student_user_id,
        )

        if file is None or file.filename is None or file.filename == "":
            raise InvalidResumeException()

        if not file.filename.lower().endswith(".pdf"):
            raise InvalidResumeException()

        try:
            if student.resume_path is not None:
                self.storage_service.delete_resume(
                    student.resume_path,
                )

            resume_path = self.storage_service.upload_resume(
                student_id=str(student.id),
                file=file,
            )

            student.resume_path = resume_path

            self.student_repository.save()

            self.logger.info(
                "Resume uploaded successfully for student %s",
                student.id,
            )

            return ResumeResponse(
                resume_path=resume_path,
                uploaded_at=student.updated_at,
            )

        except Exception:
            self.student_repository.rollback()

            self.logger.exception(
                "Failed to upload resume for student %s",
                student.id,
            )

            raise

    def get_resume(
        self,
        student_user_id: UUID,
    ) -> ResumeResponse:

        self.logger.info(
            "Fetching resume for student %s",
            student_user_id,
        )

        student = self._get_approved_student(
            student_user_id,
        )

        if student.resume_path is None:
            raise ResumeNotFoundException()

        return ResumeResponse(
            resume_path=self.storage_service.get_resume_path(
                student.resume_path,
            ),
            uploaded_at=student.updated_at,
        )

    def delete_resume(
        self,
        student_user_id: UUID,
    ) -> None:

        self.logger.info(
            "Deleting resume for student %s",
            student_user_id,
        )

        student = self._get_approved_student(
            student_user_id,
        )

        if student.resume_path is None:
            raise ResumeNotFoundException()

        try:
            self.storage_service.delete_resume(
                student.resume_path,
            )

            student.resume_path = None

            self.student_repository.save()

            self.logger.info(
                "Resume deleted successfully for student %s",
                student.id,
            )

        except Exception:
            self.student_repository.rollback()

            self.logger.exception(
                "Failed to delete resume for student %s",
                student.id,
            )

            raise
