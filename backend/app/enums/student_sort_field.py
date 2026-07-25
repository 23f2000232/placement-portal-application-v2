from enum import StrEnum


class StudentSortField(StrEnum):
    CREATED_AT = "created_at"
    FULL_NAME = "full_name"
    ROLL_NUMBER = "roll_number"
    CGPA = "cgpa"
    SEMESTER = "semester"