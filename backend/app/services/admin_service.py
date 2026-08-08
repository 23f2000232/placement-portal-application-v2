import logging
from collections import Counter
from uuid import UUID

from app.enums import ApprovalStatus
from app.enums import AccountStatus, PlacementDriveStatus
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
from app.schemas.requests import (
    user_sort_request,
    user_search_request,
    StudentFilterRequest,
    StudentSortRequest,
    StudentSearchRequest,
)
from app.schemas.requests.company_filter_request import CompanyFilterRequest
from app.schemas.requests.company_search_request import CompanySearchRequest
from app.schemas.requests.company_sort_request import CompanySortRequest
from app.schemas.requests.user_filter_request import UserFilterRequest
from app.schemas.response.admin import StudentSummaryResponse, CompanySummaryResponse
from app.schemas.response.admin.user_summary_response import UserSummaryResponse
from app.schemas.response.common.page_response import PageResponse
from app.utils.page_builder import build_page_response
from app.mappers.placement_drive_mapper import PlacementDriveMapper
from app.schemas.requests.placement.placement_drive_filter_request import PlacementDriveFilterRequest
from app.schemas.requests.placement.placement_drive_search_request import PlacementDriveSearchRequest
from app.schemas.requests.placement.placement_drive_sort_request import PlacementDriveSortRequest
from app.schemas.response.placement.placement_drive_summary_response import PlacementDriveSummaryResponse


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
        sorting: user_sort_request.UserSortRequest,
        search: user_search_request.UserSearchRequest,
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
            search=search,
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

    def get_students(
        self,
        pagination: PaginationRequest,
        filters: StudentFilterRequest,
        sorting: StudentSortRequest,
        search: StudentSearchRequest,
    ) -> PageResponse[StudentSummaryResponse]:

        self.logger.info(
            "Fetching students (page=%d, size=%d)",
            pagination.page,
            pagination.size,
        )

        total_items = self.student_repository.count(
            filters=filters,
            search=search,
        )

        students = self.student_repository.get_page(
            page=pagination.page,
            size=pagination.size,
            filters=filters,
            sorting=sorting,
            search=search,
        )

        self.logger.info(
            "Fetched %d of %d students (page=%d, size=%d)",
            len(students),
            total_items,
            pagination.page,
            pagination.size,
        )

        return build_page_response(
            items=students,
            mapper=StudentMapper.to_summary_response,
            page=pagination.page,
            size=pagination.size,
            total_items=total_items,
        )

    def get_companies(
        self,
        pagination: PaginationRequest,
        filters: CompanyFilterRequest,
        sorting: CompanySortRequest,
        search: CompanySearchRequest,
    ) -> PageResponse[CompanySummaryResponse]:

        self.logger.info(
            "Fetching companies (page=%d, size=%d)",
            pagination.page,
            pagination.size,
        )

        total_items = self.company_repository.count(
            filters=filters,
            search=search,
        )

        companies = self.company_repository.get_page(
            page=pagination.page,
            size=pagination.size,
            filters=filters,
            sorting=sorting,
            search=search,
        )

        self.logger.info(
            "Fetched %d of %d companies (page=%d, size=%d)",
            len(companies),
            total_items,
            pagination.page,
            pagination.size,
        )

        return build_page_response(
            items=companies,
            mapper=CompanyMapper.to_summary_response,
            page=pagination.page,
            size=pagination.size,
            total_items=total_items,
        )

    def get_drives(
        self,
        pagination: PaginationRequest,
        filters: PlacementDriveFilterRequest,
        sorting: PlacementDriveSortRequest,
        search: PlacementDriveSearchRequest,
    ) -> PageResponse[PlacementDriveSummaryResponse]:
        total_items = self.placement_drive_repository.count_all(filters, search)
        drives = self.placement_drive_repository.get_all_page(
            page=pagination.page, size=pagination.size, filters=filters,
            sorting=sorting, search=search,
        )
        return build_page_response(
            items=drives,
            mapper=PlacementDriveMapper.to_summary_response,
            page=pagination.page,
            size=pagination.size,
            total_items=total_items,
        )

    def get_dashboard(self) -> dict:
        """Return the headline counts required on the admin dashboard."""
        drives = self.placement_drive_repository.get_all()
        users = self.user_repository.get_all()
        return {
            "students": len(self.student_repository.get_all()),
            "companies": len(self.company_repository.get_all()),
            "placement_drives": len(drives),
            "applications": self.application_repository.count(),
            "pending_companies": len(self.company_repository.get_by_approval_status(ApprovalStatus.PENDING)),
            "pending_drives": len(self.placement_drive_repository.get_by_status(PlacementDriveStatus.PENDING)),
            "drive_statuses": dict(Counter(drive.status.value for drive in drives)),
            "account_statuses": dict(Counter(user.account_status.value for user in users)),
        }

    def get_pending_drives(self):
        return self.placement_drive_repository.get_by_status(PlacementDriveStatus.PENDING)

    def approve_drive(self, drive_id: UUID):
        drive = self.placement_drive_repository.get_by_id(drive_id)
        if drive is None:
            from app.exceptions.placement.placement_drive_not_found_exception import PlacementDriveNotFoundException
            raise PlacementDriveNotFoundException(drive_id)
        if drive.status != PlacementDriveStatus.PENDING:
            from app.exceptions.common.bad_request_exception import BadRequestException
            raise BadRequestException("Only pending placement drives can be approved")
        drive.status = PlacementDriveStatus.OPEN
        self.placement_drive_repository.save()
        return drive

    def reject_drive(self, drive_id: UUID):
        drive = self.placement_drive_repository.get_by_id(drive_id)
        if drive is None:
            from app.exceptions.placement.placement_drive_not_found_exception import PlacementDriveNotFoundException
            raise PlacementDriveNotFoundException(drive_id)
        if drive.status != PlacementDriveStatus.PENDING:
            from app.exceptions.common.bad_request_exception import BadRequestException
            raise BadRequestException("Only pending placement drives can be rejected")
        drive.status = PlacementDriveStatus.REJECTED
        self.placement_drive_repository.save()
        return drive

    def close_drive(self, drive_id: UUID):
        drive = self.placement_drive_repository.get_by_id(drive_id)
        if drive is None:
            from app.exceptions.placement.placement_drive_not_found_exception import PlacementDriveNotFoundException
            raise PlacementDriveNotFoundException(drive_id)
        if drive.status != PlacementDriveStatus.OPEN:
            from app.exceptions.common.bad_request_exception import BadRequestException
            raise BadRequestException("Only open placement drives can be closed")
        drive.status = PlacementDriveStatus.CLOSED
        self.placement_drive_repository.save()
        return drive

    def cancel_drive(self, drive_id: UUID):
        drive = self.placement_drive_repository.get_by_id(drive_id)
        if drive is None:
            from app.exceptions.placement.placement_drive_not_found_exception import PlacementDriveNotFoundException
            raise PlacementDriveNotFoundException(drive_id)
        if drive.status in (PlacementDriveStatus.CLOSED, PlacementDriveStatus.CANCELLED):
            from app.exceptions.common.bad_request_exception import BadRequestException
            raise BadRequestException("Closed or cancelled placement drives cannot be cancelled")
        drive.status = PlacementDriveStatus.CANCELLED
        self.placement_drive_repository.save()
        return drive

    def set_user_account_status(self, user_id: UUID, status: AccountStatus) -> UserSummaryResponse:
        user = self.user_repository.get_by_id(user_id)
        if user is None:
            from app.exceptions.admin.user_not_found_exception import UserNotFoundException
            raise UserNotFoundException(user_id)
        user.account_status = status
        user.is_active = status == AccountStatus.ACTIVE
        self.user_repository.save()
        return UserMapper.to_summary_response(user)
