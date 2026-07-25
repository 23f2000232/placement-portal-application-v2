from uuid import UUID

from sqlalchemy import select, Select, or_, func

from app.enums import ApprovalStatus, StudentSortField, SortDirection
from app.extensions import db
from app.models.student import Student
from app.repositories.base_repository import BaseRepository
from app.schemas.requests import (
    StudentFilterRequest,
    StudentSearchRequest,
    StudentSortRequest,
)


class StudentRepository(BaseRepository[Student]):
    def __init__(self):
        super().__init__(Student)

    _SORT_COLUMNS = {
        StudentSortField.CREATED_AT: Student.created_at,
        StudentSortField.FULL_NAME: Student.full_name,
        StudentSortField.ROLL_NUMBER: Student.roll_number,
        StudentSortField.CGPA: Student.cgpa,
        StudentSortField.SEMESTER: Student.semester,
    }

    def get_by_user_id(self, user_id: UUID) -> Student | None:
        return db.session.scalar(select(Student).where(Student.user_id == user_id))

    def get_by_approval_status(
        self,
        status: ApprovalStatus,
    ) -> list[Student]:
        return db.session.scalars(
            select(Student).where(Student.approval_status == status)
        ).all()

    def _apply_filters(
        self,
        query: Select,
        filters: StudentFilterRequest,
    ) -> Select:

        if filters.approval_status is not None:
            query = query.where(Student.approval_status == filters.approval_status)

        if filters.branch is not None:
            query = query.where(Student.branch == filters.branch)

        if filters.semester is not None:
            query = query.where(Student.semester == filters.semester)

        return query

    def _apply_search(
        self,
        query: Select,
        search: StudentSearchRequest,
    ) -> Select:

        if search.search:
            query = query.where(
                or_(
                    Student.full_name.ilike(f"%{search.search}%"),
                    Student.roll_number.ilike(f"%{search.search}%"),
                    Student.phone_number.ilike(f"%{search.search}%"),
                )
            )

        return query

    def _apply_sorting(
        self,
        query: Select,
        sorting: StudentSortRequest,
    ) -> Select:

        column = self._SORT_COLUMNS[sorting.sort_by]

        if sorting.sort_direction == SortDirection.ASC:
            query = query.order_by(column.asc())
        else:
            query = query.order_by(column.desc())

        return query

    def count(
        self,
        filters: StudentFilterRequest,
        search: StudentSearchRequest,
    ) -> int:

        query = select(func.count()).select_from(Student)

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
        page: int,
        size: int,
        filters: StudentFilterRequest,
        sorting: StudentSortRequest,
        search: StudentSearchRequest,
    ) -> list[Student]:

        offset = (page - 1) * size

        query = select(Student)

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