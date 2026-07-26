from http import HTTPStatus

from app.enums import ErrorCode
from app.exceptions import AppException


class InvalidInterviewDateException(AppException):
    def __init__(self):
        super().__init__(
            "Invalid Interview Date",
            ErrorCode.INVALID_DATE,
            HTTPStatus.FORBIDDEN,
        )