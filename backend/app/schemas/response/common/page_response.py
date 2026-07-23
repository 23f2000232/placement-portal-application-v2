from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class PageResponse(BaseModel, Generic[T]):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    items: list[T]

    page: int

    size: int

    total_items: int

    total_pages: int