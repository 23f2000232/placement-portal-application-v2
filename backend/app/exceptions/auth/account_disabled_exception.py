from http import HTTPStatus

from app.enums import ErrorCode
from app.exceptions.app_exception import AppException


class AccountDisabledException(AppException):
    def __init__(self):
        super().__init__(
            "Your account has been disabled.",
            ErrorCode.ACCOUNT_DISABLED,
            HTTPStatus.FORBIDDEN,
        )