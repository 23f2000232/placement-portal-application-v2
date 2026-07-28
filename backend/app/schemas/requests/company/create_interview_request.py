from datetime import datetime, UTC

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.enums import InterviewMode


class CreateInterviewRequest(BaseModel):

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )

    round_number: int = Field(
        ge=1,
    )

    interviewer_name: str | None = Field(
        default=None,
        max_length=100,
    )

    interview_mode: InterviewMode

    meeting_link: str | None = Field(
        default=None,
        max_length=500,
    )

    location: str | None = Field(
        default=None,
        max_length=255,
    )

    scheduled_for: datetime

    @field_validator("scheduled_for")
    @classmethod
    def validate_scheduled_for(
        cls,
        value: datetime,
    ) -> datetime:

        if value <= datetime.now(UTC):
            raise ValueError("Interview must be scheduled in the future.")

        return value

    @model_validator(mode="after")
    def validate_interview_mode(self):

        if self.interview_mode == InterviewMode.ONLINE and not self.meeting_link:
            raise ValueError("Meeting link is required for online interviews.")

        if self.interview_mode == InterviewMode.OFFLINE and not self.location:
            raise ValueError("Location is required for offline interviews.")

        return self