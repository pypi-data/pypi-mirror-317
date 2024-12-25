from ._version import __version__  # noqa: I001
from .ql import (
    configure,
    executedf,
    execute,
    execute_debug,
    get_extension,
    list_extensions,
    register_extension,
    register_alias,
)

# Needed for extensions
from .datamodel.extension import IqlExtension
from .datamodel.subquery import SubQuery

from .datamodel.cache import QueryCacheBase

from .constants import get_cache, set_cache
from .jupyter_magics.iql_magic_ext import load_ipython_extension

__all__ = [
    "__version__",
    "configure",
    "executedf",
    "execute",
    "execute_debug",
    "get_extension",
    "list_extensions",
    "register_extension",
    "get_cache",
    "set_cache",
    "load_ipython_extension",
    "register_alias",
    "IqlExtension",
    "SubQuery",
    "QueryCacheBase",
]
