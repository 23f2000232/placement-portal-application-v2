from app.exceptions.app_exception import AppException


class ResourceNotFoundException(AppException):
    def __init__(self, resource: str):
        super().__init__(
            message=f"{resource} not found.",
            status_code=404,
        )