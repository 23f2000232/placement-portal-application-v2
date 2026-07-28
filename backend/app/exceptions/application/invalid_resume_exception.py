from http import HTTPStatus

from app.enums import ErrorCode
from app.exceptions import AppException


class InvalidResumeException(AppException):

    def __init__(self):
        super().__init__(
            "Only PDF files are allowed.",
            ErrorCode.INVALID_RESUME,
            HTTPStatus.BAD_REQUEST,
        )