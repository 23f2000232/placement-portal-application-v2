import logging
from uuid import UUID

from app.enums import ApprovalStatus
from app.exceptions.admin import StudentNotFoundException
from app.exceptions.admin.student_already_approved_exception import (
    StudentAlreadyApprovedException,
)
from app.exceptions.admin.student_already_rejected_exception import (
    StudentAlreadyRejectedException,
)
from app.mappers.admin import StudentMapper
from app.repositories import (
    StudentRepository,
    CompanyRepository,
    UserRepository,
    PlacementDriveRepository,
    ApplicationRepository,
    PlacementRecordRepository,
)
from app.schemas.response.admin import StudentSummaryResponse


class AdminService:

    def __init__(
        self,
        student_repository: StudentRepository,
        company_repository: CompanyRepository,
        user_repository: UserRepository,
        placement_drive_repository: PlacementDriveRepository,
        application_repository: ApplicationRepository,
        placement_record_repository: PlacementRecordRepository,
    ):
        self.student_repository = student_repository
        self.company_repository = company_repository
        self.user_repository = user_repository
        self.placement_drive_repository = placement_drive_repository
        self.application_repository = application_repository
        self.placement_record_repository = placement_record_repository

        self.logger = logging.getLogger(__name__)

    def get_pending_students(
        self,
    ) -> list[StudentSummaryResponse]:
        self.logger.info("Fetching pending students")

        students = self.student_repository.get_by_approval_status(
            ApprovalStatus.PENDING,
        )

        self.logger.info(
            "Found %d pending students",
            len(students),
        )

        return [StudentMapper.to_summary_response(student) for student in students]

    def approve_student(
        self,
        student_id: UUID,
    ) -> StudentSummaryResponse:
        student = self.student_repository.get_by_id(student_id)
        if student is None:
            self.logger.warning(
                "Student %s not found",
                student_id,
            )
            raise StudentNotFoundException(student_id)
        if student.approval_status == ApprovalStatus.APPROVED:
            raise StudentAlreadyApprovedException(student_id)
        if student.approval_status == ApprovalStatus.REJECTED:
            raise StudentAlreadyRejectedException(student_id)

        self.logger.info(
            "Approving student %s",
            student.id,
        )
        student.approval_status = ApprovalStatus.APPROVED
        self.student_repository.save()
        self.logger.info(
            "Student %s approved successfully",
            student.id,
        )
        return StudentMapper.to_summary_response(student)

    def reject_student(
        self,
        student_id: UUID,
    ) -> StudentSummaryResponse:
        student = self.student_repository.get_by_id(student_id)
        if student is None:
            self.logger.warning(
                "Student %s not found",
                student_id,
            )
            raise StudentNotFoundException(student_id)

        if student.approval_status == ApprovalStatus.APPROVED:
            raise StudentAlreadyApprovedException(student_id)

        if student.approval_status == ApprovalStatus.REJECTED:
            raise StudentAlreadyRejectedException(student_id)

        self.logger.info(
            "Rejecting student %s",
            student_id,
        )
        student.approval_status = ApprovalStatus.REJECTED
        self.student_repository.save()
        return StudentMapper.to_summary_response(student)