from app.enums.approval_status import ApprovalStatus
from app.extensions import db
from app.models.base_model import BaseModel


class Company(BaseModel):
    __tablename__ = "companies"

    user_id = db.Column(
        db.Uuid,
        db.ForeignKey("users.id"),
        nullable=False,
        unique=True,
    )

    company_name = db.Column(
        db.String(100),
        nullable=False,
        index=True,
    )

    website = db.Column(
        db.String(500),
        nullable=True,
    )

    description = db.Column(
        db.Text,
        nullable=True,
    )

    industry = db.Column(
        db.String(100),
        nullable=False,
    )

    contact_person = db.Column(
        db.String(100),
        nullable=False,
    )

    contact_email = db.Column(
        db.String(255),
        nullable=False,
    )

    contact_phone = db.Column(
        db.String(15),
        nullable=False,
    )

    approval_status = db.Column(
        db.Enum(ApprovalStatus, native_enum=False),
        nullable=False,
        default=ApprovalStatus.PENDING,
    )

    user = db.relationship(
        "User",
        back_populates="company",
    )

    placement_drives = db.relationship(
        "PlacementDrive",
        back_populates="company",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Company {self.company_name}>"