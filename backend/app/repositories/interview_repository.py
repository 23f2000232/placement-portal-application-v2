from uuid import UUID

from sqlalchemy import select

from app.enums import InterviewStatus
from app.extensions import db
from app.models.interview import Interview
from app.repositories.base_repository import BaseRepository


class InterviewRepository(BaseRepository[Interview]):
    def __init__(self):
        super().__init__(Interview)

    def get_by_application_id(
        self,
        application_id: UUID,
    ) -> list[Interview]:
        return db.session.scalars(
            select(Interview).where(Interview.application_id == application_id)
        ).all()

    def get_by_status(
        self,
        status: InterviewStatus,
    ) -> list[Interview]:
        return db.session.scalars(
            select(Interview).where(Interview.status == status)
        ).all()

    def get_by_application_and_round(
        self,
        application_id: UUID,
        round_number: int,
    ) -> Interview | None:
        return db.session.scalar(
            select(Interview).where(
                Interview.application_id == application_id,
                Interview.round_number == round_number,
            )
        )