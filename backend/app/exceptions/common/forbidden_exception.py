from http import HTTPStatus

from app.enums import ErrorCode
from app.exceptions.app_exception import AppException


class ForbiddenException(AppException):

    def __init__(self):
        super().__init__(
            "You are not authorized to access this resource.",
            ErrorCode.FORBIDDEN,
            HTTPStatus.FORBIDDEN,
        )