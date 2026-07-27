from http import HTTPStatus

from app.enums import ErrorCode
from app.exceptions import AppException


class PlacementDriveAccessDeniedException(AppException):
    def __init__(self, drive_id):
        super().__init__(
            f"You dont have the access to drive {drive_id}",
            ErrorCode.UNAUTHORIZED,
            HTTPStatus.FORBIDDEN,
        )