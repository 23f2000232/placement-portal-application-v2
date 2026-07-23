from http import HTTPStatus

from app.enums import ErrorCode
from app.exceptions.app_exception import AppException


class InvalidPaginationException(AppException):
    def __init__(self, message):
        super().__init__(
            message,
            ErrorCode.BAD_REQUEST,
            HTTPStatus.BAD_REQUEST,
        )