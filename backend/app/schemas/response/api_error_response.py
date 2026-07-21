from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.enums import ErrorCode


class ApiErrorResponse(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    timestamp: datetime
    status: int
    error: ErrorCode
    message: str
    path: str