#!/usr/bin/env python3
#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
# Copyright (c) 2023-2024 Yunqi Inc. All rights reserved.
#


import functools
import inspect
import os
import sys
import time
from logging import getLogger
from typing import IO, Any, Dict, Iterator, List, Optional, Sequence, Set, Tuple, Union

from clickzetta.zettapark._connector import (
    ClickzettaConnection,
    ClickzettaCursor,
    NotSupportedError,
    ProgrammingError,
    ReauthenticationRequest,
    ResultMetadata,
    clickzetta_connect,
    pandas,
)
from clickzetta.zettapark._internal.analyzer.analyzer_utils import (
    quote_name_without_upper_casing,
)
from clickzetta.zettapark._internal.analyzer.expression import Attribute
from clickzetta.zettapark._internal.analyzer.query_plan import (
    BatchInsertQuery,
    QueryPlan,
)
from clickzetta.zettapark._internal.analyzer.schema_utils import (
    convert_result_meta_to_attribute,
    run_new_describe,
)
from clickzetta.zettapark._internal.error_message import (
    ZettaparkClientExceptionMessages,
)
from clickzetta.zettapark._internal.telemetry import TelemetryClient
from clickzetta.zettapark._internal.utils import (
    escape_quotes,
    get_application_name,
    get_version,
    is_in_stored_procedure,
    is_sql_select_statement,
    is_sql_show_statement,
    normalize_local_file,
    normalize_remote_file_or_dir,
    result_set_to_iter,
    result_set_to_rows,
    unwrap_stage_location_single_quote,
)
from clickzetta.zettapark.async_job import AsyncJob, _AsyncResultType
from clickzetta.zettapark.exceptions import ZettaparkSQLException
from clickzetta.zettapark.query_history import QueryHistory, QueryRecord
from clickzetta.zettapark.row import Row

# from clickzetta.zettapark._internal.telemetry import TelemetryClient


logger = getLogger(__name__)

# parameters needed for usage tracking
PARAM_APPLICATION = "application"
PARAM_INTERNAL_APPLICATION_NAME = "internal_application_name"
PARAM_INTERNAL_APPLICATION_VERSION = "internal_application_version"


def _build_target_path(stage_location: str, dest_prefix: str = "") -> str:
    qualified_stage_name = unwrap_stage_location_single_quote(stage_location)
    dest_prefix_name = (
        dest_prefix
        if not dest_prefix or dest_prefix.startswith("/")
        else f"/{dest_prefix}"
    )
    return f"{qualified_stage_name}{dest_prefix_name if dest_prefix_name else ''}"


def _build_put_statement(
    local_path: str,
    stage_location: str,
    dest_prefix: str = "",
    parallel: int = 4,
    compress_data: bool = True,
    source_compression: str = "AUTO_DETECT",
    overwrite: bool = False,
) -> str:
    target_path = normalize_remote_file_or_dir(
        _build_target_path(stage_location, dest_prefix)
    )
    parallel_str = f"PARALLEL = {parallel}"
    compress_str = f"AUTO_COMPRESS = {str(compress_data).upper()}"
    source_compression_str = f"SOURCE_COMPRESSION = {source_compression.upper()}"
    overwrite_str = f"OVERWRITE = {str(overwrite).upper()}"
    final_statement = f"PUT {local_path} {target_path} {parallel_str} {compress_str} {source_compression_str} {overwrite_str}"
    return final_statement


