from app.enums.application_status import ApplicationStatus
from app.extensions import db
from app.models.base_model import BaseModel, utc_now


class Application(BaseModel):
    __tablename__ = "applications"

    __table_args__ = (
        db.UniqueConstraint(
            "student_id",
            "placement_drive_id",
            name="uq_student_placement_drive",
        ),
    )

    student_id = db.Column(
        db.Uuid,
        db.ForeignKey("students.id"),
        nullable=False,
    )

    placement_drive_id = db.Column(
        db.Uuid,
        db.ForeignKey("placement_drives.id"),
        nullable=False,
    )

    status = db.Column(
        db.Enum(
            ApplicationStatus,
            native_enum=False,
        ),
        nullable=False,
        default=ApplicationStatus.APPLIED,
    )
    status_updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )

    resume_path = db.Column(
        db.String(500),
        nullable=True,
    )

    student = db.relationship(
        "Student",
        back_populates="applications",
    )

    placement_drive = db.relationship(
        "PlacementDrive",
        back_populates="applications",
    )

    interviews = db.relationship(
        "Interview",
        back_populates="application",
        cascade="all, delete-orphan",
    )

    placement_record = db.relationship(
        "PlacementRecord",
        back_populates="application",
        uselist=False,
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"<Application("
            f"student={self.student_id}, "
            f"drive={self.placement_drive_id}, "
            f"status={self.status.value})>"
        )