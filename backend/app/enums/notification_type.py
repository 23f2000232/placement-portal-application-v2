from enum import StrEnum


class NotificationType(StrEnum):
    GENERAL = "GENERAL"
    APPLICATION = "APPLICATION"
    INTERVIEW = "INTERVIEW"
    PLACEMENT = "PLACEMENT"
    SYSTEM = "SYSTEM"