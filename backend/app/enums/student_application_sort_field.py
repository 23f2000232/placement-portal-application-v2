from enum import StrEnum


class StudentApplicationSortField(StrEnum):
    APPLIED_AT = "applied_at"
    STATUS = "status"
    COMPANY_NAME = "company_name"
    JOB_TITLE = "job_title"
    SALARY_PACKAGE = "salary_package"