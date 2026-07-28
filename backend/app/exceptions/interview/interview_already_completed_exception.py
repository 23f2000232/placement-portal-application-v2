from http import HTTPStatus

from app.enums import ErrorCode


class InterviewAlreadyCompletedException(Exception):
    def __init__(self, interview_id):
        super().__init__(
            f"The interview {interview_id} is already completed",
            ErrorCode.INTERVIEW_ALREADY_COMPLETED,
            HTTPStatus.ALREADY_REPORTED,
        )