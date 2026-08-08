from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.enums import InterviewMode, InterviewStatus


class InterviewResponse(BaseModel):

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    id: UUID

    application_id: UUID

    student_name: str

    company_name: str

    job_title: str

    round_number: int

    interviewer_name: str | None

    interview_mode: InterviewMode

    meeting_link: str | None

    location: str | None

    scheduled_for: datetime

    feedback: str | None

    status: InterviewStatus

    created_at: datetime

    updated_at: datetime
