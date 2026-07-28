from pydantic import Field, ConfigDict, BaseModel, field_validator

from app.enums import InterviewStatus


class CompleteInterviewRequest(BaseModel):

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    status: InterviewStatus

    remarks: str | None = Field(
        default=None,
        max_length=2000,
    )

    @field_validator("status")
    @classmethod
    def validate_status(
        cls,
        value: InterviewStatus,
    ) -> InterviewStatus:

        if value == InterviewStatus.SCHEDULED:
            raise ValueError("Interview cannot be completed with SCHEDULED status.")

        if value not in (
            InterviewStatus.COMPLETED,
            InterviewStatus.CANCELLED,
        ):
            raise ValueError("Invalid interview completion status.")

        return value