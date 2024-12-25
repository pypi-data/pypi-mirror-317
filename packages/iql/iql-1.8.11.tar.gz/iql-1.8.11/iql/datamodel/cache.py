from dataclasses import dataclass, field


@dataclass
class QueryCacheBase:
    """Simple cache that ignores any policy settings"""

    _cache: dict = field(default_factory=dict, init=True)

    def save(self, key: str, data: object, prefix: str = "default", policy: dict = None):
        self._cache[key] = data

    def get(self, key: str, prefix: str = "default", policy: dict = None) -> object:
        return self._cache.get(key, None)

    def clear(
        self,
        key: str,
        prefix: str = "default",
    ):
        del self._cache[key]

    def clear_all(self):
        self._cache = {}

    def cache_size(self) -> int:
        """Returns number of items in cache"""
        return len(self._cache)
