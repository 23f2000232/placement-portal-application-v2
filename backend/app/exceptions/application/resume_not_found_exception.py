from http import HTTPStatus

from app.enums import ErrorCode
from app.exceptions import AppException


class ResumeNotFoundException(AppException):

    def __init__(self):
        super().__init__(
            "Resume not found.",
            ErrorCode.RESOURCE_NOT_FOUND,
            HTTPStatus.NOT_FOUND,
        )