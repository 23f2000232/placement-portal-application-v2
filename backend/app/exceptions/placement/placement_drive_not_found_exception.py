from http import HTTPStatus

from app.enums import ErrorCode
from app.exceptions import AppException


class PlacementDriveNotFoundException(AppException):
    def __init__(self, drive_id):
        super().__init__(
            f"Placement Drive {drive_id} not found",
            ErrorCode.RESOURCE_NOT_FOUND,
            HTTPStatus.FORBIDDEN,
        )