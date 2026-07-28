from http import HTTPStatus

from app.enums import ErrorCode
from app.exceptions import AppException


class InterviewRoundAlreadyExistsException(AppException):
    def __init__(self, app_id: int, round_number: int):
        super().__init__(
            f"Interview  with {app_id} round {round_number} already exists",
            ErrorCode.INTERVIEW_ROUND_ALREADY_EXISTS,
            HTTPStatus.BAD_REQUEST,
        )