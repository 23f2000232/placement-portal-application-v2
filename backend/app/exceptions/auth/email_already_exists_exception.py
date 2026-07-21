from http import HTTPStatus

from app.enums import ErrorCode
from app.exceptions.app_exception import AppException


class EmailAlreadyExistsException(AppException):
    def __init__(self):
        super().__init__(
            "Email is already registered.",
            ErrorCode.EMAIL_ALREADY_EXISTS,
            HTTPStatus.CONFLICT,
        )