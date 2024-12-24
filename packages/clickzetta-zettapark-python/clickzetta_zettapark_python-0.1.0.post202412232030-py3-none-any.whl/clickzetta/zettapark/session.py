#!/usr/bin/env python3
#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
# Copyright (c) 2023-2024 Yunqi Inc. All rights reserved.
#


import atexit
import json
import logging
import os
import re
import sys
import tempfile
from collections import defaultdict
from functools import reduce
from logging import getLogger
from threading import RLock
from types import ModuleType
from typing import Any, Dict, List, Literal, Optional, Sequence, Set, Tuple, Union

import cloudpickle
import pkg_resources

from clickzetta.zettapark._connector import (
    ClickzettaConnection as Connection,
    ProgrammingError,
    installed_pandas,
    pandas,
)
from clickzetta.zettapark._internal.analyzer import analyzer_utils
from clickzetta.zettapark._internal.analyzer.analyzer import Analyzer
from clickzetta.zettapark._internal.analyzer.analyzer_utils import result_scan_statement
from clickzetta.zettapark._internal.analyzer.expression import Attribute
from clickzetta.zettapark._internal.analyzer.query_plan import QueryPlanBuilder
from clickzetta.zettapark._internal.analyzer.query_plan_node import Range, Values
from clickzetta.zettapark._internal.analyzer.select_statement import (
    SelectSQL,
    SelectStatement,
    SelectTableFunction,
    SelectValuesSQL,
)
from clickzetta.zettapark._internal.analyzer.table_function import (
    FlattenFunction,
    GeneratorTableFunction,
    TableFunctionRelation,
)
from clickzetta.zettapark._internal.analyzer.unary_expression import Cast
from clickzetta.zettapark._internal.df_pandas_utils import _write_pandas
from clickzetta.zettapark._internal.error_message import (
    ZettaparkClientExceptionMessages,
)
from clickzetta.zettapark._internal.packaging_utils import (
    DEFAULT_PACKAGES,
    ENVIRONMENT_METADATA_FILE_NAME,
    IMPLICIT_ZIP_FILE_NAME,
    delete_files_belonging_to_packages,
    detect_native_dependencies,
    get_signature,
    identify_supported_packages,
    map_python_packages_to_files_and_folders,
    parse_conda_environment_yaml_file,
    parse_requirements_text_file,
    pip_install_packages_to_target_folder,
    zip_directory_contents,
)
from clickzetta.zettapark._internal.server_connection import ServerConnection
from clickzetta.zettapark._internal.telemetry import set_api_call_source
from clickzetta.zettapark._internal.type_utils import (
    ColumnOrName,
    convert_data_type_to_name,
    infer_schema,
    infer_type,
    merge_type,
)
from clickzetta.zettapark._internal.udf_utils import generate_call_python_sp_sql
from clickzetta.zettapark._internal.utils import (
    MODULE_NAME_TO_PACKAGE_NAME_MAP,
    STAGE_PREFIX,
    SUPPORTED_TABLE_TYPES,
    TempObjectType,
    calculate_checksum,
    deprecated,
    escape_quotes,
    experimental,
    experimental_parameter,
    get_connector_version,
    get_os_name,
    get_python_version,
    get_temp_type_for_object,
    get_version,
    is_in_stored_procedure,
    normalize_local_file,
    normalize_remote_file_or_dir,
    parse_positional_args_to_list,
    private_preview,
    quote_name,
    random_name_for_temp_object,
    unwrap_stage_location_single_quote,
    validate_object_name,
    warning,
    zip_file_or_directory_to_stream,
)
from clickzetta.zettapark._internal.volume_utils import (
    _parse_volume_uri,
    volume_file_operation_statement,
)
from clickzetta.zettapark.async_job import AsyncJob
from clickzetta.zettapark.column import Column
from clickzetta.zettapark.context import _use_scoped_temp_objects
from clickzetta.zettapark.dataframe import DataFrame
from clickzetta.zettapark.dataframe_reader import DataFrameReader
from clickzetta.zettapark.exceptions import ZettaparkClientException
from clickzetta.zettapark.file_operation import FileOperation
from clickzetta.zettapark.functions import array_agg, col, column, lit
from clickzetta.zettapark.query_history import QueryHistory
from clickzetta.zettapark.row import Row
from clickzetta.zettapark.stored_procedure import StoredProcedureRegistration
from clickzetta.zettapark.table import Table
from clickzetta.zettapark.table_function import (
    TableFunctionCall,
    _create_table_function_expression,
)
from clickzetta.zettapark.types import DataType, StructType
from clickzetta.zettapark.udaf import UDAFRegistration
from clickzetta.zettapark.udf import UDFRegistration
from clickzetta.zettapark.udtf import UDTFRegistration

# Python 3.8 needs to use typing.Iterable because collections.abc.Iterable is not subscriptable
# Python 3.9 can use both
# Python 3.10 needs to use collections.abc.Iterable because typing.Iterable is removed
if sys.version_info <= (3, 9):
    from typing import Iterable
else:
    from collections.abc import Iterable

_logger = getLogger(__name__)

_session_management_lock = RLock()
_active_sessions: Set["Session"] = set()
_PYTHON_ZETTAPARK_USE_SCOPED_TEMP_OBJECTS_STRING = (
    "PYTHON_ZETTAPARK_USE_SCOPED_TEMP_OBJECTS"
)
_PYTHON_ZETTAPARK_USE_SQL_SIMPLIFIER_STRING = "PYTHON_ZETTAPARK_USE_SQL_SIMPLIFIER"
_PYTHON_ZETTAPARK_USE_LOGICAL_TYPE_FOR_CREATE_DATAFRAME_STRING = (
    "PYTHON_ZETTAPARK_USE_LOGICAL_TYPE_FOR_CREATE_DATAFRAME"
)
WRITE_PANDAS_CHUNK_SIZE: int = 100000 if is_in_stored_procedure() else None


def _get_active_session() -> "Session":
    with _session_management_lock:
        if len(_active_sessions) == 1:
            return next(iter(_active_sessions))
        elif len(_active_sessions) > 1:
            raise ZettaparkClientExceptionMessages.MORE_THAN_ONE_ACTIVE_SESSIONS()
        else:
            raise ZettaparkClientExceptionMessages.SERVER_NO_DEFAULT_SESSION()


def _get_active_sessions() -> Set["Session"]:
    with _session_management_lock:
        if len(_active_sessions) >= 1:
            # TODO: This function is allowing unsafe access to a mutex protected data
            #  structure, we should ONLY use it in tests
            return _active_sessions
        else:
            raise ZettaparkClientExceptionMessages.SERVER_NO_DEFAULT_SESSION()


def _add_session(session: "Session") -> None:
    with _session_management_lock:
        _active_sessions.add(session)


def _close_session_atexit():
    """
    This is the helper function to close all active sessions at interpreter shutdown. For example, when a jupyter
    notebook is shutting down, this will also close all active sessions and make sure send all telemetry to the server.
    """
    with _session_management_lock:
        for session in _active_sessions.copy():
            try:
                session.close()
            except Exception:
                pass


# Register _close_session_atexit so it will be called at interpreter shutdown
atexit.register(_close_session_atexit)


def _remove_session(session: "Session") -> None:
    with _session_management_lock:
        try:
            _active_sessions.remove(session)
        except KeyError:
            pass


