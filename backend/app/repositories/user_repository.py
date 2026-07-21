from sqlalchemy import select

from app.enums import UserRole, AccountStatus
from app.extensions import db
from app.models.user import User
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    def get_by_email(self, email: str) -> User | None:
        return db.session.scalar(select(User).where(User.email == email))

    def exists_by_email(self, email: str) -> bool:
        return self.get_by_email(email) is not None

    def get_by_role(self, role: UserRole) -> list[User]:
        return db.session.scalars(select(User).where(User.role == role)).all()

    def get_active_users(self, active: bool = True) -> list[User]:
        return db.session.scalars(select(User).where(User.is_active.is_(active))).all()

    def get_by_account_status(
        self,
        status: AccountStatus,
    ) -> list[User]:
        return db.session.scalars(
            select(User).where(User.account_status == status)
        ).all()