from enum import StrEnum

# With StrEnum, this evaluates naturally because each enum value is also a string.
# That makes serialization and comparisons with request data more convenient.


class UserRole(StrEnum):
    ADMIN = "ADMIN"
    COMPANY = "COMPANY"
    STUDENT = "STUDENT"