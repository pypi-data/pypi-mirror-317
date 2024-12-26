#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
# Copyright (c) 2023-2024 Yunqi Inc. All rights reserved.
#

from __future__ import annotations

import collections.abc
import os
import warnings
from logging import getLogger
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING, Any, Iterator, Literal, TypeVar

from clickzetta.connector.v0.exceptions import ProgrammingError
from clickzetta.connector.v0.query_result import QueryResult
from clickzetta.zettapark._connector import pandas
from clickzetta.zettapark._internal.pandas_util import (
    _extract_schema_and_data_from_pandas_df,
)
from clickzetta.zettapark._internal.type_utils import convert_data_type_to_name
from clickzetta.zettapark._internal.utils import quote_name

if TYPE_CHECKING:  # pragma: no cover
    from clickzetta.zettapark._internal.server_connection import ServerConnection

    try:
        import sqlalchemy
    except ImportError:
        sqlalchemy = None

T = TypeVar("T", bound=collections.abc.Sequence)

logger = getLogger(__name__)


def chunk_helper(
    lst: pandas.DataFrame, n: int
) -> Iterator[tuple[int, pandas.DataFrame]]:
    """Helper generator to chunk a sequence efficiently with current index like if enumerate was called on sequence."""
    if len(lst) == 0:
        yield 0, lst
        return
    for i in range(0, len(lst), n):
        yield int(i / n), lst.iloc[i : i + n]


def build_location_helper(
    database: str | None, schema: str | None, name: str, quote_identifiers: bool
) -> str:
    """Helper to format table/volume/file format's location."""
    if quote_identifiers:
        location = (
            (("`" + database + "`.") if database else "")
            + (("`" + schema + "`.") if schema else "")
            + ("`" + name + "`")
        )
    else:
        location = (
            (database + "." if database else "")
            + (schema + "." if schema else "")
            + name
        )
    return location


