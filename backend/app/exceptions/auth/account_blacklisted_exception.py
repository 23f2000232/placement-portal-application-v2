from http import HTTPStatus

from app.enums import ErrorCode
from app.exceptions import AppException


class AccountBlacklistedException(AppException):
    def __init__(self):
        super().__init__(
            "Your account has been disabled.",
            ErrorCode.ACCOUNT_BLACKLISTED,
            HTTPStatus.FORBIDDEN,
        )