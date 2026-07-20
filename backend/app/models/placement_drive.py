from app.enums.placement_drive_status import PlacementDriveStatus
from app.extensions import db
from app.models.base_model import BaseModel


class PlacementDrive(BaseModel):
    __tablename__ = "placement_drives"

    company_id = db.Column(
        db.Uuid,
        db.ForeignKey("companies.id"),
        nullable=False,
    )

    title = db.Column(
        db.String(100),
        nullable=False,
    )

    description = db.Column(
        db.Text,
        nullable=False,
    )

    location = db.Column(
        db.String(100),
        nullable=False,
    )

    package = db.Column(
        db.Numeric(6, 2),
        nullable=False,
    )

    minimum_cgpa = db.Column(
        db.Numeric(4, 2),
        nullable=False,
    )

    eligible_branches = db.Column(
        db.JSON,
        nullable=False,
    )

    maximum_backlogs = db.Column(
        db.Integer,
        nullable=False,
        default=0,
    )

    application_deadline = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
    )

    interview_date = db.Column(
        db.DateTime(timezone=True),
        nullable=True,
    )

    status = db.Column(
        db.Enum(
            PlacementDriveStatus,
            native_enum=False,
        ),
        nullable=False,
        default=PlacementDriveStatus.DRAFT,
    )

    company = db.relationship(
        "Company",
        back_populates="placement_drives",
    )

    applications = db.relationship(
        "Application",
        back_populates="placement_drive",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<PlacementDrive {self.title}>"