from uuid import UUID

from sqlalchemy import select

from app.extensions import db
from app.models.notification import Notification
from app.repositories.base_repository import BaseRepository


class NotificationRepository(BaseRepository[Notification]):
    def __init__(self):
        super().__init__(Notification)

    def get_by_user_id(
        self,
        user_id: UUID,
    ) -> list[Notification]:
        return db.session.scalars(
            select(Notification).where(Notification.user_id == user_id)
        ).all()

    def get_unread_by_user_id(
        self,
        user_id: UUID,
    ) -> list[Notification]:
        return db.session.scalars(
            select(Notification).where(
                Notification.user_id == user_id,
                Notification.is_read.is_(False),
            )
        ).all()

    def get_read_by_user_id(
        self,
        user_id: UUID,
    ) -> list[Notification]:
        return db.session.scalars(
            select(Notification).where(
                Notification.user_id == user_id,
                Notification.is_read.is_(True),
            )
        ).all()