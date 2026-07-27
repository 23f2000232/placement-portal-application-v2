from uuid import UUID

from sqlalchemy import select, exists

from app.enums import ApplicationStatus
from app.extensions import db
from app.models.application import Application
from app.repositories.base_repository import BaseRepository


class ApplicationRepository(BaseRepository[Application]):
    def __init__(self):
        super().__init__(Application)

    def get_by_student_id(
        self,
        student_id: UUID,
    ) -> list[Application]:
        return db.session.scalars(
            select(Application).where(Application.student_id == student_id)
        ).all()

    def get_by_placement_drive_id(
        self,
        placement_drive_id: UUID,
    ) -> list[Application]:
        return db.session.scalars(
            select(Application).where(
                Application.placement_drive_id == placement_drive_id
            )
        ).all()

    def get_by_student_and_drive(
        self,
        student_id: UUID,
        placement_drive_id: UUID,
    ) -> Application | None:
        return db.session.scalar(
            select(Application).where(
                Application.student_id == student_id,
                Application.placement_drive_id == placement_drive_id,
            )
        )

    def get_by_status(
        self,
        status: ApplicationStatus,
    ) -> list[Application]:
        return db.session.scalars(
            select(Application).where(Application.status == status)
        ).all()

    def exists_by_student_and_drive(
        self,
        student_id: UUID,
        drive_id: UUID,
    ) -> bool:
        return (
            db.session.scalar(
                select(
                    exists().where(
                        Application.student_id == student_id,
                        Application.placement_drive_id == drive_id,
                    )
                )
            )
            or False
        )