class ServerConnection:
    class _Decorator:
        @classmethod
        def wrap_exception(cls, func):
            def wrap(*args, **kwargs):
                if args[0]._conn.is_closed():
                    raise ZettaparkClientExceptionMessages.SERVER_SESSION_HAS_BEEN_CLOSED()
                try:
                    return func(*args, **kwargs)
                except ReauthenticationRequest as ex:
                    raise ZettaparkClientExceptionMessages.SERVER_SESSION_EXPIRED(
                        ex.cause
                    )
                except Exception as ex:
                    raise ex

            return wrap

        @classmethod
        def log_msg_and_perf_telemetry(cls, msg):
            def log_and_telemetry(func):
                @functools.wraps(func)
                def wrap(*args, **kwargs):
                    logger.debug(msg)
                    start_time = time.perf_counter()
                    result = func(*args, **kwargs)
                    end_time = time.perf_counter()
                    duration = end_time - start_time
                    # job_id = result["job_id"] if result and "job_id" in result else None
                    # If we don't have a query id, then its pretty useless to send perf telemetry
                    # if job_id:
                    #     args[0]._telemetry_client.send_upload_file_perf_telemetry(
                    #         func.__name__, duration, job_id
                    #     )
                    logger.debug(f"Finished in {duration:.4f} secs")
                    return result

                return wrap

            return log_and_telemetry

    def __init__(
        self,
        options: Dict[str, Union[int, str]],
        conn: Optional[ClickzettaConnection] = None,
    ) -> None:
        self._lower_case_parameters = {k.lower(): v for k, v in options.items()}
        self._add_application_parameters()
        self._conn = conn if conn else clickzetta_connect(**self._lower_case_parameters)
        if "password" in self._lower_case_parameters:
            self._lower_case_parameters["password"] = None
        self._cursor = self._conn.cursor()
        self._telemetry_client = TelemetryClient(self._conn)
        self._query_listener: Set[QueryHistory] = set()
        # The session in this case refers to a connector session, not a
        # Zettapark session
        self._telemetry_client.send_session_created_telemetry(not bool(conn))

        # check if cursor.execute supports _skip_upload_on_content_match
        signature = inspect.signature(self._cursor.execute)
        self._supports_skip_upload_on_content_match = (
            "_skip_upload_on_content_match" in signature.parameters
        )

    def _add_application_parameters(self) -> None:
        if PARAM_APPLICATION not in self._lower_case_parameters:
            self._lower_case_parameters[PARAM_APPLICATION] = get_application_name()

        if PARAM_INTERNAL_APPLICATION_NAME not in self._lower_case_parameters:
            self._lower_case_parameters[
                PARAM_INTERNAL_APPLICATION_NAME
            ] = get_application_name()
        if PARAM_INTERNAL_APPLICATION_VERSION not in self._lower_case_parameters:
            self._lower_case_parameters[
                PARAM_INTERNAL_APPLICATION_VERSION
            ] = get_version()

    def add_query_listener(self, listener: QueryHistory) -> None:
        self._query_listener.add(listener)

    def remove_query_listener(self, listener: QueryHistory) -> None:
        self._query_listener.remove(listener)

    def close(self) -> None:
        if self._conn:
            self._conn.close()

    def is_closed(self) -> bool:
        return self._conn._closed

    @_Decorator.wrap_exception
    def get_session_id(self) -> int:
        # return self._conn.session_id
        return 1234

    @_Decorator.wrap_exception
    def _get_current_parameter(self, param: str, quoted: bool = True) -> Optional[str]:
        if param in (
            "account",
            "user",
            "database",
            "schema",
            "warehouse",
            "workspace",  # alias to database
            "vcluster",  # alias to vcluster
            "role",
        ):
            value = self._conn.get_current_parameter(param)
            return str(value).upper() if value else None
        if param in ("database"):
            param = "workspace"
        try:
            name = getattr(self._conn, param) or self._get_string_datum(
                f"SELECT CURRENT_{param.upper()}()"
            )
            return (
                (
                    quote_name_without_upper_casing(name)
                    if quoted
                    else escape_quotes(name)
                )
                if name
                else None
            )
        except AttributeError:
            return self._lower_case_parameters[param]

    def _get_string_datum(self, query: str) -> Optional[str]:
        rows = result_set_to_rows(self.run_query(query)["data"])
        return rows[0][0] if len(rows) > 0 else None

    @QueryPlan.Decorator.wrap_exception
    def get_result_attributes(self, query: str) -> List[Attribute]:
        if not is_sql_select_statement(query) and is_sql_show_statement(query):
            logger.warning(
                "Calling get_result_attributes over a non-select sql"
                f" might not work as expected: {query}"
            )
        return convert_result_meta_to_attribute(run_new_describe(self._cursor, query))

    @_Decorator.log_msg_and_perf_telemetry("Uploading file to stage")
    def upload_file(
        self,
        path: str,
        stage_location: str,
        dest_prefix: str = "",
        parallel: int = 4,
        compress_data: bool = True,
        source_compression: str = "AUTO_DETECT",
        overwrite: bool = False,
        skip_upload_on_content_match: bool = False,
    ) -> Optional[Dict[str, Any]]:
        if is_in_stored_procedure():  # pragma: no cover
            file_name = os.path.basename(path)
            target_path = _build_target_path(stage_location, dest_prefix)
            try:
                # upload_stream directly consume stage path, so we don't need to normalize it
                self._cursor.upload_stream(
                    open(path, "rb"), f"{target_path}/{file_name}"
                )
            except ProgrammingError as pe:
                tb = sys.exc_info()[2]
                ne = ZettaparkClientExceptionMessages.SQL_EXCEPTION_FROM_PROGRAMMING_ERROR(
                    pe
                )
                raise ne.with_traceback(tb) from None
        else:
            uri = normalize_local_file(path)
            if self._supports_skip_upload_on_content_match:
                kwargs = {"_skip_upload_on_content_match": skip_upload_on_content_match}
            else:
                kwargs = {}
            return self.run_query(
                _build_put_statement(
                    uri,
                    stage_location,
                    dest_prefix,
                    parallel,
                    compress_data,
                    source_compression,
                    overwrite,
                ),
                **kwargs,
            )

    @_Decorator.log_msg_and_perf_telemetry("Uploading stream to stage")
    def upload_stream(
        self,
        input_stream: IO[bytes],
        stage_location: str,
        dest_filename: str,
        dest_prefix: str = "",
        parallel: int = 4,
        compress_data: bool = True,
        source_compression: str = "AUTO_DETECT",
        overwrite: bool = False,
        is_in_udf: bool = False,
        skip_upload_on_content_match: bool = False,
    ) -> Optional[Dict[str, Any]]:
        uri = normalize_local_file(f"/tmp/placeholder/{dest_filename}")
        try:
            if is_in_stored_procedure():  # pragma: no cover
                input_stream.seek(0)
                target_path = _build_target_path(stage_location, dest_prefix)
                try:
                    # upload_stream directly consume stage path, so we don't need to normalize it
                    self._cursor.upload_stream(
                        input_stream, f"{target_path}/{dest_filename}"
                    )
                except ProgrammingError as pe:
                    tb = sys.exc_info()[2]
                    ne = ZettaparkClientExceptionMessages.SQL_EXCEPTION_FROM_PROGRAMMING_ERROR(
                        pe
                    )
                    raise ne.with_traceback(tb) from None
            else:
                if self._supports_skip_upload_on_content_match:
                    kwargs = {
                        "_skip_upload_on_content_match": skip_upload_on_content_match,
                        "file_stream": input_stream,
                    }
                else:
                    kwargs = {"file_stream": input_stream}
                return self.run_query(
                    _build_put_statement(
                        uri,
                        stage_location,
                        dest_prefix,
                        parallel,
                        compress_data,
                        source_compression,
                        overwrite,
                    ),
                    **kwargs,
                )
        # If ValueError is raised and the stream is closed, we throw the error.
        # https://docs.python.org/3/library/io.html#io.IOBase.close
        except ValueError as ex:
            if input_stream.closed:
                if is_in_udf:
                    raise ZettaparkClientExceptionMessages.SERVER_UDF_UPLOAD_FILE_STREAM_CLOSED(
                        dest_filename
                    )
                else:
                    raise ZettaparkClientExceptionMessages.SERVER_UPLOAD_FILE_STREAM_CLOSED(
                        dest_filename
                    )
            else:
                raise ex

    def notify_query_listeners(self, query_record: QueryRecord) -> None:
        for listener in self._query_listener:
            listener._add_query(query_record)

    def execute_and_notify_query_listener(
        self, query: str, **kwargs: Any
    ) -> ClickzettaCursor:
        # results_cursor = self._cursor.execute(query)
        try:
            self._cursor.execute(query)
            self.notify_query_listeners(
                QueryRecord(self._cursor.job_id, self._cursor.query)
            )
        except Exception as ex:
            # wrap the execute exception to zettapark exception
            if type(ex) is Exception:
                raise ZettaparkSQLException(
                    f"Failed to execute sql query {query}\n{ex}",
                    query=query,
                )
            else:
                raise ex
        return self._cursor

    def execute_async_and_notify_query_listener(
        self, query: str, **kwargs: Any
    ) -> ClickzettaCursor:
        raise NotImplementedError("Async Job Run not currently supported.")
        self._cursor.execute(query)
        self.notify_query_listeners(
            QueryRecord(self._cursor.job_id, self._cursor.query)
        )
        return self._cursor

    def execute_and_get_job_id(
        self,
        query: str,
        statement_params: Optional[Dict[str, str]] = None,
    ) -> str:
        results_cursor = self.execute_and_notify_query_listener(
            query, _statement_params=statement_params
        )
        return results_cursor.job_id

    @_Decorator.wrap_exception
    def run_query(
        self,
        query: str,
        to_pandas: bool = False,
        to_iter: bool = False,
        is_ddl_on_temp_object: bool = False,
        block: bool = True,
        data_type: _AsyncResultType = _AsyncResultType.ROW,
        async_job_plan: Optional[
            QueryPlan
        ] = None,  # this argument is currently only used by AsyncJob
        log_on_exception: bool = False,
        case_sensitive: bool = False,
        params: Optional[Sequence[Any]] = None,
        num_statements: Optional[int] = None,
        **kwargs,
    ) -> Union[Dict[str, Any], AsyncJob]:
        try:
            # Set ZETTAPARK_SKIP_TXN_COMMIT_IN_DDL to True to avoid DDL commands to commit the open transaction
            if is_ddl_on_temp_object:
                if not kwargs.get("_statement_params"):
                    kwargs["_statement_params"] = {}
                kwargs["_statement_params"]["ZETTAPARK_SKIP_TXN_COMMIT_IN_DDL"] = True
            if block:
                results_cursor = self.execute_and_notify_query_listener(
                    query, params=params, **kwargs
                )
                logger.debug(
                    f"Execute query [queryID: {results_cursor.job_id}] {query}"
                )
            else:
                # async run wrap by lazy query execute.
                None
                # results_cursor = self.execute_async_and_notify_query_listener(
                #     query, params=params, num_statements=num_statements, **kwargs
                # )
                # logger.debug(
                #     f"Execute async query [queryID: {results_cursor['queryId']}] {query}"
                # )
        except Exception as ex:
            if log_on_exception:
                query_id_log = (
                    f" [queryID: {ex.job_id}]" if hasattr(ex, "job_id") else ""
                )
                logger.error(f"Failed to execute query{query_id_log} {query}\n{ex}")
            raise ex

        # fetch_pandas_all/batches() only works for SELECT statements
        # We call fetchall() if fetch_pandas_all/batches() fails,
        # because when the query plan has multiple queries, it will
        # have non-select statements, and it shouldn't fail if the user
        # calls to_pandas() to execute the query.
        if block:
            return self._to_data_or_iter(
                results_cursor=results_cursor, to_pandas=to_pandas, to_iter=to_iter
            )
        else:
            import uuid

            # wrap AsyncJob with SyncJob
            return AsyncJob(
                str(uuid.uuid1()),
                query,
                async_job_plan.session,
                data_type,
                async_job_plan.post_actions,
                log_on_exception,
                case_sensitive=case_sensitive,
                num_statements=num_statements,
                **kwargs,
            )

    def _to_data_or_iter(
        self,
        results_cursor: ClickzettaCursor,
        to_pandas: bool = False,
        to_iter: bool = False,
    ) -> Dict[str, Any]:
        qid = results_cursor.job_id

        if to_iter and not to_pandas:
            new_cursor = results_cursor.connection.cursor()
            new_cursor.execute(results_cursor.query)
            results_cursor = new_cursor

        if to_pandas:
            try:
                data_or_iter = (
                    map(
                        functools.partial(
                            _fix_pandas_df_fixed_type, results_cursor=results_cursor
                        ),
                        results_cursor.fetch_panda_all(),
                    )
                    if to_iter
                    else _fix_pandas_df_fixed_type(
                        results_cursor.fetch_panda_all(),
                        results_cursor,
                    )
                )
            except NotSupportedError:
                data_or_iter = (
                    iter(results_cursor) if to_iter else results_cursor.fetchall()
                )
            except KeyboardInterrupt:
                raise
            except BaseException as ex:
                raise ZettaparkClientExceptionMessages.SERVER_FAILED_FETCH_PANDAS(
                    str(ex)
                )
        else:
            data_or_iter = (
                iter(results_cursor) if to_iter else results_cursor.fetchall()
            )

        return {"data": data_or_iter, "job_id": qid}

    def execute(
        self,
        plan: QueryPlan,
        to_pandas: bool = False,
        to_iter: bool = False,
        block: bool = True,
        data_type: _AsyncResultType = _AsyncResultType.ROW,
        log_on_exception: bool = False,
        case_sensitive: bool = False,
        **kwargs,
    ) -> Union[
        List[Row], "pandas.DataFrame", Iterator[Row], Iterator["pandas.DataFrame"]
    ]:
        if (
            is_in_stored_procedure()
            and not block
            and not self._get_client_side_session_parameter(
                "ENABLE_ASYNC_QUERY_IN_PYTHON_STORED_PROCS", False
            )
        ):  # pragma: no cover
            raise NotImplementedError(
                "Async query is not supported in stored procedure yet"
            )
        result_set, result_meta = self.get_result_set(
            plan,
            to_pandas,
            to_iter,
            **kwargs,
            block=block,
            data_type=data_type,
            log_on_exception=log_on_exception,
            case_sensitive=case_sensitive,
        )
        if not block:
            return result_set
        elif to_pandas:
            return result_set["data"]
        else:
            if to_iter:
                return result_set_to_iter(
                    result_set["data"], result_meta, case_sensitive=case_sensitive
                )
            else:
                return result_set_to_rows(
                    result_set["data"], result_meta, case_sensitive=case_sensitive
                )

    @QueryPlan.Decorator.wrap_exception
    def get_result_set(
        self,
        plan: QueryPlan,
        to_pandas: bool = False,
        to_iter: bool = False,
        block: bool = True,
        data_type: _AsyncResultType = _AsyncResultType.ROW,
        log_on_exception: bool = False,
        case_sensitive: bool = False,
        **kwargs,
    ) -> Tuple[
        Dict[
            str,
            Union[
                List[Any],
                "pandas.DataFrame",
                ClickzettaCursor,
                Iterator["pandas.DataFrame"],
                str,
            ],
        ],
        List[ResultMetadata],
    ]:
        action_id = plan.session._generate_new_action_id()
        # potentially optimize the query using CTEs
        plan = plan.replace_repeated_subquery_with_cte()
        result, result_meta = None, None
        try:
            placeholders = {}
            is_batch_insert = False
            for q in plan.queries:
                if isinstance(q, BatchInsertQuery):
                    is_batch_insert = True
                    break
            # since batch insert does not support async execution (? in the query), we handle it separately here
            if len(plan.queries) > 1 and not block and not is_batch_insert:
                params = []
                final_queries = []
                last_place_holder = None
                for q in plan.queries:
                    final_queries.append(
                        q.sql.replace(f"'{last_place_holder}'", "LAST_QUERY_ID()")
                        if last_place_holder
                        else q.sql
                    )
                    last_place_holder = q.query_id_place_holder
                    params.extend(q.params)

                result = self.run_query(
                    ";".join(final_queries),
                    to_pandas,
                    to_iter,
                    is_ddl_on_temp_object=plan.queries[0].is_ddl_on_temp_object,
                    block=block,
                    data_type=data_type,
                    async_job_plan=plan,
                    log_on_exception=log_on_exception,
                    case_sensitive=case_sensitive,
                    num_statements=len(plan.queries),
                    params=params,
                    **kwargs,
                )

                # since we will return a AsyncJob instance, result_meta is not needed, we will create result_meta in
                # AsyncJob instance when needed
                result_meta = None
                if action_id < plan.session._last_canceled_id:
                    raise ZettaparkClientExceptionMessages.SERVER_QUERY_IS_CANCELLED()
            else:
                for i, query in enumerate(plan.queries):
                    if isinstance(query, BatchInsertQuery):
                        self.run_batch_insert(query.sql, query.rows, **kwargs)
                    else:
                        is_last = i == len(plan.queries) - 1 and not block
                        final_query = query.sql
                        for holder, id_ in placeholders.items():
                            final_query = final_query.replace(holder, id_)
                        result = self.run_query(
                            final_query,
                            to_pandas,
                            to_iter and (i == len(plan.queries) - 1),
                            is_ddl_on_temp_object=query.is_ddl_on_temp_object,
                            block=not is_last,
                            data_type=data_type,
                            async_job_plan=plan,
                            log_on_exception=log_on_exception,
                            case_sensitive=case_sensitive,
                            params=query.params,
                            **kwargs,
                        )
                        placeholders[query.query_id_place_holder] = (
                            result["job_id"] if not is_last else result.query_id
                        )
                        result_meta = self._cursor.description
                    if action_id < plan.session._last_canceled_id:
                        raise ZettaparkClientExceptionMessages.SERVER_QUERY_IS_CANCELLED()
        finally:
            # delete created tmp object
            if block:
                for action in plan.post_actions:
                    self.run_query(
                        action.sql,
                        is_ddl_on_temp_object=action.is_ddl_on_temp_object,
                        block=block,
                        log_on_exception=log_on_exception,
                        case_sensitive=case_sensitive,
                        **kwargs,
                    )

        if result is None:
            raise ZettaparkClientExceptionMessages.SQL_LAST_QUERY_RETURN_RESULTSET()

        return result, result_meta

    def get_result_and_metadata(
        self, plan: QueryPlan, **kwargs
    ) -> Tuple[List[Row], List[Attribute]]:
        result_set, result_meta = self.get_result_set(plan, **kwargs)
        result = result_set_to_rows(result_set["data"])
        attributes = convert_result_meta_to_attribute(result_meta)
        return result, attributes

    def get_result_query_id(self, plan: QueryPlan, **kwargs) -> str:
        # get the iterator such that the data is not fetched
        result_set, _ = self.get_result_set(plan, to_iter=True, **kwargs)
        return result_set["job_id"]

    @_Decorator.wrap_exception
    def run_batch_insert(self, query: str, rows: List[Row], **kwargs) -> None:
        params = [list(row) for row in rows]
        # statement_params = kwargs.get("_statement_params")
        self._cursor.executemany(query, params)
        self.notify_query_listeners(
            QueryRecord(self._cursor.job_id, self._cursor.query)
        )
        logger.debug("Execute batch insertion query %s", query)

    def _get_client_side_session_parameter(self, name: str, default_value: Any) -> Any:
        return (
            self._conn._session_parameters.get(name, default_value)
            if self._conn._session_parameters
            else default_value
        )


