from typing import Dict

from .datamodel.cache import QueryCacheBase

default_cache_policy_toplevel = {
    "max_age": 3600,
    "s3": False,
    "fcache": False,
    "memory": False,
}

default_cache_policies_keywords = {
    "bql": {"max_age": 3600, "fcache": True, "memory": True},
    "s3": {"max_age": None, "fcache": True, "memory": False},
    "sklearn": {"max_age": None, "fcache": True, "memory": True},
}


# Add extensions via register_extension()
# Extensions are loaded on first access, to avoid requiring
# unused dependencies

_KNOWN_EXTENSIONS: Dict[str, str] = {
    "bql": "iql.extensions.bql_ext.bql_extension",
    "pandas": "iql.extensions.pandas_extension",
    "cache": "iql.extensions.cache_extension",
    "blpapi": "iql.extensions.blpapi_ext.blp_extension",
}

_LOADED_EXTENSIONS = []

_CACHE = QueryCacheBase()


def get_cache():
    return _CACHE


def set_cache(cache: QueryCacheBase):
    global _CACHE
    _CACHE = cache
