import logging
from dataclasses import dataclass
from typing import Iterable

import pandas as pd

from ..datamodel.database import IqlDatabase
from ..datamodel.extension import IqlExtension
from ..datamodel.result import IqlResult, IqlResultData
from ..datamodel.subquery import SubQuery
from ..ql import register_extension

logger = logging.getLogger(__name__)


def get_data(sq: SubQuery, source_query) -> pd.DataFrame:
    db: IqlDatabase = sq.iqc.db  # type: ignore
    local_results: Iterable[IqlResult] = [IqlResultData(_data=ldf, name=k, query=k) for k, ldf in sq.local_dfs]

    result = db.execute_query(  # type: ignore
        query=source_query, completed_results=local_results, context=sq.iqc.context
    )
    if result is None:
        raise ValueError(f"Could not get data for query {source_query}")
    else:
        return result.df_numpy()  # type: ignore


def get_query_from_options(options) -> str:
    sql = options.get("sql")
    if sql is not None:
        return sql

    dfname = options.get("df")
    tablename = options.get("table")

    if dfname is not None:
        return f"select * from {dfname}"
    elif tablename is not None:
        return f"select * from {tablename}"

    dataname = options.get("data")
    if dataname is not None:
        if " " in dataname:
            return dataname
        else:
            return f"select * from {dataname}"

    raise ValueError("df, table, sql and data are not specified")


@dataclass
class PandasExtension(IqlExtension):
    keyword: str

    def allow_cache_read(self, sq: SubQuery) -> bool:
        # Never cache, because this depends on contents of table
        return False

    def allow_cache_save(self, sq: SubQuery) -> bool:
        return False

    def executeimpl(self, sq: SubQuery) -> pd.DataFrame:
        query = get_query_from_options(sq.options)

        return get_data(sq, query)


@dataclass
class PandasTransposeExtension(IqlExtension):
    keyword: str

    def allow_cache_read(self, sq: SubQuery) -> bool:
        # Never cache, because this depends on contents of table
        return False

    def allow_cache_save(self, sq: SubQuery) -> bool:
        return False

    def executeimpl(self, sq: SubQuery) -> pd.DataFrame:
        query = get_query_from_options(sq.options)

        result_df = get_data(sq, query)
        cols = sq.options["columns"]
        rows = sq.options["rows"]

        melt_cols = []

        if isinstance(cols, list):
            melt_cols += cols
        elif cols is not None:
            melt_cols.append(cols)

        if isinstance(rows, list):
            melt_cols += rows
        elif isinstance(rows, str):  # str
            melt_cols.append(rows)
            rows = [rows]
        else:
            raise ValueError(f"Unexpected type for rows: {type(rows)}")

        rows.append("name")

        logger.debug(
            "Melting table and repivoting: cols=%s, rows=%s, melt_cols=%s",
            cols,
            rows,
            melt_cols,
        )
        melted_df = (
            result_df.melt(melt_cols, var_name="name")  # noqa
            .pivot(index=rows, columns=cols, values="value")
            .reset_index()
        )
        return melted_df


def register(keyword: str):
    extension = PandasExtension(keyword=keyword)
    register_extension(extension)

    extension = PandasExtension(keyword=keyword, subword="pivot")
    register_extension(extension)

    extension = PandasTransposeExtension(keyword=keyword, subword="transpose")
    register_extension(extension)
