import logging
from uuid import UUID

from app.enums import ApprovalStatus
from app.exceptions.admin import StudentNotFoundException
from app.exceptions.admin.company_already_approved_exception import (
    CompanyAlreadyApprovedException,
)
from app.exceptions.admin.company_already_rejected_exception import (
    CompanyAlreadyRejectedException,
)
from app.exceptions.admin.company_not_found_exception import CompanyNotFoundException
from app.exceptions.admin.student_already_approved_exception import (
    StudentAlreadyApprovedException,
)
from app.exceptions.admin.student_already_rejected_exception import (
    StudentAlreadyRejectedException,
)
from app.mappers.admin import StudentMapper, CompanyMapper
from app.mappers.admin.user_mapper import UserMapper
from app.repositories import (
    StudentRepository,
    CompanyRepository,
    UserRepository,
    PlacementDriveRepository,
    ApplicationRepository,
    PlacementRecordRepository,
)
from app.schemas.common.pagination_request import PaginationRequest
from app.schemas.requests import sort_request
from app.schemas.requests.user_filter_request import UserFilterRequest
from app.schemas.response.admin import StudentSummaryResponse, CompanySummaryResponse
from app.schemas.response.admin.user_summary_response import UserSummaryResponse
from app.schemas.response.common.page_response import PageResponse
from app.utils.page_builder import build_page_response


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

    def get_pending_companies(
        self,
    ) -> list[CompanySummaryResponse]:
        self.logger.info("Fetching pending companies")

        companies = self.company_repository.get_by_approval_status(
            ApprovalStatus.PENDING,
        )

        self.logger.info(
            "Found %d pending companies",
            len(companies),
        )

        return [CompanyMapper.to_summary_response(company) for company in companies]

    def approve_company(
        self,
        company_id: UUID,
    ) -> CompanySummaryResponse:
        company = self.company_repository.get_by_id(company_id)

        if company is None:
            self.logger.warning(
                "Company %s not found",
                company_id,
            )
            raise CompanyNotFoundException(company_id)
        if company.approval_status == ApprovalStatus.APPROVED:
            raise CompanyAlreadyApprovedException(company_id)

        if company.approval_status == ApprovalStatus.REJECTED:
            raise CompanyAlreadyRejectedException(company_id)

        self.logger.info(
            "Approving company %s",
            company.id,
        )

        company.approval_status = ApprovalStatus.APPROVED
        self.company_repository.save()
        self.logger.info(
            "Company %s approved successfully",
            company.id,
        )
        return CompanyMapper.to_summary_response(company)

    def reject_company(
        self,
        company_id: UUID,
    ) -> CompanySummaryResponse:
        company = self.company_repository.get_by_id(company_id)

        if company is None:
            self.logger.warning(
                "Company %s not found",
                company_id,
            )
            raise CompanyNotFoundException(company_id)

        if company.approval_status == ApprovalStatus.APPROVED:
            raise CompanyAlreadyApprovedException(company_id)

        if company.approval_status == ApprovalStatus.REJECTED:
            raise CompanyAlreadyRejectedException(company_id)

        self.logger.info(
            "Rejecting company %s",
            company.id,
        )

        company.approval_status = ApprovalStatus.REJECTED

        self.company_repository.save()

        self.logger.info(
            "Company %s rejected successfully",
            company.id,
        )

        return CompanyMapper.to_summary_response(company)

    def get_users(
        self,
        pagination: PaginationRequest,
        filters: UserFilterRequest,
        sorting: sort_request.UserSortRequest,
    ) -> PageResponse[UserSummaryResponse]:
        self.logger.info(
            "Fetching users (page=%d, size=%d)",
            pagination.page,
            pagination.size,
        )

        total_items = self.user_repository.count(
            filters=filters,
        )

        users = self.user_repository.get_page(
            page=pagination.page,
            size=pagination.size,
            filters=filters,
            sorting=sorting,
        )

        self.logger.info(
            "Fetched %d of %d users (page=%d, size=%d)",
            len(users),
            total_items,
            pagination.page,
            pagination.size,
        )

        return build_page_response(
            items=users,
            mapper=UserMapper.to_summary_response,
            page=pagination.page,
            size=pagination.size,
            total_items=total_items,
        )