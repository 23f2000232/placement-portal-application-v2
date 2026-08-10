from datetime import UTC

from app.models import Interview
from app.schemas.response.interview.interview_response import (
    InterviewResponse,
)


class InterviewMapper:

    @staticmethod
    def _as_utc(value):
        """SQLite returns timezone-aware columns as naive UTC datetimes."""
        return value if value.tzinfo is not None else value.replace(tzinfo=UTC)

    @staticmethod
    def to_response(
        interview: Interview,
    ) -> InterviewResponse:
        return InterviewResponse(
            id=interview.id,
            application_id=interview.application_id,
            student_name=interview.application.student.full_name,
            company_name=interview.application.placement_drive.company.company_name,
            job_title=interview.application.placement_drive.title,
            round_number=interview.round_number,
            interviewer_name=interview.interviewer_name,
            interview_mode=interview.interview_mode,
            meeting_link=interview.meeting_link,
            location=interview.location,
            # The browser submits an ISO UTC instant. Restore its UTC offset on
            # SQLite responses so clients can correctly render local time.
            scheduled_for=InterviewMapper._as_utc(interview.scheduled_for),
            feedback=interview.feedback,
            status=interview.status,
            created_at=interview.created_at,
            updated_at=interview.updated_at,
        )
