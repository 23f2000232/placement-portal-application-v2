from http import HTTPStatus

from app.enums import ErrorCode
from app.exceptions import AppException


class ApplicationNotWithdrawableException(AppException):

    def __init__(self):
        super().__init__(
            "This application can no longer be withdrawn.",
            ErrorCode.APPLICATION_NOT_WITHDRAWABLE,
            HTTPStatus.CONFLICT,
        )