from http import HTTPStatus

from app.enums import ErrorCode
from app.exceptions import AppException


class ApplicationDeadlinePassedException(AppException):
    def __init__(self):
        super().__init__(
            "The application deadline for this placement drive has passed.",
            ErrorCode.APPLICATION_DEADLINE_PASSED,
            HTTPStatus.FORBIDDEN,
        )
