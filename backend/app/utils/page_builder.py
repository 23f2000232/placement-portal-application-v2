from collections.abc import Callable
from typing import TypeVar

from app.schemas.response.common.page_response import PageResponse
from app.utils.pagination import calculate_total_pages

T = TypeVar("T")
R = TypeVar("R")


def build_page_response(
    *,
    items: list[T],
    mapper: Callable[[T], R],
    page: int,
    size: int,
    total_items: int,
) -> PageResponse[R]:
    return PageResponse(
        items=[mapper(item) for item in items],
        page=page,
        size=size,
        total_items=total_items,
        total_pages=calculate_total_pages(
            total_items,
            size,
        ),
    )