from app.enums import UserRole
from app.models.student import Student
from app.schemas.response.auth.student_response import StudentResponse


class StudentMapper:

    @staticmethod
    def to_response(student: Student) -> StudentResponse:
        return StudentResponse(
            id=student.id,
            email=student.user.email,
            full_name=student.full_name,
            roll_number=student.roll_number,
            phone_number=student.phone_number,
            branch=student.branch,
            semester=student.semester,
            cgpa=float(student.cgpa),
            current_backlogs=student.current_backlogs,
            skills=student.skills or [],
            approval_status=student.approval_status,
            role=UserRole.STUDENT,
        )
