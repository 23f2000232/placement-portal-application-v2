from uuid import UUID

from sqlalchemy import select, exists, func

from app import Application, PlacementDrive
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
            select(Interview)
            .where(Interview.application_id == application_id)
            .order_by(
                Interview.round_number.asc(),
            )
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

    def exists_round(
        self,
        application_id: UUID,
        round_number: int,
    ) -> bool:
        query = select(
            exists().where(
                Interview.application_id == application_id,
                Interview.round_number == round_number,
            )
        )

        return bool(db.session.scalar(query))

    def get_upcoming_student_interviews(
        self,
        student_id: UUID,
    ) -> list[Interview]:
        return db.session.scalars(
            select(Interview)
            .join(
                Interview.application,
            )
            .where(
                Application.student_id == student_id,
                Interview.status == InterviewStatus.SCHEDULED,
                Interview.scheduled_for >= func.now(),
            )
            .order_by(
                Interview.scheduled_for.asc(),
            )
        ).all()

    def get_upcoming_company_interviews(
        self,
        company_id: UUID,
    ) -> list[Interview]:
        return db.session.scalars(
            select(Interview)
            .join(Interview.application)
            .join(Application.placement_drive)
            .where(
                PlacementDrive.company_id == company_id,
                Interview.status == InterviewStatus.SCHEDULED,
                Interview.scheduled_for >= func.now(),
            )
            .order_by(
                Interview.scheduled_for.asc(),
            )
        ).all()

    def get_latest_by_application(
        self,
        application_id: UUID,
    ) -> Interview | None:
        return db.session.scalar(
            select(Interview)
            .where(
                Interview.application_id == application_id,
            )
            .order_by(
                Interview.round_number.desc(),
            )
            .limit(1)
        )

    def get_all_ordered(self) -> list[Interview]:
        return db.session.scalars(
            select(Interview).order_by(Interview.scheduled_for.desc())
        ).all()

    def get_student_interviews(self, student_id: UUID) -> list[Interview]:
        return db.session.scalars(
            select(Interview)
            .join(Interview.application)
            .where(Application.student_id == student_id)
            .order_by(Interview.scheduled_for.desc())
        ).all()

    def get_company_interviews(self, company_id: UUID) -> list[Interview]:
        return db.session.scalars(
            select(Interview)
            .join(Interview.application)
            .join(Application.placement_drive)
            .where(PlacementDrive.company_id == company_id)
            .order_by(Interview.scheduled_for.desc())
        ).all()
