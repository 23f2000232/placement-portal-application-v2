from app.enums.user_role import UserRole
from app.extensions import bcrypt, db
from app.models.base_model import BaseModel


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

    def set_password(self, password: str) -> None:
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password_hash, password)

    def set_email(self, email: str) -> None:
        self.email = email.strip().lower()

    def __repr__(self) -> str:
        return f"<User {self.email}>"