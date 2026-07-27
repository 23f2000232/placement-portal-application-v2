from uuid import UUID

from sqlalchemy import select, exists, func, Select, or_

from app import Company, PlacementDrive, Student
from app.enums import ApplicationStatus, StudentApplicationSortField, SortDirection
from app.extensions import db
from app.models.application import Application
from app.repositories.base_repository import BaseRepository
from app.schemas.requests.student.student_application_filter_request import (
    StudentApplicationFilterRequest,
)
from app.schemas.requests.student.student_application_search_request import (
    StudentApplicationSearchRequest,
)
from app.schemas.requests.student.student_application_sort_request import (
    StudentApplicationSortRequest,
)


class ApplicationRepository(BaseRepository[Application]):

    _STUDENT_SORT_COLUMNS = {
        StudentApplicationSortField.APPLIED_AT: Application.created_at,
        StudentApplicationSortField.STATUS: Application.status,
        StudentApplicationSortField.COMPANY_NAME: Company.company_name,
        StudentApplicationSortField.JOB_TITLE: PlacementDrive.title,
        StudentApplicationSortField.SALARY_PACKAGE: PlacementDrive.salary_package,
    }

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

    def _apply_student_filters(
        self,
        query: Select,
        filters: StudentApplicationFilterRequest,
    ) -> Select:
        if filters.status is not None:
            query = query.where(
                Application.status == filters.status,
            )

        return query

    def _apply_student_search(
        self,
        query: Select,
        search: StudentApplicationSearchRequest,
    ) -> Select:
        if search.search:
            pattern = f"%{search.search}%"

            query = query.where(
                or_(
                    Company.company_name.ilike(pattern),
                    PlacementDrive.title.ilike(pattern),
                    PlacementDrive.job_location.ilike(pattern),
                )
            )

        return query

    def _apply_student_sorting(
        self,
        query: Select,
        sorting: StudentApplicationSortRequest,
    ) -> Select:
        column = self._STUDENT_SORT_COLUMNS[sorting.sort_by]

        if sorting.sort_direction == SortDirection.ASC:
            query = query.order_by(column.asc())
        else:
            query = query.order_by(column.desc())

        return query

    def _build_student_applications_query(
        self,
        student: Student,
    ) -> Select:
        return (
            select(Application)
            .join(PlacementDrive)
            .join(Company)
            .where(
                Application.student_id == student.id,
            )
        )

    def count_student_applications(
        self,
        student: Student,
        filters: StudentApplicationFilterRequest,
        search: StudentApplicationSearchRequest,
    ) -> int:
        query = self._build_student_applications_query(
            student,
        )

        query = query.with_only_columns(
            func.count(),
        )

        query = self._apply_student_filters(
            query,
            filters,
        )

        query = self._apply_student_search(
            query,
            search,
        )

        return db.session.scalar(query) or 0

    def get_student_applications_page(
        self,
        student: Student,
        page: int,
        size: int,
        filters: StudentApplicationFilterRequest,
        sorting: StudentApplicationSortRequest,
        search: StudentApplicationSearchRequest,
    ) -> list[Application]:
        offset = (page - 1) * size

        query = self._build_student_applications_query(
            student,
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

    def get_by_student_and_id(
        self,
        student_id: UUID,
        application_id: UUID,
    ) -> Application | None:
        return db.session.scalar(
            select(Application).where(
                Application.id == application_id,
                Application.student_id == student_id,
            )
        )