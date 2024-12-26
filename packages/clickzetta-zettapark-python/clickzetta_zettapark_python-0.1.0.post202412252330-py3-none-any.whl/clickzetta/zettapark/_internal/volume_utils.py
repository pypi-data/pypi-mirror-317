#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
# Copyright (c) 2023-2024 Yunqi Inc. All rights reserved.
#

import re
from enum import Enum
from typing import Any, Dict, List, NamedTuple, Optional


class _VolumeType(Enum):
    EXTERNAL = "external"
    TABLE = "table"
    USER = "user"


class _VolumeUri(NamedTuple):
    name: str
    type: _VolumeType
    path: str

    @property
    def volume_identifier(self) -> str:
        name_parts = self.name.split(".")
        quoted_name = ".".join(f"`{n}`" if "`" not in n else n for n in name_parts)
        if self.type == _VolumeType.EXTERNAL:
            return f"VOLUME {quoted_name}"
        if self.type == _VolumeType.TABLE:
            return f"TABLE VOLUME {quoted_name}"
        if self.type == _VolumeType.USER:
            return "USER VOLUME"
        raise ValueError(f"Unknown volume type: {self.type}")

    @property
    def subdir(self) -> str:
        if self.path == "":
            return "SUBDIRECTORY '/'"
        elif self.path.endswith("/"):
            return f"SUBDIRECTORY '{self.path}'"
        raise ValueError("Path must end with '/'")

    @property
    def subdir_or_file(self) -> str:
        if self.path == "":
            return "SUBDIRECTORY '/'"
        elif self.path.endswith("/"):
            return f"SUBDIRECTORY '{self.path}'"
        return f"FILE '{self.path}'"

    def path_filter_clause(self, pattern: Optional[str] = None) -> str:
        if not self.path.endswith("/"):
            return f"FILES ('{self.path}')"
        regexp_clause = f" REGEXP '{pattern}'" if pattern else ""
        return f"SUBDIRECTORY '{self.path}' {regexp_clause}"


_VOLUME_URL_PATTERN = re.compile(r"^volume(:\w+)?://([^/]+)(/.*)$", re.IGNORECASE)


def _parse_volume_uri(uri: str) -> Optional[_VolumeUri]:
    matched = _VOLUME_URL_PATTERN.match(uri)
    if matched is None:
        return None
    scheme_part, name, path = matched.groups()
    if scheme_part is None:
        type_ = _VolumeType.EXTERNAL
    elif scheme_part.lower() == ":table":
        type_ = _VolumeType.TABLE
    elif scheme_part.lower() == ":user":
        type_ = _VolumeType.USER
    elif scheme_part is not None:
        raise ValueError(f"Invalid volume uri: {uri}")
    return _VolumeUri(name=name, type=type_, path=path)


def to_options_clause(options: Optional[Dict[str, Any]]) -> str:
    def _value(v: Any) -> str:
        if isinstance(v, list):
            return "(" + ", ".join(_value(e) for e in v) + ")"
        return v

    return " ".join(f"{k} = {_value(v)}" for k, v in options.items()) if options else ""


def to_table_options_clause(options: Optional[Dict[str, Any]]) -> str:
    # TODO escape special characters in options
    return (
        "OPTIONS (" + ", ".join(f"'{k}' = '{str(v)}'" for k, v in options.items()) + ")"
        if options
        else ""
    )


def select_from_volume(
    project: List[str],
    volume_uri: str,
    format_name: str,
    pattern: Optional[str],
    schema_string: Optional[str],
    file_format_options: Dict[str, Any],
) -> str:
    uri = _parse_volume_uri(volume_uri)
    if not uri:
        raise ValueError(f"Invalid volume uri: {volume_uri}")
    return (
        f"SELECT * "
        f"FROM {uri.volume_identifier} "
        f"({schema_string}) "
        f"{to_table_options_clause(file_format_options)} "
        f"USING {format_name} "
        f"{uri.path_filter_clause()}"
    )


def copy_into_volume(
    query: str,
    volume_uri: str,
    partition_by: Optional[str] = None,
    file_format_name: Optional[str] = None,
    file_format_type: Optional[str] = None,
    format_type_options: Optional[Dict[str, Any]] = None,
    header: bool = False,
    **copy_options: Any,
) -> str:
    if partition_by is not None:
        raise ValueError("partition_by is not supported for copy into volume")
    if file_format_name is not None:
        raise ValueError("file_format_name is not supported for copy into volume")
    uri = _parse_volume_uri(volume_uri)
    if not uri:
        raise ValueError(f"Invalid volume uri: {volume_uri}")
    if not uri.path.endswith("/"):
        raise ValueError("Invalid volume uri: path not ends with '/'")
    return (
        f"COPY INTO {uri.volume_identifier} SUBDIRECTORY '{uri.path}' "
        f"FROM ({query}) "
        f"FILE_FORMAT = (TYPE = {file_format_type or 'CSV'} "
        f"{to_options_clause(format_type_options)}) "
        f"{to_options_clause(copy_options)}"
    )


def volume_file_operation_statement(
    command: str,
    file_name: str,
    volume_uri: str,
    options: Optional[Dict[str, str]] = None,
) -> str:
    uri = _parse_volume_uri(volume_uri)
    if not uri:
        raise ValueError(f"Invalid volume uri: {volume_uri}")
    file_name = (
        file_name.replace("'file://", "'", 1)
        if file_name.startswith("'file://")
        else file_name
    )
    if command.lower() == "put":
        return f"PUT {file_name} TO {uri.volume_identifier} {uri.subdir_or_file} {to_options_clause(options)}"
    if command.lower() == "get":
        return f"GET {uri.volume_identifier} {uri.subdir_or_file} TO {file_name} {to_options_clause(options)}"
    if command.lower() == "list":
        return f"LIST {uri.volume_identifier} {uri.subdir} {to_options_clause(options)}"
    if command.lower() == "delete":
        return f"DELETE {uri.volume_identifier} {uri.subdir_or_file} {to_options_clause(options)}"
    if command.lower() == "copy_files":
        dest_uri = uri
        src_uri = _parse_volume_uri(file_name)
        if not src_uri:
            raise ValueError(f"Invalid volume uri: {file_name}")
        return (
            f"COPY FILES "
            f"INTO {dest_uri.volume_identifier} {dest_uri.subdir} "
            f"FROM {src_uri.volume_identifier} {src_uri.subdir} "
            f"{to_options_clause(options)}"
        )

    raise ValueError(f"Unsupported file operation type {command}")
