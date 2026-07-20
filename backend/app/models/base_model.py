import uuid
from datetime import UTC, datetime

from app.extensions import db


def utc_now():
    return datetime.now(UTC)


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(
        db.Uuid,
        primary_key=True,
        default=uuid.uuid4,
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=utc_now(),
        nullable=False,
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=utc_now(),
        onupdate=utc_now(),
        nullable=False,
    )

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id}>"