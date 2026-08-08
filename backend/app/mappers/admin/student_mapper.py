from app.models import Student
from app.schemas.response.admin import StudentSummaryResponse


class StudentMapper:

    @staticmethod
    def to_summary_response(
        student: Student,
    ) -> StudentSummaryResponse:
        return StudentSummaryResponse(
            id=student.id,
            user_id=student.user_id,
            email=student.user.email,
            full_name=student.full_name,
            roll_number=student.roll_number,
            branch=student.branch,
            semester=student.semester,
            cgpa=student.cgpa,
            approval_status=student.approval_status,
            account_status=student.user.account_status,
        )
