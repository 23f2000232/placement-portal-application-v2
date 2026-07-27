from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select, Select, or_, func

from app.enums import PlacementDriveStatus, PlacementDriveSortField, SortDirection
from app.extensions import db
from app.models.placement_drive import PlacementDrive
from app.repositories.base_repository import BaseRepository
from app.schemas.requests.placement.placement_drive_filter_request import (
    PlacementDriveFilterRequest,
)
from app.schemas.requests.placement.placement_drive_search_request import (
    PlacementDriveSearchRequest,
)
from app.schemas.requests.placement.placement_drive_sort_request import (
    PlacementDriveSortRequest,
)


class PlacementDriveRepository(BaseRepository[PlacementDrive]):

    _SORT_COLUMNS = {
        PlacementDriveSortField.TITLE: PlacementDrive.title,
        PlacementDriveSortField.SALARY_PACKAGE: PlacementDrive.salary_package,
        PlacementDriveSortField.CREATED_AT: PlacementDrive.created_at,
        PlacementDriveSortField.APPLICATION_DEADLINE: PlacementDrive.application_deadline,
    }

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

    def _apply_filters(
        self,
        query: Select,
        filters: PlacementDriveFilterRequest,
    ) -> Select:
        if filters.status is not None:
            query = query.where(
                PlacementDrive.status == filters.status,
            )

        if filters.job_type is not None:
            query = query.where(
                PlacementDrive.job_type == filters.job_type,
            )

        if filters.is_remote is not None:
            query = query.where(
                PlacementDrive.is_remote.is_(filters.is_remote),
            )

        return query

    def _apply_sorting(
        self,
        query: Select,
        sorting: PlacementDriveSortRequest,
    ) -> Select:
        column = self._SORT_COLUMNS[sorting.sort_by]

        if sorting.sort_direction == SortDirection.ASC:
            query = query.order_by(column.asc())
        else:
            query = query.order_by(column.desc())

        return query

    def _apply_search(
        self,
        query: Select,
        search: PlacementDriveSearchRequest,
    ) -> Select:
        if search.search:
            pattern = f"%{search.search}%"

            query = query.where(
                or_(
                    PlacementDrive.title.ilike(pattern),
                    PlacementDrive.job_location.ilike(pattern),
                )
            )

        return query

    def count(
        self,
        company_id: UUID,
        filters: PlacementDriveFilterRequest,
        search: PlacementDriveSearchRequest,
    ) -> int:
        query = (
            select(func.count())
            .select_from(PlacementDrive)
            .where(PlacementDrive.company_id == company_id)
        )

        query = self._apply_filters(
            query,
            filters,
        )

        query = self._apply_search(
            query,
            search,
        )

        return db.session.scalar(query) or 0

    def get_page(
        self,
        company_id: UUID,
        page: int,
        size: int,
        filters: PlacementDriveFilterRequest,
        sorting: PlacementDriveSortRequest,
        search: PlacementDriveSearchRequest,
    ) -> list[PlacementDrive]:
        offset = (page - 1) * size

        query = select(PlacementDrive).where(PlacementDrive.company_id == company_id)

        query = self._apply_filters(
            query,
            filters,
        )

        query = self._apply_search(
            query,
            search,
        )

        query = self._apply_sorting(
            query,
            sorting,
        )

        query = query.offset(offset).limit(size)

        return db.session.scalars(query).all()