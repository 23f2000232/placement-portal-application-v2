from math import ceil


def calculate_total_pages(
    total_items: int,
    size: int,
) -> int:
    return ceil(total_items / size) if total_items else 0