def _fix_pandas_df_fixed_type(
    pd_df: "pandas.DataFrame", results_cursor: ClickzettaCursor
) -> "pandas.DataFrame":
    """The compiler does not make any guarantees about the return types - only that they will be large enough for the result.
    As a result, the ResultMetadata may contain precision=38, scale=0 for result of a column which may only contain single
    digit numbers. Then the returned pandas DataFrame has dtype "object" with a str value for that column instead of int64.

    Based on the Result Metadata characteristics, this functions tries to make a best effort conversion to int64 without losing
    precision.

    We need to get rid of this workaround because this causes a performance hit.
    """
    for column_metadata, pandas_dtype, pandas_col_name in zip(
        results_cursor.description, pd_df.dtypes, pd_df.columns
    ):
        if (
            column_metadata.type_code == "FIXED"
            and column_metadata.precision is not None
        ):
            if column_metadata.scale == 0 and not str(pandas_dtype).startswith("int"):
                # When scale = 0 and precision values are between 10-20, the integers fit into int64.
                # If we rely only on pandas.to_numeric, it loses precision value on large integers, therefore
                # we try to strictly use astype("int64") in this scenario. If the values are too large to
                # fit in int64, an OverflowError is thrown and we rely on to_numeric to choose and appropriate
                # floating datatype to represent the number.
                if (
                    column_metadata.precision > 10
                    and not pd_df[pandas_col_name].hasnans
                ):
                    try:
                        pd_df[pandas_col_name] = pd_df[pandas_col_name].astype("int64")
                    except OverflowError:
                        pd_df[pandas_col_name] = pandas.to_numeric(
                            pd_df[pandas_col_name], downcast="integer"
                        )
                else:
                    pd_df[pandas_col_name] = pandas.to_numeric(
                        pd_df[pandas_col_name], downcast="integer"
                    )
            elif column_metadata.scale > 0 and not str(pandas_dtype).startswith(
                "float"
            ):
                # For decimal columns, we want to cast it into float64 because pandas doesn't
                # recognize decimal type.
                pandas.to_numeric(pd_df[pandas_col_name], downcast="float")
                if pd_df[pandas_col_name].dtype == "O":
                    pd_df[pandas_col_name] = pd_df[pandas_col_name].astype("float64")
    return pd_df
