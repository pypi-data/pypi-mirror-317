import json
import logging
from dataclasses import dataclass
from typing import Optional

import pandas as pd

from ..constants import get_cache
from ..datamodel.extension import IqlExtension
from ..datamodel.subquery import SubQuery
from ..ql import register_extension

logger = logging.getLogger(__name__)


@dataclass
class CacheClearAll(IqlExtension):
    """Clears the entire cache"""

    keyword: str

    def executeimpl(self, sq: SubQuery) -> pd.DataFrame:
        get_cache().clear_all()

        return pd.DataFrame([{"result:": True}])


@dataclass
class CacheClear(IqlExtension):
    """Clears a single item from the cache"""

    keyword: str

    def executeimpl(self, sq: SubQuery) -> pd.DataFrame:
        key: str = sq.options["key"]  # type: ignore

        prefix: str = sq.options.get("prefix", "default")  # type: ignore
        get_cache().clear(key, prefix)

        return pd.DataFrame([{"result:": True}])


@dataclass
class CacheGet(IqlExtension):
    """Gets a single item from the cache"""

    keyword: str

    def executeimpl(self, sq: SubQuery) -> pd.DataFrame:
        key = sq.options["key"]
        prefix = sq.options.get("prefix", "default")
        policy = json.loads(sq.options["policy"]) if "policy" in sq.options else None  # type: ignore

        cached_df: pd.DataFrame = get_cache().get(key, prefix, policy)  # type: ignore
        return cached_df


@dataclass
class CachePut(IqlExtension):
    """Clears a single item from the cache"""

    keyword: str

    def executeimpl(self, sq: SubQuery) -> pd.DataFrame:
        prefix = "default"
        data: Optional[pd.DataFrame] = None

        query = sq.options["query"]
        key = sq.options["key"]

        if "prefix" in sq.options:
            prefix = sq.options["prefix"]

        data = sq.iqc.db.execute_query(query, context=sq.iqc.context)  # type: ignore

        if "policy" in sq.options:
            policy = json.loads(sq.options["policy"])  # type: ignore
        else:
            policy = None

        get_cache().save(key, data, prefix, policy)  # type: ignore
        return pd.DataFrame([{"result:": True}])


def register(keyword):
    register_extension(CacheClearAll(keyword=keyword, subword="clear_all"))
    register_extension(CacheClear(keyword=keyword, subword="clear"))
    register_extension(CacheGet(keyword=keyword, subword="get"))
    register_extension(CachePut(keyword=keyword, subword="put"))
