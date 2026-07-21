from datetime import datetime
from http import HTTPStatus

from pydantic import BaseModel, ConfigDict

from app.enums import ErrorCode


class ApiErrorResponse(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    timestamp: datetime
    status: HTTPStatus
    error: ErrorCode
    message: str
    path: str