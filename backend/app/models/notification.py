from app.enums import NotificationType
from app.extensions import db
from app.models.base_model import BaseModel


class Notification(BaseModel):
    __tablename__ = "notifications"

    user_id = db.Column(
        db.Uuid,
        db.ForeignKey("users.id"),
        nullable=False,
    )

    title = db.Column(
        db.String(200),
        nullable=False,
    )

    message = db.Column(
        db.Text,
        nullable=False,
    )

    notification_type = db.Column(
        db.Enum(
            NotificationType,
            native_enum=False,
        ),
        nullable=False,
        default=NotificationType.GENERAL,
    )

    is_read = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
    )

    read_at = db.Column(
        db.DateTime(timezone=True),
        nullable=True,
    )

    user = db.relationship(
        "User",
        back_populates="notifications",
    )

    def __repr__(self):
        return (
            f"<Notification("
            f"user={self.user_id}, "
            f"type={self.notification_type.value}, "
            f"read={self.is_read})>"
        )