def _write_pandas(
    conn: ServerConnection,
    df: pandas.DataFrame,
    table_name: str,
    database: str | None = None,
    schema: str | None = None,
    chunk_size: int | None = None,
    compression: str = "gzip",
    on_error: str = "abort_statement",
    parallel: int = 4,
    quote_identifiers: bool = True,
    auto_create_table: bool = False,
    create_temp_table: bool = False,
    overwrite: bool = False,
    table_type: Literal["", "temp", "temporary", "transient"] = "",
    use_logical_type: bool | None = None,
    **kwargs: Any,
) -> tuple[bool, str]:
    """Allows users to most efficiently write back a pandas DataFrame to Clickzetta.

    It works by dumping the DataFrame into Parquet files, uploading them and finally copying their data into the table.

    Returns whether all files were ingested correctly, number of chunks uploaded, and number of rows ingested
    with all of the COPY INTO command's output for debugging purposes.

        Example usage:
            import pandas

            df = pandas.DataFrame([('Mark', 10), ('Luke', 20)], columns=['name', 'balance'])

    Args:
        conn: Connection to be used to communicate with Clickzetta.
        df: Dataframe we'd like to write back.
        table_name: Table name where we want to insert into.
        database: Database schema and table is in, if not provided the default one will be used (Default value = None).
        schema: Schema table is in, if not provided the default one will be used (Default value = None).
        chunk_size: Number of elements to be inserted once, if not provided all elements will be dumped once
            (Default value = None).
        compression: The compression used on the Parquet files, can only be gzip, or snappy. Gzip gives supposedly a
            better compression, while snappy is faster. Use whichever is more appropriate (Default value = 'gzip').
        on_error: Action to take when COPY INTO statements fail, default follows documentation at:
            https://doc.clickzetta.com/
            (Default value = 'abort_statement').
        parallel: Number of threads to be used when uploading chunks, default follows documentation at:
            https://doc.clickzetta.com/ (Default value = 4).
        quote_identifiers: By default, identifiers, specifically database, schema, table and column names
            (from df.columns) will be quoted. If set to False, identifiers are passed on to Clickzetta without quoting.
            I.e. identifiers will be coerced to uppercase by Clickzetta.  (Default value = True)
        auto_create_table: When true, will automatically create a table with corresponding columns for each column in
            the passed in DataFrame. The table will not be created if it already exists
        create_temp_table: (Deprecated) Will make the auto-created table as a temporary table
        overwrite: When true, and if auto_create_table is true, then it drops the table. Otherwise, it
        truncates the table. In both cases it will replace the existing contents of the table with that of the passed in
            Pandas DataFrame.
        table_type: The table type of to-be-created table. The supported table types include ``temp``/``temporary``
            and ``transient``. Empty means permanent table as per SQL convention.
        use_logical_type: Boolean that specifies whether to use Parquet logical types. With this file format option,
            Clickzetta can interpret Parquet logical types during data loading. To enable Parquet logical types,
            set use_logical_type as True. Set to None to use Clickzetta default. For more information, see:
            https://doc.clickzetta.com/


    Returns:
        Returns the COPY INTO command's results to verify ingestion in the form of a tuple of whether all chunks were
        ingested correctly, # of chunks, # of ingested rows, and ingest's output.
    """
    if database is not None and schema is None:
        raise ProgrammingError(
            "Schema has to be provided to write_pandas when a database is provided"
        )
    # This dictionary maps the compression algorithm to Clickzetta put copy into command type
    # https://doc.clickzetta.com/
    compression_map = {"gzip": "auto", "snappy": "snappy"}
    if compression not in compression_map.keys():
        raise ProgrammingError(
            f"Invalid compression '{compression}', only acceptable values are: {compression_map.keys()}"
        )

    if create_temp_table:
        warnings.warn(
            "create_temp_table is deprecated, we still respect this parameter when it is True but "
            'please consider using `table_type="temp"` instead',
            DeprecationWarning,
            # warnings.warn -> write_pandas
            stacklevel=2,
        )
        table_type = "temp"

    if table_type and table_type.lower() not in ["temp", "temporary", "transient"]:
        raise ValueError(
            "Unsupported table type. Expected table types: temp/temporary, transient"
        )

    if chunk_size is None:
        chunk_size = len(df)

    if not (
        isinstance(df.index, pandas.RangeIndex)
        and 1 == df.index.step
        and 0 == df.index.start
    ):
        warnings.warn(
            f"Pandas Dataframe has non-standard index of type {str(type(df.index))} which will not be written."
            f" Consider changing the index to pd.RangeIndex(start=0,...,step=1) or "
            f"call reset_index() to keep index as column(s)",
            UserWarning,
            stacklevel=2,
        )

    # use_logical_type should be True when dataframe contains datetimes with timezone.
    # if not use_logical_type and any(
    #     [pandas.api.types.is_datetime64tz_dtype(df[c]) for c in df.columns]
    # ):
    #     warnings.warn(
    #         "Dataframe contains a datetime with timezone column, but "
    #         f"'{use_logical_type=}'. This can result in dateimes "
    #         "being incorrectly written to Clickzetta. Consider setting "
    #         "'use_logical_type = True'",
    #         UserWarning,
    #         stacklevel=2,
    #     )

    # if use_logical_type is None:
    #     sql_use_logical_type = ""
    # elif use_logical_type:
    #     sql_use_logical_type = " USE_LOGICAL_TYPE = TRUE"
    # else:
    #     sql_use_logical_type = " USE_LOGICAL_TYPE = FALSE"

    # get pandas dataframe schema.
    table_schema, _ = _extract_schema_and_data_from_pandas_df(df)

    cursor = conn.cursor()

    # volume_path use user volume instead.
    volume_path = " USER VOLUME "

    import uuid

    volume_dir = str(uuid.uuid1()).replace("-", "_")

    with TemporaryDirectory() as tmp_folder:
        for i, chunk in chunk_helper(df, chunk_size):
            chunk_path = os.path.join(tmp_folder, f"file{i}.txt")
            # Dump chunk into parquet file
            chunk.to_parquet(chunk_path, compression=compression, **kwargs)
            # Upload parquet file
            upload_sql = (
                "PUT /* Python:zettapark.connector.df_pandas_tools.write_pandas() */ "
                "'{path}' TO {volume_path} SUBDIRECTORY '{volume_dir}' PARALLEL={parallel}"
            ).format(
                path=chunk_path.replace("\\", "\\\\").replace("'", "\\'"),
                volume_path=volume_path,
                volume_dir=volume_dir,
                parallel=parallel,
            )
            logger.debug(f"uploading files with '{upload_sql}'")
            cursor.execute(upload_sql)
            # Remove chunk file
            os.remove(chunk_path)

    # in Clickzetta, all parquet data is stored in a single column, $1, so we must select columns explicitly
    # see (https://doc.clickzetta.com/
    if quote_identifiers:
        quote = "`"
        # if the column name contains a double quote, we need to escape it by replacing with two double quotes
        # https://doc.clickzetta.com/
        column_names = [quote_name(str(c)) for c in df.columns]
    else:
        quote = ""
        column_names = list(df.columns)
    columns = quote + f"{quote},{quote}".join(column_names) + quote

    def drop_object(name: str, object_type: str) -> None:
        drop_sql = f"DROP {object_type.upper()} IF EXISTS {name} /* Python:zettapark.connector.pandas_tools.write_pandas() */"
        logger.debug(f"dropping {object_type} with '{drop_sql}'")
        cursor.execute(drop_sql)

    column_type_mapping = dict()
    for struct_field in table_schema.fields:
        column_type_mapping[
            struct_field.name.replace("`", "")
        ] = convert_data_type_to_name(struct_field.datatype)

    if auto_create_table or overwrite:
        # Infer schema can return the columns out of order depending on the chunking we do when uploading
        # so we have to iterate through the dataframe columns to make sure we create the table with its
        # columns in order
        create_table_columns = (
            ", ".join(
                [
                    f"{quote}{col_name}{quote} {column_type_mapping[col]}"
                    for col_name, col in zip(column_names, df.columns)
                ]
            )
            .replace('"', "")
            .replace("'", "")
        )

        target_table_location = build_location_helper(
            database,
            schema,
            volume_dir if (overwrite and auto_create_table) else table_name,
            quote_identifiers,
        )

        if auto_create_table:
            create_table_sql = (
                f"CREATE TABLE IF NOT EXISTS {target_table_location} "
                f"({create_table_columns})"
                f" /* Python:zettapark.connector.pandas_tools.write_pandas() */ "
            )
            logger.debug(f"auto creating table with '{create_table_sql}'")
            cursor.execute(create_table_sql)
        # need explicit casting when the underlying table schema is inferred
        parquet_columns = ", ".join(
            f"{quote}{col_name}{quote} {column_type_mapping[col]}"
            for col_name, col in zip(column_names, df.columns)
        )
    else:
        target_table_location = build_location_helper(
            database=database,
            schema=schema,
            name=table_name,
            quote_identifiers=quote_identifiers,
        )
        parquet_columns = ", ".join(
            f"{quote}{col_name}{quote} {column_type_mapping[col]}"
            for col_name, col in zip(column_names, df.columns)
        )

    try:
        if overwrite and (not auto_create_table):
            truncate_sql = f"TRUNCATE TABLE {target_table_location} /* Python:zettapark.connector.pandas_tools.write_pandas() */"
            logger.debug(f"truncating table with '{truncate_sql}'")
            cursor.execute(truncate_sql)

        copy_into_sql = (
            f"COPY INTO {target_table_location} /* Python:zettapark.connector.pandas_tools.write_pandas() */ "
            f"FROM (SELECT {columns} FROM {volume_path} ({parquet_columns}) "
            f"USING PARQUET SUBDIRECTORY '{volume_dir}' ) "
        )
        logger.debug(f"copying into with '{copy_into_sql}'")
        cursor.execute(copy_into_sql)
        copy_results = QueryResult(cursor._query_result.total_msg, True)

        if overwrite and auto_create_table:
            original_table_location = build_location_helper(
                database=database,
                schema=schema,
                name=table_name,
                quote_identifiers=quote_identifiers,
            )
            drop_object(original_table_location, "table")
            rename_table_sql = f"ALTER TABLE {target_table_location} RENAME TO {original_table_location} /* Python:zettapark.connector.pandas_tools.write_pandas() */"
            logger.debug(f"rename table with '{rename_table_sql}'")
            cursor.execute(rename_table_sql)
    except ProgrammingError:
        if overwrite and auto_create_table:
            # drop table only if we created a new one with a random name
            drop_object(target_table_location, "table")
        raise
    finally:
        # cursor._log_telemetry_job_data(TelemetryField.PANDAS_WRITE, TelemetryData.TRUE)
        # clean user volume sub dir
        clean_volumn_dir_sql = f"DELETE {volume_path} subdirectory '{volume_dir}' "
        logger.debug(f"clean user volume with '{clean_volumn_dir_sql}'")
        cursor.execute(clean_volumn_dir_sql)
        cursor.close()

    return (
        copy_results.state == "UPLOADED" or copy_results.state == "SUCCEED",
        copy_results.total_msg,
    )
