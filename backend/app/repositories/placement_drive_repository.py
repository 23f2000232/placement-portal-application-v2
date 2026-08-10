from datetime import datetime, timezone, UTC
from uuid import UUID

from sqlalchemy import select, Select, or_, func, exists

from app import Company, Student, Application
from app.enums import (
    PlacementDriveStatus,
    PlacementDriveSortField,
    SortDirection,
    StudentDriveSortField,
)
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
from app.schemas.requests.student.student_drive_filter_request import (
    StudentDriveFilterRequest,
)
from app.schemas.requests.student.student_drive_search_request import (
    StudentDriveSearchRequest,
)
from app.schemas.requests.student.student_drive_sort_request import (
    StudentDriveSortRequest,
)


class PlacementDriveRepository(BaseRepository[PlacementDrive]):

    _STUDENT_SORT_COLUMNS = {
        StudentDriveSortField.APPLICATION_DEADLINE: PlacementDrive.application_deadline,
        StudentDriveSortField.SALARY_PACKAGE: PlacementDrive.salary_package,
        StudentDriveSortField.TITLE: PlacementDrive.title,
        StudentDriveSortField.COMPANY_NAME: Company.company_name,
    }

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
                    Company.company_name.ilike(pattern),
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
            .join(Company)
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

    def count_all(
        self,
        filters: PlacementDriveFilterRequest,
        search: PlacementDriveSearchRequest,
    ) -> int:
        query = select(func.count()).select_from(PlacementDrive).join(Company)
        query = self._apply_filters(query, filters)
        query = self._apply_search(query, search)
        return db.session.scalar(query) or 0

    def get_all_page(
        self,
        page: int,
        size: int,
        filters: PlacementDriveFilterRequest,
        sorting: PlacementDriveSortRequest,
        search: PlacementDriveSearchRequest,
    ) -> list[PlacementDrive]:
        query = select(PlacementDrive).join(Company)
        query = self._apply_filters(query, filters)
        query = self._apply_search(query, search)
        query = self._apply_sorting(query, sorting)
        return db.session.scalars(query.offset((page - 1) * size).limit(size)).all()

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

        query = select(PlacementDrive).join(Company).where(PlacementDrive.company_id == company_id)

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

    def _apply_student_filters(
        self,
        query: Select,
        filters: StudentDriveFilterRequest,
    ) -> Select:
        if filters.job_type is not None:
            query = query.where(
                PlacementDrive.job_type == filters.job_type,
            )

        if filters.is_remote is not None:
            query = query.where(
                PlacementDrive.is_remote.is_(filters.is_remote),
            )

        return query

    def _apply_student_sorting(
        self,
        query: Select,
        sorting: StudentDriveSortRequest,
    ) -> Select:
        column = self._STUDENT_SORT_COLUMNS[sorting.sort_by]

        if sorting.sort_direction == SortDirection.ASC:
            query = query.order_by(column.asc())
        else:
            query = query.order_by(column.desc())

        return query

    def _apply_student_search(
        self,
        query: Select,
        search: StudentDriveSearchRequest,
    ) -> Select:
        if search.search:
            pattern = f"%{search.search}%"

            query = query.where(
                or_(
                    PlacementDrive.title.ilike(pattern),
                    PlacementDrive.job_location.ilike(pattern),
                    Company.company_name.ilike(pattern),
                )
            )

        return query

    def _build_available_drives_query(
        self,
        student: Student,
        *,
        exclude_applied: bool = True,
    ) -> Select:
        query = select(PlacementDrive).join(Company)

        query = query.where(
            PlacementDrive.status == PlacementDriveStatus.OPEN,
            PlacementDrive.application_deadline > datetime.now(UTC),
            PlacementDrive.minimum_cgpa <= student.cgpa,
            PlacementDrive.maximum_backlogs >= student.current_backlogs,
        )

        query = query.where(
            PlacementDrive.eligible_branches.contains(
                student.branch,
            )
        )

        if exclude_applied:
            query = query.where(
                ~exists().where(
                    Application.student_id == student.id,
                    Application.placement_drive_id == PlacementDrive.id,
                )
            )

        return query

    def count_available_drives(
        self,
        student: Student,
        filters: StudentDriveFilterRequest,
        search: StudentDriveSearchRequest,
    ) -> int:

        query = self._build_available_drives_query(
            student,
            exclude_applied=True,
        )

        query = query.with_only_columns(func.count())

        query = self._apply_student_filters(
            query,
            filters,
        )

        query = self._apply_student_search(
            query,
            search,
        )

        return db.session.scalar(query) or 0

    def get_available_drives_page(
        self,
        student: Student,
        page: int,
        size: int,
        filters: StudentDriveFilterRequest,
        sorting: StudentDriveSortRequest,
        search: StudentDriveSearchRequest,
    ) -> list[PlacementDrive]:

        offset = (page - 1) * size

        query = self._build_available_drives_query(
            student,
            exclude_applied=True,
        )

        query = self._apply_student_filters(
            query,
            filters,
        )

        query = self._apply_student_search(
            query,
            search,
        )

        query = self._apply_student_sorting(
            query,
            sorting,
        )

        query = query.offset(offset).limit(size)

        return db.session.scalars(query).all()

    def get_available_drive(
        self,
        student: Student,
        drive_id: UUID,
    ) -> PlacementDrive | None:
        query = self._build_available_drives_query(
            student,
            exclude_applied=True,
        )

        query = query.where(
            PlacementDrive.id == drive_id,
        )

        return db.session.scalar(query)

    def get_drive_for_application(
        self,
        student: Student,
        drive_id: UUID,
    ) -> PlacementDrive | None:
        query = self._build_available_drives_query(
            student,
            exclude_applied=False,
        )

        query = query.where(
            PlacementDrive.id == drive_id,
        )

        return db.session.scalar(query)
