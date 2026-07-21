from app.exceptions.app_exception import AppException


class ForbiddenException(AppException):
    def __init__(self):
        super().__init__("You do not have permission to perform this action.")