from app.enums import PlacementStatus
from app.extensions import db
from app.models.base_model import BaseModel


class PlacementRecord(BaseModel):
    __tablename__ = "placement_records"

    application_id = db.Column(
        db.Uuid,
        db.ForeignKey("applications.id"),
        nullable=False,
        unique=True,
    )

    offered_package = db.Column(
        db.Numeric(10, 2),
        nullable=False,
    )

    joining_date = db.Column(
        db.Date,
        nullable=True,
    )

    offer_letter_path = db.Column(
        db.String(500),
        nullable=True,
    )

    status = db.Column(
        db.Enum(
            PlacementStatus,
            native_enum=False,
        ),
        nullable=False,
        default=PlacementStatus.OFFERED,
    )

    application = db.relationship(
        "Application",
        back_populates="placement_record",
    )

    def __repr__(self):
        return (
            f"<PlacementRecord("
            f"application={self.application_id}, "
            f"status={self.status.value})>"
        )