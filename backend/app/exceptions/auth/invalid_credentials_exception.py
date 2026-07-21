from http import HTTPStatus

from app.enums import ErrorCode
from app.exceptions.app_exception import AppException


class InvalidCredentialsException(AppException):
    def __init__(self):
        super().__init__(
            "Invalid email or password.",
            ErrorCode.INVALID_CREDENTIALS,
            HTTPStatus.UNAUTHORIZED,
        )