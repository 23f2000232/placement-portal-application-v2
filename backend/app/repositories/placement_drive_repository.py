from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select

from app.enums import PlacementDriveStatus
from app.extensions import db
from app.models.placement_drive import PlacementDrive
from app.repositories.base_repository import BaseRepository


class PlacementDriveRepository(BaseRepository[PlacementDrive]):
    def __init__(self):
        super().__init__(PlacementDrive)

    def get_by_company_id(
        self,
        company_id: UUID,
    ) -> list[PlacementDrive]:
        return db.session.scalars(
            select(PlacementDrive).where(PlacementDrive.company_id == company_id)
        ).all()

    def get_by_status(
        self,
        status: PlacementDriveStatus,
    ) -> list[PlacementDrive]:
        return db.session.scalars(
            select(PlacementDrive).where(PlacementDrive.status == status)
        ).all()

    def get_active_drives(self) -> list[PlacementDrive]:
        return db.session.scalars(
            select(PlacementDrive).where(
                PlacementDrive.status == PlacementDriveStatus.OPEN,
                PlacementDrive.application_deadline >= datetime.now(timezone.utc),
            )
        ).all()