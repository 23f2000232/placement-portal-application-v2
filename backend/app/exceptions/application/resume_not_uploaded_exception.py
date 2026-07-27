from http import HTTPStatus

from app.enums import ErrorCode
from app.exceptions import AppException


class ResumeNotUploadedException(AppException):

    def __init__(self):
        super().__init__(
            "Please upload your resume before applying.",
            ErrorCode.RESUME_NOT_UPLOADED,
            HTTPStatus.BAD_REQUEST,
        )