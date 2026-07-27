from http import HTTPStatus

from app.enums import ErrorCode
from app.exceptions import AppException


class AlreadyAppliedException(AppException):

    def __init__(self):
        super().__init__(
            "You have already applied for this placement drive.",
            ErrorCode.ALREADY_APPLIED,
            HTTPStatus.CONFLICT,
        )