def pick(
    data: dict[str, str],
    *keys: str,
) -> dict[str, str]:
    return {key: data[key] for key in keys if key in data}