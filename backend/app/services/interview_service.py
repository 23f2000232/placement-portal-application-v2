import logging
from uuid import UUID

from app import Interview, Student, Company
from app.enums import InterviewStatus, ApplicationStatus, ApprovalStatus
from app.exceptions.admin import StudentNotFoundException
from app.exceptions.admin.company_not_found_exception import CompanyNotFoundException
from app.exceptions.application.application_not_found_exception import (
    ApplicationNotFoundException,
)
from app.exceptions.auth import AccountNotApprovedException
from app.exceptions.interview.interview_already_completed_exception import (
    InterviewAlreadyCompletedException,
)
from app.exceptions.interview.interview_not_found_exception import (
    InterviewNotFoundException,
)
from app.exceptions.interview.interview_round_already_exists_exception import (
    InterviewRoundAlreadyExistsException,
)
from app.exceptions.placement.placement_drive_access_denied_exception import (
    PlacementDriveAccessDeniedException,
)
from app.mappers.interview_mapper import InterviewMapper
from app.repositories import (
    InterviewRepository,
    ApplicationRepository,
    PlacementDriveRepository,
    StudentRepository,
    CompanyRepository,
)
from app.schemas.requests.company.complete_interview_request import (
    CompleteInterviewRequest,
)
from app.schemas.requests.company.create_interview_request import CreateInterviewRequest
from app.schemas.requests.company.update_interview_request import UpdateInterviewRequest
from app.schemas.response.interview.interview_response import InterviewResponse


