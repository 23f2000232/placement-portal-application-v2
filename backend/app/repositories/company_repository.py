from uuid import UUID

from sqlalchemy import select, Select, or_, func

from app.enums import ApprovalStatus, CompanySortField, SortDirection
from app.extensions import db
from app.models.company import Company
from app.repositories.base_repository import BaseRepository
from app.schemas.requests.company_filter_request import CompanyFilterRequest
from app.schemas.requests.company_search_request import CompanySearchRequest
from app.schemas.requests.company_sort_request import CompanySortRequest


class CompanyRepository(BaseRepository[Company]):
    def __init__(self):
        super().__init__(Company)

    _SORT_COLUMNS = {
        CompanySortField.CREATED_AT: Company.created_at,
        CompanySortField.COMPANY_NAME: Company.company_name,
        CompanySortField.INDUSTRY: Company.industry,
        CompanySortField.CONTACT_PERSON: Company.contact_person,
    }

    def get_by_user_id(
        self,
        user_id: UUID,
    ) -> Company | None:
        return db.session.scalar(select(Company).where(Company.user_id == user_id))

    def get_by_approval_status(
        self,
        status: ApprovalStatus,
    ) -> list[Company]:
        return db.session.scalars(
            select(Company).where(Company.approval_status == status)
        ).all()

    def _apply_filters(
        self,
        query: Select,
        filters: CompanyFilterRequest,
    ) -> Select:

        if filters.approval_status is not None:
            query = query.where(Company.approval_status == filters.approval_status)

        if filters.industry is not None:
            query = query.where(Company.industry == filters.industry)

        return query

    def _apply_search(
        self,
        query: Select,
        search: CompanySearchRequest,
    ) -> Select:

        if search.search:
            query = query.where(
                or_(
                    Company.company_name.ilike(f"%{search.search}%"),
                    Company.contact_person.ilike(f"%{search.search}%"),
                    Company.contact_email.ilike(f"%{search.search}%"),
                )
            )

        return query

    def _apply_sorting(
        self,
        query: Select,
        sorting: CompanySortRequest,
    ) -> Select:

        column = self._SORT_COLUMNS[sorting.sort_by]

        if sorting.sort_direction == SortDirection.ASC:
            query = query.order_by(column.asc())
        else:
            query = query.order_by(column.desc())

        return query

    def count(
        self,
        filters: CompanyFilterRequest,
        search: CompanySearchRequest,
    ) -> int:

        query = select(func.count()).select_from(Company)

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
        filters: CompanyFilterRequest,
        sorting: CompanySortRequest,
        search: CompanySearchRequest,
    ) -> list[Company]:

        offset = (page - 1) * size

        query = select(Company)

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