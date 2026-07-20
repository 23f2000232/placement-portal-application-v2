from uuid import UUID

from sqlalchemy import select

from app.enums import ApprovalStatus
from app.extensions import db
from app.models.student import Student
from app.repositories.base_repository import BaseRepository


class StudentRepository(BaseRepository[Student]):
    def __init__(self):
        super().__init__(Student)

    def get_by_user_id(self, user_id: UUID) -> Student | None:
        return db.session.scalar(select(Student).where(Student.user_id == user_id))

    def get_by_approval_status(
        self,
        status: ApprovalStatus,
    ) -> list[Student]:
        return db.session.scalars(
            select(Student).where(Student.approval_status == status)
        ).all()