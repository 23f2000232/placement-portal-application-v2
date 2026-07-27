from http import HTTPStatus

from app.enums import ErrorCode
from app.exceptions import AppException


class ApplicationNotFoundException(AppException):
    def __init__(self, app_id):
        super().__init__(
            f"Application with {app_id} not found",
            ErrorCode.RESOURCE_NOT_FOUND,
            HTTPStatus.NOT_FOUND,
        )