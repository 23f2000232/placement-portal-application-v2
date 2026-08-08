from threading import Lock
from time import monotonic
from typing import Any


class TTLCache:
    """Small thread-safe in-process cache for read-heavy response payloads."""

    def __init__(self, ttl_seconds: int):
        self.ttl_seconds = ttl_seconds
        self._entries: dict[str, tuple[float, Any]] = {}
        self._lock = Lock()

    def get(self, key: str) -> Any | None:
        with self._lock:
            item = self._entries.get(key)
            if item is None or item[0] <= monotonic():
                self._entries.pop(key, None)
                return None
            return item[1]

    def set(self, key: str, value: Any) -> Any:
        with self._lock:
            self._entries[key] = (monotonic() + self.ttl_seconds, value)
        return value

    def invalidate(self, key: str | None = None) -> None:
        with self._lock:
            if key is None:
                self._entries.clear()
            else:
                self._entries.pop(key, None)
