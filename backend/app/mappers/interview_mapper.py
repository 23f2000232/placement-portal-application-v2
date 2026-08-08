from app.models import Interview
from app.schemas.response.interview.interview_response import (
    InterviewResponse,
)


class InterviewMapper:

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
            scheduled_for=interview.scheduled_for,
            feedback=interview.feedback,
            status=interview.status,
            created_at=interview.created_at,
            updated_at=interview.updated_at,
        )
