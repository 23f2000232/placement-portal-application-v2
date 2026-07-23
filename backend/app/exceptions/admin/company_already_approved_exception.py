from http import HTTPStatus

from app.enums import ErrorCode
from app.exceptions.app_exception import AppException


class CompanyAlreadyApprovedException(AppException):
    def __init__(self, company_id):
        super().__init__(
            f"Your account {company_id} is already approved.",
            ErrorCode.COMPANY_ALREADY_EXISTS,
            HTTPStatus.UNAUTHORIZED,
        )