from app.enums import InterviewMode
from app.enums import InterviewStatus
from app.extensions import db
from app.models.base_model import BaseModel


class Interview(BaseModel):
    __tablename__ = "interviews"

    __table_args__ = (
        db.UniqueConstraint(
            "application_id",
            "round_number",
            name="uq_application_round",
        ),
        db.CheckConstraint(
            "round_number > 0",
            name="ck_round_number_positive",
        ),
    )

    application_id = db.Column(
        db.Uuid,
        db.ForeignKey("applications.id"),
        nullable=False,
    )

    round_number = db.Column(
        db.Integer,
        nullable=False,
    )

    interviewer_name = db.Column(
        db.String(100),
        nullable=True,
    )

    interview_mode = db.Column(
        db.Enum(
            InterviewMode,
            native_enum=False,
        ),
        nullable=False,
    )

    scheduled_for = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
    )

    feedback = db.Column(
        db.Text,
        nullable=True,
    )
    meeting_link = db.Column(
        db.String(500),
        nullable=True,
    )

    location = db.Column(
        db.String(255),
        nullable=True,
    )

    status = db.Column(
        db.Enum(
            InterviewStatus,
            native_enum=False,
        ),
        nullable=False,
        default=InterviewStatus.SCHEDULED,
    )

    application = db.relationship(
        "Application",
        back_populates="interviews",
    )

    def __repr__(self) -> str:
        return (
            f"<Interview("
            f"application={self.application_id}, "
            f"round={self.round_number})>"
        )