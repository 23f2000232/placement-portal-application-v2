from http import HTTPStatus

from app.enums import ErrorCode
from app.exceptions import AppException


class PlacementDriveNotDeletableException(AppException):
    def __init__(self, drive_id):
        super().__init__(
            f"Placement Drive {drive_id} cannot be deleted",
            ErrorCode.UNAUTHORIZED,
            HTTPStatus.FORBIDDEN,
        )