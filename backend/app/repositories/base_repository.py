from typing import Generic, TypeVar
from uuid import UUID

from sqlalchemy import select, func

from app.extensions import db

T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, model: type[T]):
        self.model = model

    def create(self, entity: T) -> T:
        db.session.add(entity)
        return entity

    def get_by_id(self, entity_id: UUID) -> T | None:
        return db.session.get(self.model, entity_id)

    def get_all(self) -> list[T]:
        return db.session.scalars(select(self.model)).all()

    def delete(self, entity: T) -> None:
        db.session.delete(entity)

    def exists(self, entity_id: UUID) -> bool:
        return self.get_by_id(entity_id) is not None

    def save(self) -> None:
        db.session.commit()

    def rollback(self) -> None:
        db.session.rollback()

    def count(self):
        return db.session.scalar(select(func.count()).select_from(self.model))

    def get_page(
        self,
        page: int,
        size: int,
    ) -> list[T]:
        offset = (page - 1) * size

        return db.session.scalars(
            select(self.model)
            .order_by(self.model.created_at.desc())
            .offset(offset)
            .limit(size)
        ).all()