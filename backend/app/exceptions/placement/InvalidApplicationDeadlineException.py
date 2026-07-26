from http import HTTPStatus

from app.enums import ErrorCode
from app.exceptions import AppException


class InvalidApplicationDeadlineException(AppException):
    def __init__(self):
        super().__init__(
            "Invalid Application Deadline",
            ErrorCode.INVALID_APPLICATION_DEADLINE,
            HTTPStatus.FORBIDDEN,
        )