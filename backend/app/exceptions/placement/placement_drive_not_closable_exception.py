from http import HTTPStatus

from app.enums import ErrorCode
from app.exceptions import AppException


class PlacementDriveNotClosableException(AppException):
    def __init__(self, drive_id):
        super().__init__(
            f"Placement drive {drive_id} is not closable",
            ErrorCode.UNAUTHORIZED,
            HTTPStatus.FORBIDDEN,
        )