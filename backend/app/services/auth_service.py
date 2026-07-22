import logging
from uuid import UUID

from app.enums import UserRole, ApprovalStatus, AccountStatus
from app.exceptions.auth import (
    EmailAlreadyExistsException,
    InvalidCredentialsException,
    AccountDisabledException,
    AccountNotApprovedException,
    AccountBlacklistedException,
)
from app.mappers.auth import StudentMapper, CompanyMapper
from app.models import Student, User, Company
from app.repositories import StudentRepository, CompanyRepository, UserRepository
from app.schemas.auth import (
    StudentRegistrationRequest,
    CompanyRegistrationRequest,
    LoginRequest,
)
from app.schemas.response.auth import StudentResponse, CompanyResponse, LoginResponse
from app.utils import create_access_token_for_user

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(
        self,
        user_repository: UserRepository,
        student_repository: StudentRepository,
        company_repository: CompanyRepository,
    ):
        self.user_repository = user_repository
        self.student_repository = student_repository
        self.company_repository = company_repository

    def register_student(
        self,
        request: StudentRegistrationRequest,
    ) -> StudentResponse:
        if self.user_repository.exists_by_email(request.email):
            logger.warning(
                "Student registration attempted with existing email=%s",
                request.email,
            )
            raise EmailAlreadyExistsException()

        logger.info("Registering student with email=%s", request.email)

        user = User(
            role=UserRole.STUDENT,
        )
        user.set_email(request.email)
        user.set_password(request.password)

        student = Student(
            full_name=request.full_name,
            roll_number=request.roll_number,
            phone_number=request.phone_number,
            branch=request.branch,
            semester=request.semester,
            cgpa=request.cgpa,
            resume_path=request.resume_path,
        )

        student.user = user

        try:
            self.user_repository.create(user)
            self.student_repository.create(student)
            self.user_repository.save()
        except Exception:
            logger.exception(
                "Failed to register student with email=%s",
                request.email,
            )
            self.user_repository.rollback()
            raise
        return StudentMapper.to_response(student)

    def register_company(
        self,
        request: CompanyRegistrationRequest,
    ) -> CompanyResponse:
        if self.user_repository.exists_by_email(request.email):
            logger.warning(
                "Company registration attempted with existing email=%s",
                request.email,
            )
            raise EmailAlreadyExistsException()

        user = User(
            role=UserRole.COMPANY,
        )
        user.set_email(request.email)
        user.set_password(request.password)

        company = Company(
            company_name=request.company_name,
            website=request.website,
            description=request.description,
            industry=request.industry,
            contact_person=request.contact_person,
            contact_email=request.contact_email,
            contact_phone=request.contact_phone,
        )

        company.user = user

        try:
            self.user_repository.create(user)
            self.company_repository.create(company)

            self.user_repository.save()

        except Exception:
            logger.exception(
                "Failed to register company with email=%s",
                request.email,
            )
            self.user_repository.rollback()
            raise

        return CompanyMapper.to_response(company)

    def login(
        self,
        request: LoginRequest,
    ) -> LoginResponse:
        logger.info("Login attempt for email=%s", request.email)
        user = self.user_repository.get_by_email(request.email)
        user = self._validate_credentials(user, request)
        self._ensure_account_active(user)
        self._ensure_account_not_blacklisted(user)
        self._ensure_account_approved(user)

        token = create_access_token_for_user(user)
        logger.info("User logged in successfully: email=%s", request.email)

        return LoginResponse(
            access_token=token,
        )

    def _validate_credentials(
        self,
        user: User | None,
        request: LoginRequest,
    ) -> User:
        if user is None:
            logger.warning("Login failed: unknown email=%s", request.email)
            raise InvalidCredentialsException()

        if not user.check_password(request.password):
            logger.warning("Login failed: invalid password for email=%s", request.email)
            raise InvalidCredentialsException()
        return user

    def _ensure_account_active(self, user: User) -> None:
        if not user.is_active:
            raise AccountDisabledException()

    def _ensure_account_not_blacklisted(self, user: User) -> None:
        if user.account_status == AccountStatus.BLACKLISTED:
            raise AccountBlacklistedException()

    def _ensure_account_approved(self, user: User) -> None:

        match user.role:
            case UserRole.STUDENT:
                student = self.student_repository.get_by_user_id(user.id)

                if (
                    student is None
                    or student.approval_status != ApprovalStatus.APPROVED
                ):
                    raise AccountNotApprovedException()
            case UserRole.COMPANY:
                company = self.company_repository.get_by_user_id(user.id)

                if (
                    company is None
                    or company.approval_status != ApprovalStatus.APPROVED
                ):
                    raise AccountNotApprovedException()
            case _:
                raise InvalidCredentialsException()

    def get_current_user(
        self,
        user_id: UUID,
    ) -> StudentResponse | CompanyResponse:
        user = self.user_repository.get_by_id(user_id)

        if user is None:
            raise InvalidCredentialsException()

        match user.role:
            case UserRole.STUDENT:
                student = self.student_repository.get_by_user_id(user.id)

                if student is None:
                    raise InvalidCredentialsException()

                return StudentMapper.to_response(student)

            case UserRole.COMPANY:
                company = self.company_repository.get_by_user_id(user.id)

                if company is None:
                    raise InvalidCredentialsException()

                return CompanyMapper.to_response(company)

            case _:
                raise InvalidCredentialsException()