from http import HTTPStatus

from app.enums import ErrorCode
from app.exceptions.app_exception import AppException


class CompanyAlreadyRejectedException(AppException):
    def __init__(self, company_id):
        super().__init__(
            f"Your account with company id {company_id} is  rejected",
            ErrorCode.ACCOUNT_NOT_APPROVED,
            HTTPStatus.UNAUTHORIZED,
        )