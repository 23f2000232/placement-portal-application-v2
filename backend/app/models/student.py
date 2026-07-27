from app.enums import ApprovalStatus
from app.extensions import db
from app.models.base_model import BaseModel


class Student(BaseModel):
    __tablename__ = "students"

    user_id = db.Column(
        db.Uuid,
        db.ForeignKey("users.id"),
        nullable=False,
        unique=True,
    )
    approval_status = db.Column(
        db.Enum(ApprovalStatus, native_enum=False),
        nullable=False,
        default=ApprovalStatus.PENDING,
    )
    full_name = db.Column(
        db.String(100),
        nullable=False,
    )

    roll_number = db.Column(
        db.String(20),
        nullable=False,
        unique=True,
    )

    phone_number = db.Column(
        db.String(15),
        nullable=False,
        unique=True,
    )

    branch = db.Column(
        db.String(50),
        nullable=False,
    )

    semester = db.Column(
        db.Integer,
        nullable=False,
    )

    cgpa = db.Column(
        # for 10.00
        db.Numeric(4, 2),
        nullable=False,
    )

    resume_path = db.Column(
        db.String(255),
        nullable=True,
    )
    current_backlogs = db.Column(
        db.Integer,
        nullable=False,
        default=0,
    )

    user = db.relationship(
        "User",
        back_populates="student",
    )

    applications = db.relationship(
        "Application",
        back_populates="student",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Student {self.roll_number}>"