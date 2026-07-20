from uuid import UUID

from sqlalchemy import select

from app.enums import ApprovalStatus
from app.extensions import db
from app.models.company import Company
from app.repositories.base_repository import BaseRepository


class CompanyRepository(BaseRepository[Company]):
    def __init__(self):
        super().__init__(Company)

    def get_by_user_id(
        self,
        user_id: UUID,
    ) -> Company | None:
        return db.session.scalar(select(Company).where(Company.user_id == user_id))

    def get_by_approval_status(
        self,
        status: ApprovalStatus,
    ) -> list[Company]:
        return db.session.scalars(
            select(Company).where(Company.approval_status == status)
        ).all()