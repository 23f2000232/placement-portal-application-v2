from app.enums.account_status import AccountStatus
from app.enums.user_role import UserRole
from app.extensions import db
from app.models.base_model import BaseModel
from app.utils.password_utils import hash_password, verify_password


class User(BaseModel):
    __tablename__ = "users"

    email = db.Column(
        db.String(255),
        unique=True,
        nullable=False,
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False,
    )

    role = db.Column(
        db.Enum(UserRole, native_enum=False),
        nullable=False,
    )

    is_active = db.Column(
        db.Boolean,
        default=True,
        nullable=False,
    )

    account_status = db.Column(
        db.Enum(AccountStatus, native_enum=False),
        default=AccountStatus.ACTIVE,
        nullable=False,
    )

    student = db.relationship(
        "Student",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )

    company = db.relationship(
        "Company",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    notifications = db.relationship(
        "Notification",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def set_password(self, password: str) -> None:
        self.password_hash = hash_password(password)

    def check_password(self, password: str) -> bool:
        return verify_password(password, self.password_hash)

    def set_email(self, email: str) -> None:
        self.email = email.strip().lower()

    def __repr__(self) -> str:
        return f"<User {self.email}>"