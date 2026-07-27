from http import HTTPStatus

from app.enums import ErrorCode
from app.exceptions import AppException


class PlacementDriveNotCancellableException(AppException):
    def __init__(self, drive_id):
        super().__init__(
            f"Placement Drive {drive_id} cannot be cancelled",
            ErrorCode.UNAUTHORIZED,
            HTTPStatus.FORBIDDEN,
        )