class InterviewService:

    logger = logging.getLogger(__name__)

    def __init__(
        self,
        interview_repository: InterviewRepository,
        application_repository: ApplicationRepository,
        placement_drive_repository: PlacementDriveRepository,
        student_repository: StudentRepository,
        company_repository: CompanyRepository,
    ):
        self.interview_repository = interview_repository
        self.application_repository = application_repository
        self.placement_drive_repository = placement_drive_repository
        self.student_repository = student_repository
        self.company_repository = company_repository

    def create_interview(
        self,
        company_user_id: UUID,
        application_id: UUID,
        request: CreateInterviewRequest,
    ) -> InterviewResponse:

        self.logger.info(
            "Creating interview round %d for application %s",
            request.round_number,
            application_id,
        )

        application = self.application_repository.get_by_id(
            application_id,
        )

        if application is None:
            raise ApplicationNotFoundException(
                application_id,
            )

        if application.placement_drive.company.user_id != company_user_id:
            raise PlacementDriveAccessDeniedException(
                application.placement_drive_id,
            )

        if application.status != ApplicationStatus.SHORTLISTED:
            raise InvalidApplicationStatusTransitionException(
                current_status=application.status,
                expected_status=ApplicationStatus.SHORTLISTED,
            )

        if self.interview_repository.exists_round(
            application.id,
            request.round_number,
        ):
            raise InterviewRoundAlreadyExistsException(
                application.id,
                request.round_number,
            )

        interview = Interview(
            application=application,
            round_number=request.round_number,
            interviewer_name=request.interviewer_name,
            interview_mode=request.interview_mode,
            meeting_link=request.meeting_link,
            location=request.location,
            scheduled_for=request.scheduled_for,
            status=InterviewStatus.SCHEDULED,
        )

        try:
            self.interview_repository.create(
                interview,
            )

            application.status = ApplicationStatus.INTERVIEW_SCHEDULED

            self.interview_repository.save()

            self.logger.info(
                "Interview created successfully for application %s",
                application.id,
            )

            return InterviewMapper.to_response(
                interview,
            )

        except Exception:
            self.interview_repository.rollback()

            self.logger.exception(
                "Failed to create interview for application %s",
                application.id,
            )

            raise

    def update_interview(
        self,
        company_user_id: UUID,
        interview_id: UUID,
        request: UpdateInterviewRequest,
    ) -> InterviewResponse:
        self.logger.info(
            "Updating interview %s",
            interview_id,
        )
        interview = self.interview_repository.get_by_id(
            interview_id,
        )
        if interview is None:
            raise InterviewNotFoundException(
                interview_id,
            )
        if interview.application.placement_drive.company.user_id != company_user_id:
            raise PlacementDriveAccessDeniedException(
                interview.application.placement_drive_id,
            )
        if interview.status != InterviewStatus.SCHEDULED:
            raise InterviewAlreadyCompletedException(
                interview.id,
            )
        changed = (
            interview.interviewer_name != request.interviewer_name
            or interview.interview_mode != request.interview_mode
            or interview.meeting_link != request.meeting_link
            or interview.location != request.location
            or interview.scheduled_for != request.scheduled_for
        )

        if not changed:
            return InterviewMapper.to_response(interview)

        interview.interviewer_name = request.interviewer_name

        interview.interview_mode = request.interview_mode

        interview.meeting_link = request.meeting_link

        interview.location = request.location

        interview.scheduled_for = request.scheduled_for

        try:
            self.interview_repository.save()

            self.logger.info(
                "Interview %s updated successfully",
                interview.id,
            )

            return InterviewMapper.to_response(
                interview,
            )

        except Exception:
            self.interview_repository.rollback()

            self.logger.exception(
                "Failed to update interview %s",
                interview.id,
            )

            raise

    def complete_interview(
        self,
        company_user_id: UUID,
        interview_id: UUID,
        request: CompleteInterviewRequest,
    ) -> InterviewResponse:
        self.logger.info(
            "Completing interview %s",
            interview_id,
        )
        interview = self.interview_repository.get_by_id(
            interview_id,
        )

        if interview is None:
            raise InterviewNotFoundException(
                interview_id,
            )
        if interview.application.placement_drive.company.user_id != company_user_id:
            raise PlacementDriveAccessDeniedException(
                interview.application.placement_drive_id,
            )
        if interview.status != InterviewStatus.SCHEDULED:
            raise InterviewAlreadyCompletedException(
                interview.id,
            )
        interview.status = request.status

        interview.feedback = request.remarks
        try:
            self.interview_repository.save()

            self.logger.info(
                "Interview %s marked as %s",
                interview.id,
                interview.status.value,
            )

            return InterviewMapper.to_response(
                interview,
            )

        except Exception:
            self.interview_repository.rollback()

            self.logger.exception(
                "Failed to complete interview %s",
                interview.id,
            )

            raise

    def get_interview(
        self,
        company_user_id: UUID,
        interview_id: UUID,
    ) -> InterviewResponse:

        self.logger.info(
            "Fetching interview %s",
            interview_id,
        )

        interview = self.interview_repository.get_by_id(
            interview_id,
        )

        if interview is None:
            raise InterviewNotFoundException(
                interview_id,
            )

        if interview.application.placement_drive.company.user_id != company_user_id:
            raise PlacementDriveAccessDeniedException(
                interview.application.placement_drive_id,
            )

        return InterviewMapper.to_response(
            interview,
        )

    def get_application_interviews(
        self,
        company_user_id: UUID,
        application_id: UUID,
    ) -> list[InterviewResponse]:

        self.logger.info(
            "Fetching interviews for application %s",
            application_id,
        )

        application = self.application_repository.get_by_id(
            application_id,
        )

        if application is None:
            raise ApplicationNotFoundException(
                application_id,
            )

        if application.placement_drive.company.user_id != company_user_id:
            raise PlacementDriveAccessDeniedException(
                application.placement_drive_id,
            )

        interviews = self.interview_repository.get_by_application_id(
            application.id,
        )

        return [
            InterviewMapper.to_response(
                interview,
            )
            for interview in interviews
        ]

    def get_student_upcoming_interviews(
        self,
        student_user_id: UUID,
    ) -> list[InterviewResponse]:

        self.logger.info(
            "Fetching upcoming interviews for student %s",
            student_user_id,
        )

        student = self._get_approved_student(
            student_user_id,
        )

        interviews = self.interview_repository.get_student_interviews(
            student.id,
        )

        return [
            InterviewMapper.to_response(
                interview,
            )
            for interview in interviews
        ]

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

    def get_company_upcoming_interviews(
        self,
        company_user_id: UUID,
    ) -> list[InterviewResponse]:

        self.logger.info(
            "Fetching upcoming interviews for company %s",
            company_user_id,
        )

        company = self._get_approved_company(
            company_user_id,
        )

        interviews = self.interview_repository.get_company_interviews(
            company.id,
        )

        return [
            InterviewMapper.to_response(
                interview,
            )
            for interview in interviews
        ]

    def get_all_interviews(self) -> list[InterviewResponse]:
        return [
            InterviewMapper.to_response(interview)
            for interview in self.interview_repository.get_all_ordered()
        ]

    def update_interview_as_admin(
        self, interview_id: UUID, request: UpdateInterviewRequest
    ) -> InterviewResponse:
        interview = self.interview_repository.get_by_id(interview_id)
        if interview is None:
            raise InterviewNotFoundException(interview_id)
        if interview.status != InterviewStatus.SCHEDULED:
            raise InterviewAlreadyCompletedException(interview.id)
        interview.interviewer_name = request.interviewer_name
        interview.interview_mode = request.interview_mode
        interview.meeting_link = request.meeting_link
        interview.location = request.location
        interview.scheduled_for = request.scheduled_for
        try:
            self.interview_repository.save()
            return InterviewMapper.to_response(interview)
        except Exception:
            self.interview_repository.rollback()
            raise

    def complete_interview_as_admin(
        self, interview_id: UUID, request: CompleteInterviewRequest
    ) -> InterviewResponse:
        interview = self.interview_repository.get_by_id(interview_id)
        if interview is None:
            raise InterviewNotFoundException(interview_id)
        if interview.status != InterviewStatus.SCHEDULED:
            raise InterviewAlreadyCompletedException(interview.id)
        interview.status = request.status
        interview.feedback = request.remarks
        try:
            self.interview_repository.save()
            return InterviewMapper.to_response(interview)
        except Exception:
            self.interview_repository.rollback()
            raise

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
