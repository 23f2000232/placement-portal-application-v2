from http import HTTPStatus

from app.enums import ErrorCode
from app.exceptions.app_exception import AppException


class StudentAlreadyRejectedException(AppException):
    def __init__(self, student_id):
        super().__init__(
            f"Your account with student id {student_id} is already rejected",
            ErrorCode.ACCOUNT_NOT_APPROVED,
            HTTPStatus.UNAUTHORIZED,
        )