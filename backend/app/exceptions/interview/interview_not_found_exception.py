from http import HTTPStatus
from uuid import UUID

from app.enums import ErrorCode


class InterviewNotFoundException(Exception):
    def __init__(self, interview_id: UUID) -> None:
        super().__init__(
            f"Interview {interview_id} not found",
            ErrorCode.RESOURCE_NOT_FOUND,
            HTTPStatus.NOT_FOUND,
        )