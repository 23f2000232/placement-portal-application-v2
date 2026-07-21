from app.exceptions.app_exception import AppException


class BadRequestException(AppException):
    def __init__(self, message: str):
        super().__init__(message)