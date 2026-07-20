from enum import StrEnum

# Whether a candidate passes a round is really an application outcome, not the interview's state.
# An interview can be:
# scheduled
# completed
# cancelled


class InterviewStatus(StrEnum):
    SCHEDULED = "SCHEDULED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"