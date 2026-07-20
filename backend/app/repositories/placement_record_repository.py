from uuid import UUID

from sqlalchemy import select

from app.enums import PlacementStatus
from app.extensions import db
from app.models.placement_record import PlacementRecord
from app.repositories.base_repository import BaseRepository


class PlacementRecordRepository(BaseRepository[PlacementRecord]):
    def __init__(self):
        super().__init__(PlacementRecord)

    def get_by_application_id(
        self,
        application_id: UUID,
    ) -> PlacementRecord | None:
        return db.session.scalar(
            select(PlacementRecord).where(
                PlacementRecord.application_id == application_id
            )
        )

    def get_by_status(
        self,
        status: PlacementStatus,
    ) -> list[PlacementRecord]:
        return db.session.scalars(
            select(PlacementRecord).where(PlacementRecord.status == status)
        ).all()

    def get_all_placed(self) -> list[PlacementRecord]:
        return self.get_by_status(PlacementStatus.PLACED)