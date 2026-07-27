from http import HTTPStatus

from app.enums import ErrorCode, ApplicationStatus
from app.exceptions import AppException


class InvalidApplicationStatusTransitionException(
    AppException,
):
    def __init__(
        self,
        current_status: ApplicationStatus,
        expected_status: ApplicationStatus,
    ):
        super().__init__(
            (
                f"Application must be in '{expected_status.value}' "
                f"status but is currently '{current_status.value}'."
            ),
            ErrorCode.INVALID_APPLICATION_STATUS_TRANSITION,
            HTTPStatus.CONFLICT,
        )


# Instead of passing a single expected_status, we can update  exception to support multiple allowed statuses: