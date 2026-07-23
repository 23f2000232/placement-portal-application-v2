from enum import StrEnum


class UserSortField(StrEnum):
    EMAIL = "email"
    ROLE = "role"
    ACCOUNT_STATUS = "account_status"
    CREATED_AT = "created_at"