class Session:
    """
    Establishes a connection with a ClickZetta database and provides methods for creating DataFrames
    and accessing objects for working with files in stages.

    When you create a :class:`Session` object, you provide connection parameters to establish a
    connection with a ClickZetta database (e.g. an account, a user name, etc.). You can
    specify these settings in a dict that associates connection parameters names with values.
    The Zettapark library uses `the Clickzetta Connector for Python <https://doc.clickzetta.com/>`_
    to connect to ClickZetta. Refer to
    `Connecting to ClickZetta using the Python Connector <https://doc.clickzetta.com/>`_
    for the details of `Connection Parameters <https://doc.clickzetta.com/>`_.

    To create a :class:`Session` object from a ``dict`` of connection parameters::

        >>> connection_parameters = {
        ...     "user": "<user_name>",
        ...     "password": "<password>",
        ...     "account": "<account_name>",
        ...     "role": "<role_name>",
        ...     "warehouse": "<warehouse_name>",
        ...     "database": "<database_name>",
        ...     "schema": "<schema_name>",
        ... }
        >>> session = Session.builder.configs(connection_parameters).create() # doctest: +SKIP

    To create a :class:`Session` object from an existing Python Connector connection::

        >>> session = Session.builder.configs({"connection": <your python connector connection>}).create() # doctest: +SKIP

    :class:`Session` contains functions to construct a :class:`DataFrame` like :meth:`table`,
    :meth:`sql` and :attr:`read`, etc.

    A :class:`Session` object is not thread-safe.
    """

    class RuntimeConfig:
        def __init__(self, session: "Session", conf: Dict[str, Any]) -> None:
            self._session = session
            self._conf = {
                "use_constant_subquery_alias": True,
                "flatten_select_after_filter_and_orderby": True,
            }  # For config that's temporary/to be removed soon
            for key, val in conf.items():
                if self.is_mutable(key):
                    self.set(key, val)

        def get(self, key: str, default=None) -> Any:
            if hasattr(Session, key):
                return getattr(self._session, key)
            if hasattr(self._session._conn._conn, key):
                return getattr(self._session._conn._conn, key)
            return self._conf.get(key, default)

        def is_mutable(self, key: str) -> bool:
            if hasattr(Session, key) and isinstance(getattr(Session, key), property):
                return getattr(Session, key).fset is not None
            if hasattr(Connection, key) and isinstance(
                getattr(Connection, key), property
            ):
                return getattr(Connection, key).fset is not None
            return key in self._conf

        def set(self, key: str, value: Any) -> None:
            if self.is_mutable(key):
                if hasattr(Session, key):
                    setattr(self._session, key, value)
                if hasattr(Connection, key):
                    setattr(self._session._conn._conn, key, value)
                if key in self._conf:
                    self._conf[key] = value
            else:
                raise AttributeError(
                    f'Configuration "{key}" does not exist or is not mutable in runtime'
                )

    class SessionBuilder:
        """
        Provides methods to set connection parameters and create a :class:`Session`.
        """

        def __init__(self) -> None:
            self._options = {}
            self._app_name = None

        def _remove_config(self, key: str) -> "Session.SessionBuilder":
            """Only used in test."""
            self._options.pop(key, None)
            return self

        def app_name(self, app_name: str) -> "Session.SessionBuilder":
            """
            Adds the app name to the :class:`SessionBuilder`
            """
            self._app_name = app_name
            return self

        def config(self, key: str, value: Union[int, str]) -> "Session.SessionBuilder":
            """
            Adds the specified connection parameter to the :class:`SessionBuilder` configuration.
            """
            self._options[key] = value
            return self

        def configs(
            self, options: Dict[str, Union[int, str]]
        ) -> "Session.SessionBuilder":
            """
            Adds the specified :class:`dict` of connection parameters to
            the :class:`SessionBuilder` configuration.

            Note:
                Calling this method overwrites any existing connection parameters
                that you have already set in the SessionBuilder.
            """
            self._options = {**self._options, **options}
            return self

        def create(self) -> "Session":
            """Creates a new Session."""
            session = self._create_internal(self._options.get("connection"))
            return session

        def getOrCreate(self) -> "Session":
            """Gets the last created session or creates a new one if needed."""
            try:
                session = _get_active_session()
                if session._conn._conn.expired:
                    _remove_session(session)
                    return self.create()
                return session
            except ZettaparkClientException as ex:
                if ex.error_code == "1403":  # No session, ok lets create one
                    return self.create()
                raise

        def _create_internal(
            self,
            conn: Optional[Connection] = None,
        ) -> "Session":
            # Set paramstyle to qmark by default to be consistent with previous behavior
            if "paramstyle" not in self._options:
                self._options["paramstyle"] = "qmark"
            new_session = Session(
                ServerConnection({}, conn) if conn else ServerConnection(self._options),
                self._options,
            )

            if "password" in self._options:
                self._options["password"] = None
            _add_session(new_session)
            return new_session

        def __get__(self, obj, objtype=None):
            return Session.SessionBuilder()

    #: Returns a builder you can use to set configuration properties
    #: and create a :class:`Session` object.
    builder: SessionBuilder = SessionBuilder()

    def __init__(
        self,
        conn: ServerConnection,
        options: Optional[Dict[str, Any]] = None,
    ) -> None:
        if len(_active_sessions) >= 1 and is_in_stored_procedure():
            raise ZettaparkClientExceptionMessages.DONT_CREATE_SESSION_IN_SP()
        self._conn = conn
        self._import_paths: Dict[str, Tuple[Optional[str], Optional[str]]] = {}
        self._packages: Dict[str, str] = {}
        self._session_id = self._conn.get_session_id()
        self._session_info = f"""
"version" : {get_version()},
"python.version" : {get_python_version()},
"python.connector.version" : {get_connector_version()},
"python.connector.session.id" : {self._session_id},
"os.name" : {get_os_name()}
"""
        self._session_stage = random_name_for_temp_object(TempObjectType.STAGE)
        self._stage_created = False
        self._udf_registration = UDFRegistration(self)
        self._udtf_registration = UDTFRegistration(self)
        self._udaf_registration = UDAFRegistration(self)
        self._sp_registration = StoredProcedureRegistration(self)
        self._plan_builder = QueryPlanBuilder(self)
        self._last_action_id = 0
        self._last_canceled_id = 0
        self._use_scoped_temp_objects: bool = (
            _use_scoped_temp_objects
            and self._conn._get_client_side_session_parameter(
                _PYTHON_ZETTAPARK_USE_SCOPED_TEMP_OBJECTS_STRING, True
            )
        )
        self._file = FileOperation(self)
        self._analyzer = Analyzer(self)
        self._sql_simplifier_enabled: bool = True
        self._cte_optimization_enabled: bool = False
        self._use_logical_type_for_create_df: bool = True
        self._custom_package_usage_config: Dict = {}
        self._conf = self.RuntimeConfig(self, options or {})
        self._tmpdir_handler: Optional[tempfile.TemporaryDirectory] = None
        self._runtime_version_from_requirement: str = None
        self._created_temp_objects: Dict[TempObjectType, Set[str]] = defaultdict(set)

        _logger.info("Zettapark Session information: %s", self._session_info)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __str__(self):
        return (
            f"<{self.__class__.__module__}.{self.__class__.__name__}: account={self.get_current_account()}, "
            f"role={self.get_current_role()}, database={self.get_current_database()}, "
            f"schema={self.get_current_schema()}, warehouse={self.get_current_warehouse()}>"
        )

    def _generate_new_action_id(self) -> int:
        self._last_action_id += 1
        return self._last_action_id

    def _register_temp_object(self, typ: TempObjectType, name: str) -> None:
        if typ not in (TempObjectType.TABLE, TempObjectType.VIEW):
            raise ZettaparkClientException(f"Cannot register temp object: {typ}")
        self._created_temp_objects[typ].add(name)

    def _drop_temp_objects(self):
        objects = self._created_temp_objects.copy()
        self._created_temp_objects.clear()
        for typ, objs in objects.items():
            for obj in objs:
                self._conn.run_query(f"DROP {typ.name.upper()} IF EXISTS {obj}")
                _logger.info(f"Dropped temp {typ.name.lower()}: {obj}")

    def close(self) -> None:
        """Close this session."""
        if is_in_stored_procedure():
            raise ZettaparkClientExceptionMessages.DONT_CLOSE_SESSION_IN_SP()
        try:
            if self._conn.is_closed():
                _logger.debug(
                    "No-op because session %s had been previously closed.",
                    self._session_id,
                )
            else:
                self._drop_temp_objects()
                _logger.info("Closing session: %s", self._session_id)
                self.cancel_all()
        except Exception as ex:
            raise ZettaparkClientExceptionMessages.SERVER_FAILED_CLOSE_SESSION(str(ex))
        finally:
            try:
                self._conn.close()
                _logger.info("Closed session: %s", self._session_id)
            finally:
                _remove_session(self)

    @property
    def conf(self) -> RuntimeConfig:
        return self._conf

    @property
    def sql_simplifier_enabled(self) -> bool:
        """Set to ``True`` to use the SQL simplifier (defaults to ``True``).
        The generated SQLs from ``DataFrame`` transformations would have fewer layers of nested queries if the SQL simplifier is enabled.
        """
        return self._sql_simplifier_enabled

    @property
    def custom_package_usage_config(self) -> Dict:
        """Get or set configuration parameters related to usage of custom Python packages in ClickZetta.

        If enabled, pure Python packages that are not available in ClickZetta will be installed locally via pip and made available
        as an import (see :func:`add_import` for more information on imports). You can speed up this process by mentioning
        a remote stage path as ``cache_path`` where unsupported pure Python packages will be persisted. To use a specific
        version of pip, you can set the environment variable ``PIP_PATH`` to point to your pip executable. To use custom
        Python packages which are not purely Python, specify the ``force_push`` configuration parameter (*note that using
        non-pure Python packages is not recommended!*).

        This feature is **experimental**, please do not use it in production!

        Configurations:
            - **enabled** (*bool*): Turn on usage of custom pure Python packages.
            - **force_push** (*bool*): Use Python packages regardless of whether the packages are pure Python or not.
            - **cache_path** (*str*): Cache custom Python packages on a stage directory. This parameter greatly reduces latency of custom package import.
            - **force_cache** (*bool*): Use this parameter if you specified a ``cache_path`` but wish to create a fresh cache of your environment.

        Args:
            config (dict): Dictionary containing configuration parameters mentioned above (defaults to empty dictionary).

        Example::

            >>> from clickzetta.zettapark.functions import udf
            >>> session.custom_package_usage_config = {"enabled": True, "cache_path": "@my_permanent_stage/folder"} # doctest: +SKIP
            >>> session.add_packages("package_unavailable_in_clickzetta") # doctest: +SKIP
            >>> @udf
            ... def use_my_custom_package() -> str:
            ...     import package_unavailable_in_clickzetta
            ...     return "works"
            >>> session.clear_packages()
            >>> session.clear_imports()

        Note:
            - These configurations allow custom package addition via :func:`Session.add_requirements` and :func:`Session.add_packages`.
            - These configurations also allow custom package addition for all UDFs or stored procedures created later in the current session. If you only want to add custom packages for a specific UDF, you can use ``packages`` argument in :func:`functions.udf` or :meth:`session.udf.register() <clickzetta.zettapark.udf.UDFRegistration.register>`.
        """
        return self._custom_package_usage_config

    @sql_simplifier_enabled.setter
    def sql_simplifier_enabled(self, value: bool) -> None:
        self._conn._telemetry_client.send_sql_simplifier_telemetry(
            self._session_id, value
        )
        # try:
        #     self._conn._cursor.execute(
        #         f"alter session set {_PYTHON_ZETTAPARK_USE_SQL_SIMPLIFIER_STRING} = {value}"
        #     )
        # except Exception:
        #     pass
        self._sql_simplifier_enabled = value

    @custom_package_usage_config.setter
    @experimental_parameter(version="1.6.0")
    def custom_package_usage_config(self, config: Dict) -> None:
        self._custom_package_usage_config = {k.lower(): v for k, v in config.items()}

    def cancel_all(self) -> None:
        """
        Cancel all action methods that are running currently.
        This does not affect any action methods called in the future.
        """
        _logger.info("Canceling all running queries")
        self._last_canceled_id = self._last_action_id
        # self._conn.run_query(f"select system$cancel_all_queries({self._session_id})")

    def get_imports(self) -> List[str]:
        """
        Returns a list of imports added for user defined functions (UDFs).
        This list includes any Python or zip files that were added automatically by the library.
        """
        return list(self._import_paths.keys())

    def add_import(
        self,
        path: str,
        import_path: Optional[str] = None,
        chunk_size: int = 8192,
        whole_file_hash: bool = False,
    ) -> None:
        """
        Registers a remote file in stage or a local file as an import of a user-defined function
        (UDF). The local file can be a compressed file (e.g., zip), a Python file (.py),
        a directory, or any other file resource. You can also find examples in
        :class:`~clickzetta.zettapark.udf.UDFRegistration`.

        Args:
            path: The path of a local file or a remote file in the stage. In each case:

                * if the path points to a local file, this file will be uploaded to the
                  stage where the UDF is registered and ClickZetta will import the file when
                  executing that UDF.

                * if the path points to a local directory, the directory will be compressed
                  as a zip file and will be uploaded to the stage where the UDF is registered
                  and ClickZetta will import the file when executing that UDF.

                * if the path points to a file in a stage, the file will be included in the
                  imports when executing a UDF.

            import_path: The relative Python import path for a UDF.
                If it is not provided or it is None, the UDF will import the package
                directly without any leading package/module. This argument will become
                a no-op if the path  points to a stage file or a non-Python local file.

            chunk_size: The number of bytes to hash per chunk of the uploaded files.

            whole_file_hash: By default only the first chunk of the uploaded import is hashed to save
                time. When this is set to True each uploaded file is fully hashed instead.

        Example::

            >>> from clickzetta.zettapark.types import IntegerType
            >>> from resources.test_udf_dir.test_udf_file import mod5
            >>> session.add_import("tests/resources/test_udf_dir/test_udf_file.py", import_path="resources.test_udf_dir.test_udf_file")
            >>> mod5_and_plus1_udf = session.udf.register(
            ...     lambda x: mod5(x) + 1,
            ...     return_type=IntegerType(),
            ...     input_types=[IntegerType()]
            ... )
            >>> session.range(1, 8, 2).select(mod5_and_plus1_udf("id")).to_df("col1").collect()
            [Row(COL1=2), Row(COL1=4), Row(COL1=1), Row(COL1=3)]
            >>> session.clear_imports()

        Note:
            1. In favor of the lazy execution, the file will not be uploaded to the stage
            immediately, and it will be uploaded when a UDF is created.

            2. The Zettapark library calculates a sha256 checksum for every file/directory.
            Each file is uploaded to a subdirectory named after the checksum for the
            file in the stage. If there is an existing file or directory, the Zettapark
            library will compare their checksums to determine whether it should be re-uploaded.
            Therefore, after uploading a local file to the stage, if the user makes
            some changes to this file and intends to upload it again, just call this
            function with the file path again, the existing file in the stage will be
            overwritten by the re-uploaded file.

            3. Adding two files with the same file name is not allowed, because UDFs
            can't be created with two imports with the same name.

            4. This method will register the file for all UDFs created later in the current
            session. If you only want to import a file for a specific UDF, you can use
            ``imports`` argument in :func:`functions.udf` or
            :meth:`session.udf.register() <clickzetta.zettapark.udf.UDFRegistration.register>`.
        """
        path, checksum, leading_path = self._resolve_import_path(
            path, import_path, chunk_size, whole_file_hash
        )
        self._import_paths[path] = (checksum, leading_path)

    def remove_import(self, path: str) -> None:
        """
        Removes a file in stage or local file from the imports of a user-defined function (UDF).

        Args:
            path: a path pointing to a local file or a remote file in the stage

        Examples::

            >>> session.clear_imports()
            >>> len(session.get_imports())
            0
            >>> session.add_import("tests/resources/test_udf_dir/test_udf_file.py")
            >>> len(session.get_imports())
            1
            >>> session.remove_import("tests/resources/test_udf_dir/test_udf_file.py")
            >>> len(session.get_imports())
            0
        """
        trimmed_path = path.strip()
        abs_path = (
            os.path.abspath(trimmed_path)
            if not trimmed_path.startswith(STAGE_PREFIX)
            else trimmed_path
        )
        if abs_path not in self._import_paths:
            raise KeyError(f"{abs_path} is not found in the existing imports")
        else:
            self._import_paths.pop(abs_path)

    def clear_imports(self) -> None:
        """
        Clears all files in a stage or local files from the imports of a user-defined function (UDF).
        """
        self._import_paths.clear()

    def _resolve_import_path(
        self,
        path: str,
        import_path: Optional[str] = None,
        chunk_size: int = 8192,
        whole_file_hash: bool = False,
    ) -> Tuple[str, Optional[str], Optional[str]]:
        trimmed_path = path.strip()
        trimmed_import_path = import_path.strip() if import_path else None

        if not trimmed_path.startswith(STAGE_PREFIX):
            if not os.path.exists(trimmed_path):
                raise FileNotFoundError(f"{trimmed_path} is not found")
            if not os.path.isfile(trimmed_path) and not os.path.isdir(
                trimmed_path
            ):  # pragma: no cover
                # os.path.isfile() returns True when the passed in file is a symlink.
                # So this code might not be reachable. To avoid mistakes, keep it here for now.
                raise ValueError(
                    f"add_import() only accepts a local file or directory, "
                    f"or a file in a stage, but got {trimmed_path}"
                )
            abs_path = os.path.abspath(trimmed_path)

            # convert the Python import path to the file path
            # and extract the leading path, where
            # absolute path = [leading path]/[parsed file path of Python import path]
            if trimmed_import_path is not None:
                # the import path only works for the directory and the Python file
                if os.path.isdir(abs_path):
                    import_file_path = trimmed_import_path.replace(".", os.path.sep)
                elif os.path.isfile(abs_path) and abs_path.endswith(".py"):
                    import_file_path = (
                        f"{trimmed_import_path.replace('.', os.path.sep)}.py"
                    )
                else:
                    import_file_path = None
                if import_file_path:
                    if abs_path.endswith(import_file_path):
                        leading_path = abs_path[: -len(import_file_path)]
                    else:
                        raise ValueError(
                            f"import_path {trimmed_import_path} is invalid "
                            f"because it's not a part of path {abs_path}"
                        )
                else:
                    leading_path = None
            else:
                leading_path = None

            # Include the information about import path to the checksum
            # calculation, so if the import path changes, the checksum
            # will change and the file in the stage will be overwritten.
            return (
                abs_path,
                calculate_checksum(
                    abs_path,
                    additional_info=leading_path,
                    chunk_size=chunk_size,
                    whole_file_hash=whole_file_hash,
                ),
                leading_path,
            )
        else:
            return trimmed_path, None, None

    def _resolve_imports(
        self,
        import_only_stage: str,
        upload_and_import_stage: str,
        udf_level_import_paths: Optional[
            Dict[str, Tuple[Optional[str], Optional[str]]]
        ] = None,
        *,
        statement_params: Optional[Dict[str, str]] = None,
    ) -> List[str]:
        """Resolve the imports and upload local files (if any) to the stage."""
        resolved_stage_files = []
        stage_file_list = self._list_files_in_volume(
            import_only_stage, statement_params=statement_params
        )

        normalized_import_only_location = unwrap_stage_location_single_quote(
            import_only_stage
        )
        normalized_upload_and_import_location = unwrap_stage_location_single_quote(
            upload_and_import_stage
        )

        import_paths = udf_level_import_paths or self._import_paths
        for path, (prefix, leading_path) in import_paths.items():
            # stage file
            if path.startswith(STAGE_PREFIX):
                resolved_stage_files.append(path)
            else:
                filename = (
                    f"{os.path.basename(path)}.zip"
                    if os.path.isdir(path) or path.endswith(".py")
                    else os.path.basename(path)
                )
                filename_with_prefix = f"{prefix}/{filename}"
                if filename_with_prefix in stage_file_list:
                    _logger.debug(
                        f"{filename} exists on {normalized_import_only_location}, skipped"
                    )
                    resolved_stage_files.append(
                        normalize_remote_file_or_dir(
                            f"{normalized_import_only_location}/{filename_with_prefix}"
                        )
                    )
                else:
                    # local directory or .py file
                    if os.path.isdir(path) or path.endswith(".py"):
                        with zip_file_or_directory_to_stream(
                            path, leading_path
                        ) as input_stream:
                            self._conn.upload_stream(
                                input_stream=input_stream,
                                stage_location=normalized_upload_and_import_location,
                                dest_filename=filename,
                                dest_prefix=prefix,
                                source_compression="DEFLATE",
                                compress_data=False,
                                overwrite=True,
                                is_in_udf=True,
                                skip_upload_on_content_match=True,
                            )
                    # local file
                    else:
                        self._conn.upload_file(
                            path=path,
                            stage_location=normalized_upload_and_import_location,
                            dest_prefix=prefix,
                            compress_data=False,
                            overwrite=True,
                            skip_upload_on_content_match=True,
                        )
                    resolved_stage_files.append(
                        normalize_remote_file_or_dir(
                            f"{normalized_upload_and_import_location}/{filename_with_prefix}"
                        )
                    )

        return resolved_stage_files

    def _list_files_in_volume(
        self,
        volume_path: Optional[str] = None,
        *,
        statement_params: Optional[Dict[str, str]] = None,
    ) -> Set[str]:
        if not volume_path.endswith("/"):
            raise ValueError(f"volume_path must end with '/': {volume_path}")
        res = self.sql(
            volume_file_operation_statement("LIST", "", volume_path)
        ).collect()
        volume_uri = _parse_volume_uri(volume_path)
        prefix_length = len(volume_uri.path) - 1
        return {str(row[0])[prefix_length:] for row in res}

    def get_packages(self) -> Dict[str, str]:
        """
        Returns a ``dict`` of packages added for user-defined functions (UDFs).
        The key of this ``dict`` is the package name and the value of this ``dict``
        is the corresponding requirement specifier.
        """
        return self._packages.copy()

    def add_packages(
        self, *packages: Union[str, ModuleType, Iterable[Union[str, ModuleType]]]
    ) -> None:
        """
        Adds third-party packages as dependencies of a user-defined function (UDF).
        Use this method to add packages for UDFs as installing packages using
        `conda <https://docs.conda.io/en/latest/>`_. You can also find examples in
        :class:`~clickzetta.zettapark.udf.UDFRegistration`. See details of
        `third-party Python packages in ClickZetta <https://doc.clickzetta.com/>`_.

        To use Python packages that are not available in ClickZetta, refer to :meth:`~clickzetta.zettapark.Session.custom_package_usage_config`.

        Args:
            packages: A `requirement specifier <https://packaging.python.org/en/latest/glossary/#term-Requirement-Specifier>`_,
                a ``module`` object or a list of them for installing the packages. An exception
                will be raised if two conflicting requirement specifiers are provided.
                The syntax of a requirement specifier is defined in full in
                `PEP 508 <https://www.python.org/dev/peps/pep-0508/>`_, but currently only the
                `version matching clause <https://www.python.org/dev/peps/pep-0440/#version-matching>`_ (``==``)
                is supported as a `version specifier <https://packaging.python.org/en/latest/glossary/#term-Version-Specifier>`_
                for this argument. If a ``module`` object is provided, the package will be
                installed with the version in the local environment.

        Example::

            >>> import numpy as np
            >>> from clickzetta.zettapark.functions import udf
            >>> import numpy
            >>> import pandas
            >>> import dateutil
            >>> # add numpy with the latest version on ClickZetta Anaconda
            >>> # and pandas with the version "1.3.*"
            >>> # and dateutil with the local version in your environment
            >>> session.custom_package_usage_config = {"enabled": True}
            >>> session.add_packages("numpy", "pandas==1.5.*", dateutil)
            >>> @udf
            ... def get_package_name_udf() -> list:
            ...     return [numpy.__name__, pandas.__name__, dateutil.__name__]
            >>> session.sql(f"select {get_package_name_udf.name}()").to_df("col1").show()
            ----------------
            |"COL1"        |
            ----------------
            |[             |
            |  "numpy",    |
            |  "pandas",   |
            |  "dateutil"  |
            |]             |
            ----------------
            <BLANKLINE>
            >>> session.clear_packages()

        Note:
            1. This method will add packages for all UDFs created later in the current
            session. If you only want to add packages for a specific UDF, you can use
            ``packages`` argument in :func:`functions.udf` or
            :meth:`session.udf.register() <clickzetta.zettapark.udf.UDFRegistration.register>`.

            2. We recommend you to `setup the local environment with Anaconda <https://doc.clickzetta.com/>`_,
            to ensure the consistent experience of a UDF between your local environment
            and the ClickZetta server.
        """
        self._resolve_packages(
            parse_positional_args_to_list(*packages),
            self._packages,
        )

    def remove_package(self, package: str) -> None:
        """
        Removes a third-party package from the dependency list of a user-defined function (UDF).

        Args:
            package: The package name.

        Examples::

            >>> session.clear_packages()
            >>> len(session.get_packages())
            0
            >>> session.add_packages("numpy", "pandas==1.3.5")
            >>> len(session.get_packages())
            2
            >>> session.remove_package("numpy")
            >>> len(session.get_packages())
            1
            >>> session.remove_package("pandas")
            >>> len(session.get_packages())
            0
        """
        package_name = pkg_resources.Requirement.parse(package).key
        if package_name in self._packages:
            self._packages.pop(package_name)
        else:
            raise ValueError(f"{package_name} is not in the package list")

    def clear_packages(self) -> None:
        """
        Clears all third-party packages of a user-defined function (UDF).
        """
        self._packages.clear()

    def add_requirements(self, file_path: str) -> None:
        """
        Adds a `requirement file <https://pip.pypa.io/en/stable/user_guide/#requirements-files>`_
        that contains a list of packages as dependencies of a user-defined function (UDF). This function also supports
        addition of requirements via a `conda environment file <https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#create-env-file-manually>`_.

        To use Python packages that are not available in ClickZetta, refer to :meth:`~clickzetta.zettapark.Session.custom_package_usage_config`.

        Args:
            file_path: The path of a local requirement file.

        Example::

            >>> from clickzetta.zettapark.functions import udf
            >>> import numpy
            >>> import pandas
            >>> # test_requirements.txt contains "numpy" and "pandas"
            >>> session.add_requirements("tests/resources/test_requirements.txt")
            >>> @udf
            ... def get_package_name_udf() -> list:
            ...     return [numpy.__name__, pandas.__name__]
            >>> session.sql(f"select {get_package_name_udf.name}()").to_df("col1").show()
            --------------
            |"COL1"      |
            --------------
            |[           |
            |  "numpy",  |
            |  "pandas"  |
            |]           |
            --------------
            <BLANKLINE>
            >>> session.clear_packages()

        Note:
            1. This method will add packages for all UDFs created later in the current
            session. If you only want to add packages for a specific UDF, you can use
            ``packages`` argument in :func:`functions.udf` or
            :meth:`session.udf.register() <clickzetta.zettapark.udf.UDFRegistration.register>`.

            2. We recommend you to `setup the local environment with Anaconda <https://doc.clickzetta.com/>`_,
            to ensure the consistent experience of a UDF between your local environment
            and the ClickZetta server.
        """
        if file_path.endswith(".yml") or file_path.endswith(".yaml"):
            packages, runtime_version = parse_conda_environment_yaml_file(file_path)
            self._runtime_version_from_requirement = runtime_version
        else:
            packages, new_imports = parse_requirements_text_file(file_path)
            for import_path in new_imports:
                self.add_import(import_path)
        self.add_packages(packages)

    @experimental(version="1.7.0")
    def replicate_local_environment(
        self, ignore_packages: Set[str] = None, relax: bool = False
    ) -> None:
        """
        Adds all third-party packages in your local environment as dependencies of a user-defined function (UDF).
        Use this method to add packages for UDFs as installing packages using `conda <https://docs.conda.io/en/latest/>`_.
        You can also find examples in :class:`~clickzetta.zettapark.udf.UDFRegistration`. See details of `third-party Python packages in ClickZetta <https://doc.clickzetta.com/>`_.

        If you find that certain packages are causing failures related to duplicate dependencies, try adding
        duplicate dependencies to the ``ignore_packages`` parameter. If your local environment contains Python packages
        that are not available in ClickZetta, refer to :meth:`~clickzetta.zettapark.Session.custom_package_usage_config`.

        This function is **experimental**, please do not use it in production!

        Example::

            >>> from clickzetta.zettapark.functions import udf
            >>> import numpy
            >>> import pandas
            >>> # test_requirements.txt contains "numpy" and "pandas"
            >>> session.custom_package_usage_config = {"enabled": True, "force_push": True} # Recommended configuration
            >>> session.replicate_local_environment(ignore_packages={"clickzetta-zettapark-python", "clickzetta-connector-python", "urllib3", "tzdata", "numpy"}, relax=True)
            >>> @udf
            ... def get_package_name_udf() -> list:
            ...     return [numpy.__name__, pandas.__name__]
            >>> session.sql(f"select {get_package_name_udf.name}()").to_df("col1").show()
            --------------
            |"COL1"      |
            --------------
            |[           |
            |  "numpy",  |
            |  "pandas"  |
            |]           |
            --------------
            <BLANKLINE>
            >>> session.clear_packages()
            >>> session.clear_imports()

        Args:
            ignore_packages: Set of package names that will be ignored.
            relax: If set to True, package versions will not be considered.

        Note:
            1. This method will add packages for all UDFs created later in the current
            session. If you only want to add packages for a specific UDF, you can use
            ``packages`` argument in :func:`functions.udf` or
            :meth:`session.udf.register() <clickzetta.zettapark.udf.UDFRegistration.register>`.

            2. We recommend you to `setup the local environment with Anaconda <https://doc.clickzetta.com/>`_,
            to ensure the consistent experience of a UDF between your local environment
            and the ClickZetta server.
        """
        ignore_packages = {} if ignore_packages is None else ignore_packages

        packages = []
        for package in pkg_resources.working_set:
            if package.key in ignore_packages:
                _logger.info(f"{package.key} found in environment, ignoring...")
                continue
            if package.key in DEFAULT_PACKAGES:
                _logger.info(f"{package.key} is available by default, ignoring...")
                continue
            version_text = (
                "==" + package.version if package.has_version() and not relax else ""
            )
            packages.append(f"{package.key}{version_text}")

        self.add_packages(packages)

    @staticmethod
    def _parse_packages(
        packages: List[Union[str, ModuleType]],
    ) -> Dict[str, Tuple[str, bool, pkg_resources.Requirement]]:
        package_dict = dict()
        for package in packages:
            if isinstance(package, ModuleType):
                package_name = MODULE_NAME_TO_PACKAGE_NAME_MAP.get(
                    package.__name__, package.__name__
                )
                package = f"{package_name}=={pkg_resources.get_distribution(package_name).version}"
                use_local_version = True
            else:
                package = package.strip().lower()
                if package.startswith("#"):
                    continue
                use_local_version = False
            package_req = pkg_resources.Requirement.parse(package)
            # get the standard package name if there is no underscore
            # underscores are discouraged in package names, but are still used in Anaconda channel
            # pkg_resources.Requirement.parse will convert all underscores to dashes
            # the regexp is to deal with case that "_" is in the package requirement as well as version restrictions
            # we only extract the valid package name from the string by following:
            # https://packaging.python.org/en/latest/specifications/name-normalization/
            # A valid name consists only of ASCII letters and numbers, period, underscore and hyphen.
            # It must start and end with a letter or number.
            # however, we don't validate the pkg name as this is done by pkg_resources.Requirement.parse
            # find the index of the first char which is not an valid package name character
            package_name = package_req.key
            if not use_local_version and "_" in package:
                reg_match = re.search(r"[^0-9a-zA-Z\-_.]", package)
                package_name = package[: reg_match.start()] if reg_match else package

            package_dict[package] = (package_name, use_local_version, package_req)
        return package_dict

    def _get_dependency_packages(
        self,
        package_dict: Dict[str, Tuple[str, bool, pkg_resources.Requirement]],
        validate_package: bool,
        package_table: str,
        current_packages: Dict[str, str],
    ) -> (List[Exception], Any):
        # Keep track of any package errors
        errors = []

        valid_packages = self._get_available_versions_for_packages(
            package_names=[v[0] for v in package_dict.values()],
            package_table_name=package_table,
            validate_package=validate_package,
        )

        unsupported_packages: List[str] = []
        for package, package_info in package_dict.items():
            package_name, use_local_version, package_req = package_info
            package_version_req = package_req.specs[0][1] if package_req.specs else None

            if validate_package:
                if package_name not in valid_packages or (
                    package_version_req
                    and not any(v in package_req for v in valid_packages[package_name])
                ):
                    version_text = (
                        f"(version {package_version_req})"
                        if package_version_req is not None
                        else ""
                    )
                    if is_in_stored_procedure():  # pragma: no cover
                        errors.append(
                            RuntimeError(
                                f"Cannot add package {package_name}{version_text} because it is not available in ClickZetta "
                                f"and it cannot be installed via pip as you are executing this code inside a stored "
                                f"procedure. You can find the directory of these packages and add it via "
                                f"Session.add_import. See details at "
                                f"https://doc.clickzetta.com/"
                            )
                        )
                        continue
                    if (
                        package_name not in valid_packages
                        and not self._is_anaconda_terms_acknowledged()
                    ):
                        errors.append(
                            RuntimeError(
                                f"Cannot add package {package_name}{version_text} because Anaconda terms must be accepted "
                                "by ORGADMIN to use Anaconda 3rd party packages. Please follow the instructions at "
                                "https://doc.clickzetta.com/"
                            )
                        )
                        continue
                    if not self._custom_package_usage_config.get("enabled", False):
                        errors.append(
                            RuntimeError(
                                f"Cannot add package {package_req} because it is not available in ClickZetta "
                                f"and Session.custom_package_usage_config['enabled'] is not set to True. To upload these packages, you can "
                                f"set it to True or find the directory of these packages and add it via Session.add_import. See details at "
                                f"https://doc.clickzetta.com/"
                            )
                        )
                        continue
                    unsupported_packages.append(package)
                    continue
                elif not use_local_version:
                    try:
                        package_client_version = pkg_resources.get_distribution(
                            package_name
                        ).version
                        if package_client_version not in valid_packages[package_name]:
                            _logger.warning(
                                f"The version of package '{package_name}' in the local environment is "
                                f"{package_client_version}, which does not fit the criteria for the "
                                f"requirement '{package}'. Your UDF might not work when the package version "
                                f"is different between the server and your local environment."
                            )
                    except pkg_resources.DistributionNotFound:
                        _logger.warning(
                            f"Package '{package_name}' is not installed in the local environment. "
                            f"Your UDF might not work when the package is installed on the server "
                            f"but not on your local environment."
                        )
                    except Exception as ex:  # pragma: no cover
                        logging.warning(
                            "Failed to get the local distribution of package %s: %s",
                            package_name,
                            ex,
                        )

            if package_name in current_packages:
                if current_packages[package_name] != package:
                    errors.append(
                        ValueError(
                            f"Cannot add package '{package}' because {current_packages[package_name]} "
                            "is already added."
                        )
                    )
            else:
                current_packages[package_name] = package

        # Raise all exceptions at once so users know all issues in a single invocation.
        if len(errors) == 1:
            raise errors[0]
        elif len(errors) > 0:
            raise RuntimeError(errors)

        dependency_packages: List[pkg_resources.Requirement] = []
        if len(unsupported_packages) != 0:
            _logger.warning(
                f"The following packages are not available in Clickzetta: {unsupported_packages}."
            )
            if self._custom_package_usage_config.get(
                "cache_path", False
            ) and not self._custom_package_usage_config.get("force_cache", False):
                cache_path = self._custom_package_usage_config["cache_path"]
                try:
                    environment_signature = get_signature(unsupported_packages)
                    dependency_packages = self._load_unsupported_packages_from_stage(
                        environment_signature
                    )
                    if dependency_packages is None:
                        _logger.warning(
                            f"Unable to load environments from remote path {cache_path}, creating a fresh "
                            f"environment instead."
                        )
                except Exception as e:
                    _logger.warning(
                        f"Unable to load environments from remote path {cache_path}, creating a fresh "
                        f"environment instead. Error: {e.__repr__()}"
                    )

            if not dependency_packages:
                dependency_packages = self._upload_unsupported_packages(
                    unsupported_packages,
                    package_table,
                    current_packages,
                )

        return dependency_packages

    @staticmethod
    def _get_req_identifiers_list(
        modules: List[Union[str, ModuleType]], result_dict: Dict[str, str]
    ) -> List[str]:
        res = []
        for m in modules:
            if isinstance(m, str) and m not in result_dict:
                res.append(m)
            elif isinstance(m, ModuleType) and m.__name__ not in result_dict:
                res.append(f"{m.__name__}=={m.__version__}")

        return res

    def _resolve_packages(
        self,
        packages: List[Union[str, ModuleType]],
        existing_packages_dict: Optional[Dict[str, str]] = None,
        validate_package: bool = True,
        include_pandas: bool = False,
    ) -> List[str]:
        # Extract package names, whether they are local, and their associated Requirement objects
        package_dict = self._parse_packages(packages)

        package_table = "information_schema.packages"
        if not self.get_current_database():
            package_table = f"clickzetta.{package_table}"

        # result_dict is a mapping of package name -> package_spec, example
        # {'pyyaml': 'pyyaml==6.0',
        #  'networkx': 'networkx==3.1',
        #  'numpy': 'numpy',
        #  'scikit-learn': 'scikit-learn==1.2.2',
        #  'python-dateutil': 'python-dateutil==2.8.2'}
        # Add to packages dictionary
        result_dict = (
            existing_packages_dict if existing_packages_dict is not None else {}
        )

        # Retrieve list of dependencies that need to be added
        dependency_packages = self._get_dependency_packages(
            package_dict, validate_package, package_table, result_dict
        )

        # Add dependency packages
        for package in dependency_packages:
            name = package.name
            version = package.specs[0][1] if package.specs else None

            if name in result_dict:
                if version is not None:
                    added_package_has_version = "==" in result_dict[name]
                    if added_package_has_version and result_dict[name] != str(package):
                        raise ValueError(
                            f"Cannot add dependency package '{name}=={version}' "
                            f"because {result_dict[name]} is already added."
                        )
                    result_dict[name] = str(package)
            else:
                result_dict[name] = str(package)

        # Always include cloudpickle
        extra_modules = [cloudpickle]
        if include_pandas:
            extra_modules.append("pandas")

        return list(result_dict.values()) + self._get_req_identifiers_list(
            extra_modules, result_dict
        )

    def _upload_unsupported_packages(
        self,
        packages: List[str],
        package_table: str,
        package_dict: Dict[str, str],
    ) -> List[pkg_resources.Requirement]:
        """
        Uploads a list of Pypi packages, which are unavailable in ClickZetta, to session stage.

        Args:
            packages (List[str]): List of package names requested by the user, that are not present in ClickZetta.
            package_table (str): Name of ClickZetta table containing information about Anaconda packages.
            package_dict (Dict[str, str]): A dictionary of package name -> package spec of packages that have
                been added explicitly so far using add_packages() or other such methods.

        Returns:
            List[pkg_resources.Requirement]: List of package dependencies (present in ClickZetta) that would need to be added
            to the package dictionary.

        Raises:
            RuntimeError: If any failure occurs in the workflow.

        """
        if not self._custom_package_usage_config.get("cache_path", False):
            _logger.warning(
                "If you are adding package(s) unavailable in ClickZetta, it is highly recommended that you "
                "include the 'cache_path' configuration parameter in order to reduce latency."
            )

        try:
            # Setup a temporary directory and target folder where pip install will take place.
            self._tmpdir_handler = tempfile.TemporaryDirectory()
            tmpdir = self._tmpdir_handler.name
            target = os.path.join(tmpdir, "unsupported_packages")
            if not os.path.exists(target):
                os.makedirs(target)

            pip_install_packages_to_target_folder(packages, target)

            # Create Requirement objects for packages installed, mapped to list of package files and folders.
            downloaded_packages_dict = map_python_packages_to_files_and_folders(target)

            # Fetch valid ClickZetta Anaconda versions for all packages installed by pip (if present).
            valid_downloaded_packages = self._get_available_versions_for_packages(
                package_names=[
                    package.name for package in downloaded_packages_dict.keys()
                ],
                package_table_name=package_table,
            )

            # Detect packages which use native code.
            native_packages = detect_native_dependencies(
                target, downloaded_packages_dict
            )

            # Figure out which dependencies are available in ClickZetta, and which native dependencies can be dropped.
            (
                supported_dependencies,
                dropped_dependencies,
                new_dependencies,
            ) = identify_supported_packages(
                list(downloaded_packages_dict.keys()),
                valid_downloaded_packages,
                native_packages,
                package_dict,
            )

            if len(native_packages) > 0 and not self._custom_package_usage_config.get(
                "force_push", False
            ):
                raise ValueError(
                    "Your code depends on packages that contain native code, it may not work on ClickZetta! Set Session.custom_package_usage_config['force_push'] to True "
                    "if you wish to proceed with using them anyway."
                )

            # Delete files
            delete_files_belonging_to_packages(
                supported_dependencies + dropped_dependencies,
                downloaded_packages_dict,
                target,
            )

            # Zip and add to stage
            environment_signature: str = get_signature(packages)
            zip_file = f"{IMPLICIT_ZIP_FILE_NAME}_{environment_signature}.zip"
            zip_path = os.path.join(tmpdir, zip_file)
            zip_directory_contents(target, zip_path)

            # Add packages to stage
            stage_name = self.get_session_stage()

            if self._custom_package_usage_config.get("cache_path", False):
                # Switch the stage used for storing zip file.
                stage_name = self._custom_package_usage_config["cache_path"]

                # Download metadata dictionary using the technique mentioned here: https://doc.clickzetta.com/
                metadata_file = f"{ENVIRONMENT_METADATA_FILE_NAME}.txt"
                normalized_metadata_path = normalize_remote_file_or_dir(
                    f"{stage_name}/{metadata_file}"
                )
                metadata = {
                    row[0]: row[1] if row[1] else []
                    for row in (
                        self.sql(
                            f"SELECT t.$1 as signature, t.$2 as packages from {normalized_metadata_path} t"
                        )._internal_collect_with_tag()
                    )
                }
                _logger.info(f"METADATA: {metadata}")

                # Add a new enviroment to the metadata, avoid commas while storing list of dependencies because commas are treated as default delimiters.
                metadata[environment_signature] = "|".join(
                    [
                        str(requirement)
                        for requirement in supported_dependencies + new_dependencies
                    ]
                )
                metadata_local_path = os.path.join(
                    self._tmpdir_handler.name, metadata_file
                )
                with open(metadata_local_path, "w") as file:
                    for key, value in metadata.items():
                        file.write(f"{key},{value}\n")

                # Upload metadata file to stage
                # Note that the metadata file is not compressed, only the zip files are.
                self._conn.upload_file(
                    path=normalize_local_file(metadata_local_path),
                    stage_location=normalize_remote_file_or_dir(stage_name),
                    compress_data=False,
                    overwrite=True,
                )

            self._conn.upload_file(
                path=normalize_local_file(zip_path),
                stage_location=normalize_remote_file_or_dir(stage_name),
                compress_data=True,
                overwrite=True,
            )

            # Add zipped file as an import
            stage_zip_path = f"{stage_name}/{zip_file}"
            self.add_import(
                stage_zip_path
                if stage_zip_path.startswith(STAGE_PREFIX)
                else f"{STAGE_PREFIX}{stage_zip_path}"
            )
        except Exception as e:
            raise RuntimeError(
                f"Unable to auto-upload packages: {packages}, Error: {e} | NOTE: Alternatively, you can find the "
                f"directory of these packages and add it via Session.add_import. See details at "
                f"https://doc.clickzetta.com/"
                f"-third-party-packages-from-anaconda-in-a-udf."
            )
        finally:
            if self._tmpdir_handler:
                self._tmpdir_handler.cleanup()
                self._tmpdir_handler = None

        return supported_dependencies + new_dependencies

    def _is_anaconda_terms_acknowledged(self) -> bool:
        return self._run_query("select system$are_anaconda_terms_acknowledged()")[0][0]

    def _load_unsupported_packages_from_stage(
        self, environment_signature: str
    ) -> List[pkg_resources.Requirement]:
        """
        Uses specified stage path to auto-import a group of unsupported packages, along with its dependencies. This
        saves time spent on pip install, native package detection and zip upload to stage.

        A cached environment on a stage consists of two files:
        1. A metadata dictionary, pickled using cloudpickle, which maps environment signatures to a list of
        Anaconda-supported dependency packages required for that environment.
        2. Zip files named '{PACKAGES_ZIP_NAME}_<environment_signature>.zip.gz which contain the unsupported packages.

        Note that a cached environment is only useful if you wish to use packages unsupported in ClickZetta! Supported
        packages will not be cached (and need not be cached).

        Also note that any changes to your package list, which does not involve changing the versions or names
        of unsupported packages, will not necessarily affect your environment signature. Your environment signature
        corresponds only to packages currently not supported in the Anaconda channel.

        Args:
            environment_signature (str): Unique hash signature for a set of unsupported packages, computed by hashing
            a sorted tuple of unsupported package requirements (package versioning included).
        Returns:
            Optional[List[pkg_resources.Requirement]]: A list of package dependencies for the set of unsupported packages requested.
        """
        cache_path = self._custom_package_usage_config["cache_path"]
        # Ensure that metadata file exists
        metadata_file = f"{ENVIRONMENT_METADATA_FILE_NAME}.txt"
        files: Set[str] = self._list_files_in_volume(cache_path)
        if metadata_file not in files:
            _logger.info(
                f"Metadata file named {metadata_file} not found at stage path {cache_path}."
            )
            return None  # We need the metadata file to obtain dependency package names.

        # Ensure that zipped package exists
        required_file = f"{IMPLICIT_ZIP_FILE_NAME}_{environment_signature}.zip.gz"
        if required_file not in files:
            _logger.info(
                f"Matching environment file not found at stage path {cache_path}."
            )
            return None  # We need the zipped packages folder.

        # Download metadata
        metadata_file_path = f"{cache_path}/{metadata_file}"
        metadata = {
            row[0]: row[1].split("|") if row[1] else []
            for row in (
                self.sql(
                    f"SELECT t.$1 as signature, t.$2 as packages from {normalize_remote_file_or_dir(metadata_file_path)} t"
                )
                .filter(col("signature") == environment_signature)
                ._internal_collect_with_tag()
            )
        }

        dependency_packages = [
            pkg_resources.Requirement.parse(package)
            for package in metadata[environment_signature]
        ]
        _logger.info(
            f"Loading dependency packages list - {metadata[environment_signature]}."
        )

        import_path = (
            f"{cache_path}/{IMPLICIT_ZIP_FILE_NAME}_{environment_signature}.zip.gz"
        )
        self.add_import(
            import_path
            if import_path.startswith(STAGE_PREFIX)
            else f"{STAGE_PREFIX}{import_path}"
        )
        return dependency_packages

    def _get_available_versions_for_packages(
        self,
        package_names: List[str],
        package_table_name: str,
        validate_package: bool = True,
    ) -> Dict[str, List[str]]:
        package_to_version_mapping = (
            {
                p[0]: json.loads(p[1])
                for p in self.table(package_table_name)
                .filter(
                    (col("language") == "python")
                    & (col("package_name").in_(package_names))
                )
                .group_by("package_name")
                .agg(array_agg("version"))
                ._internal_collect_with_tag()
            }
            if validate_package and len(package_names) > 0
            else None
        )
        return package_to_version_mapping

    def table(self, name: Union[str, Iterable[str]]) -> Table:
        """
        Returns a Table that points the specified table.

        Args:
            name: A string or list of strings that specify the table name or
                fully-qualified object identifier (database name, schema name, and table name).

            Note:
                If your table name contains special characters, use double quotes to mark it like this, ``session.table('"my table"')``.
                For fully qualified names, you need to use double quotes separately like this, ``session.table('"my db"."my schema"."my.table"')``.
                Refer to `Identifier Requirements <https://doc.clickzetta.com/>`_.

        Examples::

            >>> df1 = session.create_dataframe([[1, 2], [3, 4]], schema=["a", "b"])
            >>> df1.write.save_as_table("my_table", mode="overwrite", table_type="temporary")
            >>> session.table("my_table").collect()
            [Row(A=1, B=2), Row(A=3, B=4)]
            >>> current_db = session.get_current_database()
            >>> current_schema = session.get_current_schema()
            >>> session.table([current_db, current_schema, "my_table"]).collect()
            [Row(A=1, B=2), Row(A=3, B=4)]
        """

        if not isinstance(name, str) and isinstance(name, Iterable):
            name = ".".join(name)
        validate_object_name(name)
        t = Table(name, self)
        # Replace API call origin for table
        set_api_call_source(t, "Session.table")
        return t

    def table_function(
        self,
        func_name: Union[str, List[str], TableFunctionCall],
        *func_arguments: ColumnOrName,
        **func_named_arguments: ColumnOrName,
    ) -> DataFrame:
        """Creates a new DataFrame from the given SQL table function.

        References: `SQL functions <https://doc.clickzetta.com/>`_.

        Example 1
            Query a table function by function name:

            >>> from clickzetta.zettapark.functions import lit
            >>> session.table_function("split_to_table", lit("split words to table"), lit(" ")).collect()
            [Row(SEQ=1, INDEX=1, VALUE='split'), Row(SEQ=1, INDEX=2, VALUE='words'), Row(SEQ=1, INDEX=3, VALUE='to'), Row(SEQ=1, INDEX=4, VALUE='table')]

        Example 2
            Define a table function variable and query it:

            >>> from clickzetta.zettapark.functions import table_function, lit
            >>> split_to_table = table_function("split_to_table")
            >>> session.table_function(split_to_table(lit("split words to table"), lit(" "))).collect()
            [Row(SEQ=1, INDEX=1, VALUE='split'), Row(SEQ=1, INDEX=2, VALUE='words'), Row(SEQ=1, INDEX=3, VALUE='to'), Row(SEQ=1, INDEX=4, VALUE='table')]

        Example 3
            If you want to call a UDTF right after it's registered, the returned ``UserDefinedTableFunction`` is callable:

            >>> from clickzetta.zettapark.types import IntegerType, StructField, StructType
            >>> from clickzetta.zettapark.functions import udtf, lit
            >>> class GeneratorUDTF:
            ...     def process(self, n):
            ...         for i in range(n):
            ...             yield (i, )
            >>> generator_udtf = udtf(GeneratorUDTF, output_schema=StructType([StructField("number", IntegerType())]), input_types=[IntegerType()])
            >>> session.table_function(generator_udtf(lit(3))).collect()
            [Row(NUMBER=0), Row(NUMBER=1), Row(NUMBER=2)]

        Args:
            func_name: The SQL function name.
            func_arguments: The positional arguments for the SQL function.
            func_named_arguments: The named arguments for the SQL function, if it accepts named arguments.

        Returns:
            A new :class:`DataFrame` with data from calling the table function.

        See Also:
            - :meth:`DataFrame.join_table_function`, which lateral joins an existing :class:`DataFrame` and a SQL function.
            - :meth:`Session.generator`, which is used to instantiate a :class:`DataFrame` using Generator table function.
                Generator functions are not supported with :meth:`Session.table_function`.
        """
        func_expr = _create_table_function_expression(
            func_name, *func_arguments, **func_named_arguments
        )

        if self.sql_simplifier_enabled:
            d = DataFrame(
                self,
                self._analyzer.create_select_statement(
                    from_=SelectTableFunction(func_expr, analyzer=self._analyzer),
                    analyzer=self._analyzer,
                ),
            )
        else:
            d = DataFrame(
                self,
                TableFunctionRelation(func_expr),
            )
        set_api_call_source(d, "Session.table_function")
        return d

    def generator(
        self, *columns: Column, rowcount: int = 0, timelimit: int = 0
    ) -> DataFrame:
        """Creates a new DataFrame using the Generator table function.

        References: `Generator function <https://doc.clickzetta.com/>`_.

        Args:
            columns: List of data generation function that work in tandem with generator table function.
            rowcount: Resulting table with contain ``rowcount`` rows if only this argument is specified. Defaults to 0.
            timelimit: The query runs for ``timelimit`` seconds, generating as many rows as possible within the time frame. The
                exact row count depends on the system speed. Defaults to 0.

        Usage Notes:
                - When both ``rowcount`` and ``timelimit`` are specified, then:

                    + if the ``rowcount`` is reached before the ``timelimit``, the resulting table with contain ``rowcount`` rows.
                    + if the ``timelimit`` is reached before the ``rowcount``, the table will contain as many rows generated within this time.
                - If both ``rowcount`` and ``timelimit`` are not specified, 0 rows will be generated.

        Example 1
            >>> from clickzetta.zettapark.functions import seq1, seq8, uniform
            >>> df = session.generator(seq1(1).as_("sequence one"), uniform(1, 10, 2).as_("uniform"), rowcount=3)
            >>> df.show()
            ------------------------------
            |"sequence one"  |"UNIFORM"  |
            ------------------------------
            |0               |3          |
            |1               |3          |
            |2               |3          |
            ------------------------------
            <BLANKLINE>

        Example 2
            >>> df = session.generator(seq8(0), uniform(1, 10, 2), timelimit=1).order_by(seq8(0)).limit(3)
            >>> df.show()
            -----------------------------------
            |"SEQ8(0)"  |"UNIFORM(1, 10, 2)"  |
            -----------------------------------
            |0          |3                    |
            |1          |3                    |
            |2          |3                    |
            -----------------------------------
            <BLANKLINE>

        Returns:
            A new :class:`DataFrame` with data from calling the generator table function.
        """
        if not columns:
            raise ValueError("Columns cannot be empty for generator table function")
        named_args = {}
        if rowcount != 0:
            named_args["rowcount"] = lit(rowcount)._expression
        if timelimit != 0:
            named_args["timelimit"] = lit(timelimit)._expression

        operators = [self._analyzer.analyze(col._expression, {}) for col in columns]
        func_expr = GeneratorTableFunction(args=named_args, operators=operators)

        if self.sql_simplifier_enabled:
            d = DataFrame(
                self,
                SelectStatement(
                    from_=SelectTableFunction(
                        func_expr=func_expr, analyzer=self._analyzer
                    ),
                    analyzer=self._analyzer,
                ),
            )
        else:
            d = DataFrame(
                self,
                TableFunctionRelation(func_expr),
            )
        set_api_call_source(d, "Session.generator")
        return d

    def sql(self, query: str, params: Optional[Sequence[Any]] = None) -> DataFrame:
        """
        Returns a new DataFrame representing the results of a SQL query.

        Note:
            You can use this method to execute a SQL query lazily,
            which means the SQL is not executed until methods like :func:`DataFrame.collect`
            or :func:`DataFrame.to_pandas` evaluate the DataFrame.
            For **immediate execution**, chain the call with the collect method: `session.sql(query).collect()`.

        Args:
            query: The SQL statement to execute.
            params: binding parameters. We only support qmark bind variables. For more information, check
                https://doc.clickzetta.com/

        Example::

            >>> # create a dataframe from a SQL query
            >>> df = session.sql("select 1/2")
            >>> # execute the query
            >>> df.collect()
            [Row(1/2=Decimal('0.500000'))]

            >>> # Use params to bind variables
            >>> session.sql("select * from values (?, ?), (?, ?)", params=[1, "a", 2, "b"]).sort("column1").collect()
            [Row(COLUMN1=1, COLUMN2='a'), Row(COLUMN1=2, COLUMN2='b')]
        """
        pattern = re.compile(r"\(\s*\?\s*(?:,\s*\?\s*)*\)")
        if "values" in query and len(pattern.findall(query)) >= 1:
            matches = pattern.findall(query)
            if len(matches) >= 1 and not params:
                raise TypeError(f"error sql values: {params}")
            columns = []
            match = matches[0]
            if not match.count("?") - match.count(",") == 1:
                raise TypeError(f"error sql format: {match}")
            count = match.count("?")
            for i in range(count):
                columns.append(Attribute(f"col{i}", infer_type(params[i])))
            d = DataFrame(
                self,
                self._analyzer.create_select_statement(
                    from_=SelectValuesSQL(
                        query, analyzer=self._analyzer, params=params, columns=columns
                    ),
                    analyzer=self._analyzer,
                ),
            )
        else:
            # replace placeholder first.
            if "?" in query and params:
                for param in params:
                    query = query.replace("?", str(param), 1)
                params = None
            if self.sql_simplifier_enabled:
                d = DataFrame(
                    self,
                    self._analyzer.create_select_statement(
                        from_=SelectSQL(query, analyzer=self._analyzer, params=params),
                        analyzer=self._analyzer,
                    ),
                )
            else:
                d = DataFrame(
                    self,
                    self._analyzer.plan_builder.query(
                        query, source_plan=None, params=params
                    ),
                )
        set_api_call_source(d, "Session.sql")
        return d

    @property
    def read(self) -> "DataFrameReader":
        """Returns a :class:`DataFrameReader` that you can use to read data from various
        supported sources (e.g. a file in a stage) as a DataFrame."""
        return DataFrameReader(self)

    @property
    def session_id(self) -> int:
        """Returns an integer that represents the session ID of this session."""
        return self._session_id

    @property
    def connection(self) -> "Connection":
        """Returns a :class:`ClickzettaConnection` object that allows you to access the connection between the current session
        and ClickZetta server."""
        return self._conn._conn

    def _run_query(
        self,
        query: str,
        is_ddl_on_temp_object: bool = False,
        log_on_exception: bool = True,
    ) -> List[Any]:
        return self._conn.run_query(
            query,
            is_ddl_on_temp_object=is_ddl_on_temp_object,
            log_on_exception=log_on_exception,
        )["data"]

    def _get_result_attributes(self, query: str) -> List[Attribute]:
        return self._conn.get_result_attributes(query)

    def get_session_stage(self) -> str:
        """
        Returns the name of the temporary stage created by the Zettapark library
        for uploading and storing temporary artifacts for this session.
        These artifacts include libraries and packages for UDFs that you define
        in this session via :func:`add_import`.
        """
        stage_name = self.get_fully_qualified_name_if_possible(self._session_stage)
        if not self._stage_created:
            self._run_query(
                f"create {get_temp_type_for_object(self._use_scoped_temp_objects, True)} \
                stage if not exists {stage_name}",
                is_ddl_on_temp_object=True,
            )
            self._stage_created = True
        return f"{STAGE_PREFIX}{stage_name}"

    def write_pandas(
        self,
        df: "pandas.DataFrame",
        table_name: str,
        *,
        database: Optional[str] = None,
        schema: Optional[str] = None,
        chunk_size: Optional[int] = WRITE_PANDAS_CHUNK_SIZE,
        compression: str = "gzip",
        on_error: str = "abort_statement",
        parallel: int = 4,
        quote_identifiers: bool = True,
        auto_create_table: bool = False,
        create_temp_table: bool = False,
        overwrite: bool = False,
        table_type: Literal["", "temp", "temporary", "transient"] = "",
        **kwargs: Dict[str, Any],
    ) -> Table:
        """Writes a pandas DataFrame to a table in ClickZetta and returns a
        Zettapark :class:`DataFrame` object referring to the table where the
        pandas DataFrame was written to.

        Args:
            df: The pandas DataFrame we'd like to write back.
            table_name: Name of the table we want to insert into.
            database: Database that the table is in. If not provided, the default one will be used.
            schema: Schema that the table is in. If not provided, the default one will be used.
            chunk_size: Number of rows to be inserted once. If not provided, all rows will be dumped once.
                Default to None normally, 100,000 if inside a stored procedure.
            compression: The compression used on the Parquet files: gzip or snappy. Gzip gives supposedly a
                better compression, while snappy is faster. Use whichever is more appropriate.
            on_error: Action to take when COPY INTO statements fail. See details at
                `copy options <https://doc.clickzetta.com/>`_.
            parallel: Number of threads to be used when uploading chunks. See details at
                `parallel parameter <https://doc.clickzetta.com/>`_.
            quote_identifiers: By default, identifiers, specifically database, schema, table and column names
                (from :attr:`DataFrame.columns`) will be quoted. If set to ``False``, identifiers
                are passed on to ClickZetta without quoting, i.e. identifiers will be coerced to uppercase by ClickZetta.
            auto_create_table: When true, automatically creates a table to store the passed in pandas DataFrame using the
                passed in ``database``, ``schema``, and ``table_name``. Note: there are usually multiple table configurations that
                would allow you to upload a particular pandas DataFrame successfully. If you don't like the auto created
                table, you can always create your own table before calling this function. For example, auto-created
                tables will store :class:`list`, :class:`tuple` and :class:`dict` as strings in a VARCHAR column.
            create_temp_table: (Deprecated) The to-be-created table will be temporary if this is set to ``True``. Note
                that to avoid breaking changes, currently when this is set to True, it overrides ``table_type``.
            overwrite: Default value is ``False`` and the pandas DataFrame data is appended to the existing table. If set to ``True`` and if auto_create_table is also set to ``True``,
                then it drops the table. If set to ``True`` and if auto_create_table is set to ``False``,
                then it truncates the table. Note that in both cases (when overwrite is set to ``True``) it will replace the existing
                contents of the table with that of the passed in pandas DataFrame.
            table_type: The table type of table to be created. The supported values are: ``temp``, ``temporary``,
                and ``transient``. An empty string means to create a permanent table. Learn more about table types
                `here <https://doc.clickzetta.com/>`_.

        Example::

            >>> import pandas as pd
            >>> pandas_df = pd.DataFrame([(1, "Steve"), (2, "Bob")], columns=["id", "name"])
            >>> zettapark_df = session.write_pandas(pandas_df, "write_pandas_table", auto_create_table=True, table_type="temp")
            >>> zettapark_df.sort('"id"').to_pandas()
               id   name
            0   1  Steve
            1   2    Bob

            >>> pandas_df2 = pd.DataFrame([(3, "John")], columns=["id", "name"])
            >>> zettapark_df2 = session.write_pandas(pandas_df2, "write_pandas_table", auto_create_table=False)
            >>> zettapark_df2.sort('"id"').to_pandas()
               id   name
            0   1  Steve
            1   2    Bob
            2   3   John

            >>> pandas_df3 = pd.DataFrame([(1, "Jane")], columns=["id", "name"])
            >>> zettapark_df3 = session.write_pandas(pandas_df3, "write_pandas_table", auto_create_table=False, overwrite=True)
            >>> zettapark_df3.to_pandas()
               id  name
            0   1  Jane

            >>> pandas_df4 = pd.DataFrame([(1, "Jane")], columns=["id", "name"])
            >>> zettapark_df4 = session.write_pandas(pandas_df4, "write_pandas_transient_table", auto_create_table=True, table_type="transient")
            >>> zettapark_df4.to_pandas()
               id  name
            0   1  Jane

        Note:
            Unless ``auto_create_table`` is ``True``, you must first create a table in
            ClickZetta that the passed in pandas DataFrame can be written to. If
            your pandas DataFrame cannot be written to the specified table, an
            exception will be raised.
        """
        if create_temp_table:
            warning(
                "write_pandas.create_temp_table",
                "create_temp_table is deprecated. We still respect this parameter when it is True but "
                'please consider using `table_type="temporary"` instead.',
            )
            table_type = "temporary"

        if table_type and table_type.lower() not in SUPPORTED_TABLE_TYPES:
            raise ValueError(
                f"Unsupported table type. Expected table types: {SUPPORTED_TABLE_TYPES}"
            )

        success = None  # forward declaration
        try:
            if quote_identifiers:
                location = (
                    (("`" + database + "`.") if database else "")
                    + (("`" + schema + "`.") if schema else "")
                    + ("`" + table_name + "`")
                )
            else:
                location = (
                    (database + "." if database else "")
                    + (schema + "." if schema else "")
                    + (table_name)
                )
            success, ci_output = _write_pandas(
                self._conn._conn,
                df,
                table_name,
                database=database,
                schema=schema,
                chunk_size=chunk_size,
                compression=compression,
                on_error=on_error,
                parallel=parallel,
                quote_identifiers=quote_identifiers,
                auto_create_table=auto_create_table,
                overwrite=overwrite,
                table_type=table_type,
                **kwargs,
            )
        except ProgrammingError as pe:
            if pe.msg.endswith("does not exist"):
                raise ZettaparkClientExceptionMessages.DF_PANDAS_TABLE_DOES_NOT_EXIST_EXCEPTION(
                    location
                ) from pe
            else:
                raise pe

        if success:
            t = self.table(location)
            set_api_call_source(t, "Session.write_pandas")
            return t
        else:
            raise ZettaparkClientExceptionMessages.DF_PANDAS_GENERAL_EXCEPTION(
                str(ci_output)
            )

    def create_dataframe(
        self,
        data: Union[List, Tuple, "pandas.DataFrame"],
        schema: Optional[Union[StructType, Iterable[str]]] = None,
    ) -> DataFrame:
        """Creates a new DataFrame containing the specified values from the local data.

        If creating a new DataFrame from a pandas Dataframe, we will store the pandas
        DataFrame in a temporary table and return a DataFrame pointing to that temporary
        table for you to then do further transformations on. This temporary table will be
        dropped at the end of your session. If you would like to save the pandas DataFrame,
        use the :meth:`write_pandas` method instead.

        Args:
            data: The local data for building a :class:`DataFrame`. ``data`` can only
                be a :class:`list`, :class:`tuple` or pandas DataFrame. Every element in
                ``data`` will constitute a row in the DataFrame.
            schema: A :class:`~clickzetta.zettapark.types.StructType` containing names and
                data types of columns, or a list of column names, or ``None``.
                When ``schema`` is a list of column names or ``None``, the schema of the
                DataFrame will be inferred from the data across all rows. To improve
                performance, provide a schema. This avoids the need to infer data types
                with large data sets.

        Examples::

            >>> # create a dataframe with a schema
            >>> from clickzetta.zettapark.types import IntegerType, StringType, StructField
            >>> schema = StructType([StructField("a", IntegerType()), StructField("b", StringType())])
            >>> session.create_dataframe([[1, "alice"], [3, "bob"]], schema).collect()
            [Row(A=1, B='alice'), Row(A=3, B='bob')]

            >>> # create a dataframe by inferring a schema from the data
            >>> from clickzetta.zettapark import Row
            >>> # infer schema
            >>> session.create_dataframe([1, 2, 3, 4], schema=["a"]).collect()
            [Row(A=1), Row(A=2), Row(A=3), Row(A=4)]
            >>> session.create_dataframe([[1, 2, 3, 4]], schema=["a", "b", "c", "d"]).collect()
            [Row(A=1, B=2, C=3, D=4)]
            >>> session.create_dataframe([[1, 2], [3, 4]], schema=["a", "b"]).collect()
            [Row(A=1, B=2), Row(A=3, B=4)]
            >>> session.create_dataframe([Row(a=1, b=2, c=3, d=4)]).collect()
            [Row(A=1, B=2, C=3, D=4)]
            >>> session.create_dataframe([{"a": 1}, {"b": 2}]).collect()
            [Row(A=1, B=None), Row(A=None, B=2)]

            >>> # create a dataframe from a pandas Dataframe
            >>> import pandas as pd
            >>> session.create_dataframe(pd.DataFrame([(1, 2, 3, 4)], columns=["a", "b", "c", "d"])).collect()
            [Row(a=1, b=2, c=3, d=4)]

        Note:
            When `data` is a pandas DataFrame, `clickzetta.connector.pandas_tools.write_pandas` is called, which
            requires permission to (1) CREATE STAGE (2) CREATE TABLE and (3) CREATE FILE FORMAT under the current
            database and schema.
        """
        if data is None:
            raise ValueError("data cannot be None.")

        # check the type of data
        if isinstance(data, Row):
            raise TypeError("create_dataframe() function does not accept a Row object.")

        if not isinstance(data, (list, tuple)) and (
            not installed_pandas
            or (installed_pandas and not isinstance(data, pandas.DataFrame))
        ):
            raise TypeError(
                "create_dataframe() function only accepts data as a list, tuple or a pandas DataFrame."
            )

        # check to see if it is a pandas DataFrame and if so, write that to a temp
        # table and return as a DataFrame
        if installed_pandas and isinstance(data, pandas.DataFrame):
            temp_table_name = escape_quotes(
                random_name_for_temp_object(TempObjectType.TABLE)
            )
            try:
                database = self._conn._get_current_parameter("database", quoted=False)
            except AttributeError:
                database = self._conn._lower_case_parameters("workspace")

            try:
                schema = self._conn._get_current_parameter("schema", quoted=False)
            except AttributeError:
                database = self._conn._lower_case_parameters("schema")

            t = self.write_pandas(
                data,
                temp_table_name,
                database=database,
                schema=schema,
                quote_identifiers=True,
                auto_create_table=True,
                table_type="temporary",
                use_logical_type=self._use_logical_type_for_create_df,
            )
            set_api_call_source(t, "Session.create_dataframe[pandas]")
            return t

        # infer the schema based on the data
        names = None
        schema_query = None
        if isinstance(schema, StructType):
            new_schema = schema
            # SELECT query has an undefined behavior for nullability, so if the schema requires non-nullable column and
            # all columns are primitive type columns, we use a temp table to lock in the nullabilities.
            if any([field.nullable is False for field in schema.fields]) and all(
                [field.datatype.is_primitive() for field in schema.fields]
            ):
                temp_table_name = random_name_for_temp_object(TempObjectType.TABLE)
                schema_string = analyzer_utils.attribute_to_schema_string(
                    schema._to_attributes()
                )
                try:
                    self._register_temp_object(
                        TempObjectType.TABLE,
                        self.get_fully_qualified_name_if_possible(temp_table_name),
                    )
                    self._run_query(
                        f"CREATE TABLE {self.get_fully_qualified_name_if_possible(temp_table_name)} ({schema_string})"
                    )
                    schema_query = f"SELECT * FROM {self.get_fully_qualified_name_if_possible(temp_table_name)}"
                except ProgrammingError as e:
                    logging.debug(
                        f"Cannot create temp table for specified non-nullable schema, fall back to using schema "
                        f"string from select query. Exception: {str(e)}"
                    )
        else:
            if not data:
                raise ValueError("Cannot infer schema from empty data")
            if isinstance(schema, Iterable):
                names = list(schema)
            new_schema = reduce(
                merge_type,
                (infer_schema(row, names) for row in data),
            )
        if len(new_schema.fields) == 0:
            raise ValueError(
                "The provided schema or inferred schema cannot be None or empty"
            )

        def convert_row_to_list(
            row: Union[Iterable[Any], Any], names: List[str]
        ) -> List:
            row_dict = None
            if row is None:
                row = [None]
            elif isinstance(row, (tuple, list)):
                if not row:
                    row = [None]
                elif getattr(row, "_fields", None):  # Row or namedtuple
                    row_dict = row.as_dict() if isinstance(row, Row) else row._asdict()
            elif isinstance(row, dict):
                row_dict = row.copy()
            else:
                row = [row]

            if row_dict:
                # fill None if the key doesn't exist
                row_dict = {quote_name(k): v for k, v in row_dict.items()}
                return [row_dict.get(name) for name in names]
            else:
                # check the length of every row, which should be same across data
                if len(row) != len(names):
                    raise ValueError(
                        f"{len(names)} fields are required by schema "
                        f"but {len(row)} values are provided. This might be because "
                        f"data consists of rows with different lengths, or mixed rows "
                        f"with column names or without column names"
                    )
                return list(row)

        # always overwrite the column names if they are provided via schema
        if not names:
            names = [f.name for f in new_schema.fields]
        quoted_names = [quote_name(name) for name in names]
        rows = [convert_row_to_list(row, quoted_names) for row in data]

        # get attributes and data types
        attrs, data_types = [], []
        for field, quoted_name in zip(new_schema.fields, quoted_names):
            # data_type = (
            #     StringType()
            #     if isinstance(
            #         field.datatype,
            #         (
            #             VariantType,
            #             ArrayType,
            #             MapType,
            #             VectorType,
            #         ),
            #     )
            #     else field.datatype
            # )
            data_type = field.datatype
            if not isinstance(data_type, DataType):
                raise TypeError(
                    f"Type of field {field.name} ({data_type}) is not a DataType"
                )
            attrs.append(Attribute(quoted_name, data_type, field.nullable))
            data_types.append(field.datatype)

        converted = []
        for row in rows:
            converted.append(Row(*row))
        project_columns = [column(name) for name in names]

        if self.sql_simplifier_enabled:
            df = DataFrame(
                self,
                self._analyzer.create_select_statement(
                    from_=self._analyzer.create_select_query_plan(
                        Values(attrs, converted, schema_query=schema_query),
                        analyzer=self._analyzer,
                    ),
                    analyzer=self._analyzer,
                ),
            ).select(project_columns)
        else:
            df = DataFrame(
                self, Values(attrs, converted, schema_query=schema_query)
            ).select(project_columns)
        set_api_call_source(df, "Session.create_dataframe[values]")

        return df

    def range(self, start: int, end: Optional[int] = None, step: int = 1) -> DataFrame:
        """
        Creates a new DataFrame from a range of numbers. The resulting DataFrame has
        single column named ``ID``, containing elements in a range from ``start`` to
        ``end`` (exclusive) with the step value ``step``.

        Args:
            start: The start of the range. If ``end`` is not specified,
                ``start`` will be used as the value of ``end``.
            end: The end of the range.
            step: The step of the range.

        Examples::

            >>> session.range(10).collect()
            [Row(ID=0), Row(ID=1), Row(ID=2), Row(ID=3), Row(ID=4), Row(ID=5), Row(ID=6), Row(ID=7), Row(ID=8), Row(ID=9)]
            >>> session.range(1, 10).collect()
            [Row(ID=1), Row(ID=2), Row(ID=3), Row(ID=4), Row(ID=5), Row(ID=6), Row(ID=7), Row(ID=8), Row(ID=9)]
            >>> session.range(1, 10, 2).collect()
            [Row(ID=1), Row(ID=3), Row(ID=5), Row(ID=7), Row(ID=9)]
        """
        range_plan = Range(0, start, step) if end is None else Range(start, end, step)

        if self.sql_simplifier_enabled:
            df = DataFrame(
                self,
                self._analyzer.create_select_statement(
                    from_=self._analyzer.create_select_query_plan(
                        range_plan, analyzer=self._analyzer
                    ),
                    analyzer=self._analyzer,
                ),
            )
        else:
            df = DataFrame(self, range_plan)
        set_api_call_source(df, "Session.range")
        return df

    def create_async_job(self, query_id: str) -> AsyncJob:
        """
        Creates an :class:`AsyncJob` from a query ID.

        See also:
            :class:`AsyncJob`
        """
        if (
            is_in_stored_procedure()
            and not self._conn._get_client_side_session_parameter(
                "ENABLE_ASYNC_QUERY_IN_PYTHON_STORED_PROCS", False
            )
        ):  # pragma: no cover
            raise NotImplementedError(
                "Async query is not supported in stored procedure yet"
            )
        return AsyncJob(query_id, None, self)

    def get_current_account(self) -> Optional[str]:
        """
        Returns the name of the current account for the Python connector session attached
        to this session.
        """
        return self._conn._get_current_parameter("account")

    def get_current_user(self) -> Optional[str]:
        """
        Returns the name of the user in the connection to ClickZetta attached
        to this session.
        """
        return self._conn._get_current_parameter("user")

    def get_current_database(self) -> Optional[str]:
        """
        Returns the name of the current database for the Python connector session attached
        to this session. See the example in :meth:`table`.
        """
        return self._conn._get_current_parameter("database")

    def get_current_schema(self) -> Optional[str]:
        """
        Returns the name of the current schema for the Python connector session attached
        to this session. See the example in :meth:`table`.
        """
        return self._conn._get_current_parameter("schema")

    @deprecated(version="1.14.0")
    def get_fully_qualified_current_schema(self) -> str:
        """Returns the fully qualified name of the current schema for the session."""
        return self.get_fully_qualified_name_if_possible("")[:-1]

    def get_fully_qualified_name_if_possible(
        self, name: Union[str, List[str], Tuple[str]]
    ) -> str:
        """
        Returns the fully qualified object name if current database/schema exists, otherwise returns the object name
        """
        if len(name) == 0:
            raise ValueError("Empty name")
        database = self.get_current_database()
        schema = self.get_current_schema()
        if isinstance(name, (List, Tuple)):
            database = name[-3] if len(name) >= 3 else database
            schema = name[-2] if len(name) >= 2 else schema
            name = name[-1]
        if database and schema:
            return f"`{database}`.`{schema}`.`{name}`"

        # In stored procedure, there are scenarios like bundle where we allow empty current schema
        if not is_in_stored_procedure():
            missing_item = "DATABASE" if not database else "SCHEMA"
            raise ZettaparkClientExceptionMessages.SERVER_CANNOT_FIND_CURRENT_DB_OR_SCHEMA(
                missing_item, missing_item, missing_item
            )
        return name

    def get_current_warehouse(self) -> Optional[str]:
        """
        Returns the name of the warehouse in use for the current session.
        """
        return self._conn._get_current_parameter("warehouse")

    def get_current_role(self) -> Optional[str]:
        """
        Returns the name of the primary role in use for the current session.
        """
        return self._conn._get_current_parameter("role")

    def use_database(self, database: str) -> None:
        """Specifies the active/current database for the session.

        Args:
            database: The database name.
        """
        self._use_object(database, "database")

    def use_schema(self, schema: str) -> None:
        """Specifies the active/current schema for the session.

        Args:
            schema: The schema name.
        """
        self._use_object(schema, "schema")

    def use_warehouse(self, warehouse: str) -> None:
        """Specifies the active/current warehouse for the session.

        Args:
            warehouse: the warehouse name.
        """
        self._use_object(warehouse, "warehouse")

    def use_role(self, role: str) -> None:
        """Specifies the active/current primary role for the session.

        Args:
            role: the role name.
        """
        self._use_object(role, "role")

    def use_secondary_roles(self, roles: Optional[Literal["all", "none"]]) -> None:
        """
        Specifies the active/current secondary roles for the session.
        The currently-active secondary roles set the context that determines whether
        the current user has the necessary privileges to perform SQL actions.

        Args:
            roles: "all" or "none". ``None`` means "none".

        References: `command USE SECONDARY ROLES <https://doc.clickzetta.com/>`_.
        """
        self._run_query(
            f"use secondary roles {'none' if roles is None else roles.lower()}"
        )

    def _use_object(self, object_name: str, object_type: str) -> None:
        if object_name:
            validate_object_name(object_name)
            self._conn._conn.use_object(object_name, object_type)
        else:
            raise ValueError(f"'{object_type}' must not be empty or None.")

    @property
    def telemetry_enabled(self) -> bool:
        """Controls whether or not the Zettapark client sends usage telemetry to ClickZetta.
        This typically includes information like the API calls invoked, libraries used in conjunction with Zettapark,
        and information that will let us better diagnose and fix client side errors.

        The default value is ``True``.

        Example::

            >>> session.telemetry_enabled
            True
            >>> session.telemetry_enabled = False
            >>> session.telemetry_enabled
            False
            >>> session.telemetry_enabled = True
            >>> session.telemetry_enabled
            True
        """
        return self._conn._conn.telemetry_enabled

    @telemetry_enabled.setter
    def telemetry_enabled(self, value):
        # Set both in-band and out-of-band telemetry to True/False
        if value:
            self._conn._conn.telemetry_enabled = True
            self._conn._telemetry_client.telemetry._enabled = True
        else:
            self._conn._conn.telemetry_enabled = False
            self._conn._telemetry_client.telemetry._enabled = False

    @property
    def file(self) -> FileOperation:
        """
        Returns a :class:`FileOperation` object that you can use to perform file operations on stages.
        See details of how to use this object in :class:`FileOperation`.
        """
        return self._file

    @property
    def udf(self) -> UDFRegistration:
        """
        Returns a :class:`udf.UDFRegistration` object that you can use to register UDFs.
        See details of how to use this object in :class:`udf.UDFRegistration`.
        """
        return self._udf_registration

    @property
    def udtf(self) -> UDTFRegistration:
        """
        Returns a :class:`udtf.UDTFRegistration` object that you can use to register UDTFs.
        See details of how to use this object in :class:`udtf.UDTFRegistration`.
        """
        return self._udtf_registration

    @property
    @private_preview(version="1.6.0")
    def udaf(self) -> UDAFRegistration:
        """
        Returns a :class:`udaf.UDAFRegistration` object that you can use to register UDAFs.
        See details of how to use this object in :class:`udaf.UDAFRegistration`.
        """
        return self._udaf_registration

    @property
    def sproc(self) -> StoredProcedureRegistration:
        """
        Returns a :class:`stored_procedure.StoredProcedureRegistration` object that you can use to register stored procedures.
        See details of how to use this object in :class:`stored_procedure.StoredProcedureRegistration`.
        """
        return self._sp_registration

    def _infer_is_return_table(
        self, sproc_name: str, *args: Any, log_on_exception: bool = False
    ) -> bool:
        func_signature = ""
        try:
            arg_types = []
            for arg in args:
                if isinstance(arg, Column):
                    expr = arg._expression
                    if isinstance(expr, Cast):
                        arg_types.append(convert_data_type_to_name(expr.to))
                    else:
                        arg_types.append(convert_data_type_to_name(expr.datatype))
                else:
                    arg_types.append(convert_data_type_to_name(infer_type(arg)))
            func_signature = f"{sproc_name.upper()}({', '.join(arg_types)})"

            # describe procedure returns two column table with columns - property and value
            # the second row in the sproc_desc is property=returns and value=<return type of procedure>
            # when no procedure of the signature is found, SQL exception is raised
            sproc_desc = self._run_query(
                f"describe procedure {func_signature}",
                log_on_exception=log_on_exception,
            )
            return_type = sproc_desc[1][1]
            return return_type.upper().startswith("TABLE")
        except Exception as exc:
            _logger.info(
                f"Could not describe procedure {func_signature} due to exception {exc}"
            )
        return False

    def call(
        self,
        sproc_name: str,
        *args: Any,
        statement_params: Optional[Dict[str, Any]] = None,
        log_on_exception: bool = False,
    ) -> Any:
        """Calls a stored procedure by name.

        Args:
            sproc_name: The name of stored procedure in ClickZetta.
            args: Arguments should be basic Python types.
            statement_params: Dictionary of statement level parameters to be set while executing this action.
            log_on_exception: Log warnings if they arise when trying to determine if the stored procedure
                as a table return type.

        Example::

            >>> import clickzetta.zettapark
            >>> from clickzetta.zettapark.functions import sproc
            >>>
            >>> session.add_packages('clickzetta-zettapark-python')
            >>>
            >>> @sproc(name="my_copy_sp", replace=True)
            ... def my_copy(session: clickzetta.zettapark.Session, from_table: str, to_table: str, count: int) -> str:
            ...     session.table(from_table).limit(count).write.save_as_table(to_table)
            ...     return "SUCCESS"
            >>> _ = session.sql("create table test_from(test_str varchar) as select randstr(20, random()) from table(generator(rowCount => 100))").collect()
            >>> _ = session.sql("drop table if exists test_to").collect()
            >>> session.call("my_copy_sp", "test_from", "test_to", 10)
            'SUCCESS'
            >>> session.table("test_to").count()
            10

        Example::

            >>> from clickzetta.zettapark.dataframe import DataFrame
            >>>
            >>> @sproc(name="my_table_sp", replace=True)
            ... def my_table(session: clickzetta.zettapark.Session, x: int, y: int, col1: str, col2: str) -> DataFrame:
            ...     return session.sql(f"select {x} as {col1}, {y} as {col2}")
            >>> session.call("my_table_sp", 1, 2, "a", "b").show()
            -------------
            |"A"  |"B"  |
            -------------
            |1    |2    |
            -------------
            <BLANKLINE>
        """
        return self._call(
            sproc_name,
            *args,
            statement_params=statement_params,
            log_on_exception=log_on_exception,
        )

    def _call(
        self,
        sproc_name: str,
        *args: Any,
        statement_params: Optional[Dict[str, Any]] = None,
        is_return_table: Optional[bool] = None,
        log_on_exception: bool = False,
    ) -> Any:
        """Private implementation of session.call

        Args:
            sproc_name: The name of stored procedure in ClickZetta.
            args: Arguments should be basic Python types.
            statement_params: Dictionary of statement level parameters to be set while executing this action.
            is_return_table: When set to a non-null value, it signifies whether the return type of sproc_name
                is a table return type. This skips infer check and returns a dataframe with appropriate sql call.
        """
        validate_object_name(sproc_name)
        query = generate_call_python_sp_sql(self, sproc_name, *args)

        if is_return_table is None:
            is_return_table = self._infer_is_return_table(
                sproc_name, *args, log_on_exception=log_on_exception
            )
        if is_return_table:
            qid = self._conn.execute_and_get_job_id(
                query, statement_params=statement_params
            )
            df = self.sql(result_scan_statement(qid))
            set_api_call_source(df, "Session.call")
            return df

        df = self.sql(query)
        set_api_call_source(df, "Session.call")
        return df.collect(statement_params=statement_params)[0][0]

    @deprecated(
        version="0.7.0",
        extra_warning_text="Use `Session.table_function()` instead.",
        extra_doc_string="Use :meth:`table_function` instead.",
    )
    def flatten(
        self,
        input: ColumnOrName,
        path: Optional[str] = None,
        outer: bool = False,
        recursive: bool = False,
        mode: str = "BOTH",
    ) -> DataFrame:
        """Creates a new :class:`DataFrame` by flattening compound values into multiple rows.

        The new :class:`DataFrame` will consist of the following columns:

            - SEQ
            - KEY
            - PATH
            - INDEX
            - VALUE
            - THIS

        References: `SQL function FLATTEN <https://doc.clickzetta.com/>`_.

        Example::

            df = session.flatten(parse_json(lit('{"a":[1,2]}')), "a", False, False, "BOTH")

        Args:
            input: The name of a column or a :class:`Column` instance that will be unseated into rows.
                The column data must be of ClickZetta data type VARIANT, OBJECT, or ARRAY.
            path: The path to the element within a VARIANT data structure which needs to be flattened.
                The outermost element is to be flattened if path is empty or ``None``.
            outer: If ``False``, any input rows that cannot be expanded, either because they cannot be accessed in the ``path``
                or because they have zero fields or entries, are completely omitted from the output.
                Otherwise, exactly one row is generated for zero-row expansions
                (with NULL in the KEY, INDEX, and VALUE columns).
            recursive: If ``False``, only the element referenced by ``path`` is expanded.
                Otherwise, the expansion is performed for all sub-elements recursively.
            mode: Specifies which types should be flattened "OBJECT", "ARRAY", or "BOTH".

        Returns:
            A new :class:`DataFrame` that has the flattened new columns and new rows from the compound data.

        Example::

            >>> from clickzetta.zettapark.functions import lit, parse_json
            >>> session.flatten(parse_json(lit('{"a":[1,2]}')), path="a", outer=False, recursive=False, mode="BOTH").show()
            -------------------------------------------------------
            |"SEQ"  |"KEY"  |"PATH"  |"INDEX"  |"VALUE"  |"THIS"  |
            -------------------------------------------------------
            |1      |NULL   |a[0]    |0        |1        |[       |
            |       |       |        |         |         |  1,    |
            |       |       |        |         |         |  2     |
            |       |       |        |         |         |]       |
            |1      |NULL   |a[1]    |1        |2        |[       |
            |       |       |        |         |         |  1,    |
            |       |       |        |         |         |  2     |
            |       |       |        |         |         |]       |
            -------------------------------------------------------
            <BLANKLINE>

        See Also:
            - :meth:`DataFrame.flatten`, which creates a new :class:`DataFrame` by exploding a VARIANT column of an existing :class:`DataFrame`.
            - :meth:`Session.table_function`, which can be used for any ClickZetta table functions, including ``flatten``.
        """
        mode = mode.upper()
        if mode not in ("OBJECT", "ARRAY", "BOTH"):
            raise ValueError("mode must be one of ('OBJECT', 'ARRAY', 'BOTH')")
        if isinstance(input, str):
            input = col(input)
        df = DataFrame(
            self,
            TableFunctionRelation(
                FlattenFunction(input._expression, path, outer, recursive, mode)
            ),
        )
        set_api_call_source(df, "Session.flatten")
        return df

    def query_history(self) -> QueryHistory:
        """Create an instance of :class:`QueryHistory` as a context manager to record queries that are pushed down to the ClickZetta database.

        >>> with session.query_history() as query_history:
        ...     df = session.create_dataframe([[1, 2], [3, 4]], schema=["a", "b"])
        ...     df = df.filter(df.a == 1)
        ...     res = df.collect()
        >>> assert len(query_history.queries) == 1
        """
        query_listener = QueryHistory(self)
        self._conn.add_query_listener(query_listener)
        return query_listener

    def _table_exists(self, raw_table_name: Iterable[str]):
        if len(raw_table_name) > 3:
            raise ZettaparkClientExceptionMessages.GENERAL_INVALID_OBJECT_NAME(
                ".".join(raw_table_name)
            )
        sql = (
            "SELECT `table_name` FROM ( SHOW TABLES "
            + (
                (" IN " + ".".join(f"`{i}`" for i in raw_table_name[:-1]))
                if len(raw_table_name) > 1
                else ""
            )
            + f" ) WHERE `table_name` = '{raw_table_name[-1]}'"
        )
        tables = self._run_query(sql)
        return tables is not None and len(tables) > 0

    def _explain_query(self, query: str) -> Optional[str]:
        try:
            return self._run_query(f"explain {query}")[0][1]
        # return None for queries which can't be explained
        except ProgrammingError:
            _logger.warning("query `%s` cannot be explained", query)
            return None

    createDataFrame = create_dataframe
