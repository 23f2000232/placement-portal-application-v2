from http import HTTPStatus

from app.enums import ErrorCode
from app.exceptions.app_exception import AppException


class StudentAlreadyApprovedException(AppException):
    def __init__(self, student_id):
        super().__init__(
            f"Your account {student_id} is already approved.",
            ErrorCode.ACCOUNT_NOT_APPROVED,
            HTTPStatus.UNAUTHORIZED,
        )