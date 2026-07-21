from http import HTTPStatus

from app.enums.error_code import ErrorCode


class AppException(Exception):
    def __init__(
        self,
        message: str,
        error_code: ErrorCode,
        status_code: HTTPStatus,
    ):
        super().__init__(message)

        self.message = message
        self.error_code = error_code
        self.status_code = status_code