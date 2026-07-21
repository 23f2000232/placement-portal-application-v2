from http import HTTPStatus

from app.enums import ErrorCode
from app.exceptions.app_exception import AppException


class AccountNotApprovedException(AppException):
    def __init__(self):
        super().__init__(
            "Your account is awaiting approval.",
            ErrorCode.ACCOUNT_NOT_APPROVED,
            HTTPStatus.UNAUTHORIZED,
        )