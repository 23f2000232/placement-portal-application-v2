from http import HTTPStatus

from app.enums import ErrorCode
from app.exceptions.app_exception import AppException


class UnauthorizedException(AppException):
    def __init__(self):
        super().__init__(
            "Authentication is required.",
            ErrorCode.UNAUTHORIZED,
            HTTPStatus.UNAUTHORIZED,
        )