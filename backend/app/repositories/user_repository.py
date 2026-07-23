from sqlalchemy import select, Select, func

from app.enums import UserRole, AccountStatus, SortDirection, UserSortField
from app.extensions import db
from app.models.user import User
from app.repositories.base_repository import BaseRepository
from app.schemas.requests import UserSearchRequest
from app.schemas.requests.user_filter_request import UserFilterRequest
from app.schemas.requests.user_sort_request import UserSortRequest


class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    _SORT_COLUMNS = {
        UserSortField.EMAIL: User.email,
        UserSortField.ROLE: User.role,
        UserSortField.ACCOUNT_STATUS: User.account_status,
        UserSortField.CREATED_AT: User.created_at,
    }

    def get_by_email(self, email: str) -> User | None:
        return db.session.scalar(select(User).where(User.email == email))

    def exists_by_email(self, email: str) -> bool:
        return self.get_by_email(email) is not None

    def get_by_role(self, role: UserRole) -> list[User]:
        return db.session.scalars(select(User).where(User.role == role)).all()

    def get_active_users(self, active: bool = True) -> list[User]:
        return db.session.scalars(select(User).where(User.is_active.is_(active))).all()

    def get_by_account_status(
        self,
        status: AccountStatus,
    ) -> list[User]:
        return db.session.scalars(
            select(User).where(User.account_status == status)
        ).all()

    def _apply_filters(
        self,
        query: Select,
        filters: UserFilterRequest,
    ) -> Select:
        if filters.role is not None:
            query = query.where(User.role == filters.role)

        if filters.account_status is not None:
            query = query.where(User.account_status == filters.account_status)

        if filters.is_active is not None:
            query = query.where(User.is_active.is_(filters.is_active))

        return query

    def get_page(
        self,
        page: int,
        size: int,
        filters: UserFilterRequest,
        sorting: UserSortRequest,
        search: UserSearchRequest,
    ) -> list[User]:
        offset = (page - 1) * size

        query = select(User)
        query = self._apply_filters(query, filters)
        query = self._apply_search(query, search)
        query = self._apply_sorting(
            query,
            sorting,
        )

        # query = query.order_by(User.created_at.desc()).offset(offset).limit(size)
        query = query.offset(offset).limit(size)
        return db.session.scalars(query).all()

    def count(
        self,
        filters: UserFilterRequest,
    ) -> int:
        query = select(func.count()).select_from(User)
        query = self._apply_filters(query, filters)

        return db.session.scalar(query) or 0

    def _apply_sorting(
        self,
        query: Select,
        sorting: UserSortRequest,
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
        search: UserSearchRequest,
    ) -> Select:
        if search.search:
            query = query.where(User.email.ilike(f"%{search.search}%"))

        return query