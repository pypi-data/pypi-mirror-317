#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
# Copyright (c) 2023-2024 Yunqi Inc. All rights reserved.
#

import functools
import importlib
import io
from logging import getLogger
from typing import IO, Dict, Optional, Sequence, Tuple

import requests

import clickzetta.connector
import clickzetta.connector.version
from clickzetta.connector.v0 import connection, cursor, exceptions
from clickzetta.zettapark._internal.volume_utils import _parse_volume_uri
from clickzetta.zettapark.exceptions import (
    ZettaparkSQLException,
    ZettaparkUploadFileException,
)

_logger = getLogger(__name__)


ResultMetadata = cursor.Column


def _parse_version() -> Tuple[str]:
    parts = clickzetta.connector.version.__version__.split(".")
    numbers = [int(part) for part in parts]
    if len(numbers) < 4:
        numbers += [0] * (4 - len(numbers))
    return tuple(numbers)


CONNECTOR_VERSION = _parse_version()


class DatabaseError(exceptions.DatabaseError):
    def __init__(
        self,
        msg: Optional[str] = None,
        errno: Optional[int] = None,
        job_id: Optional[str] = None,
        query: Optional[str] = None,
    ) -> None:
        self.raw_msg = msg
        self.errno = errno or -1
        self.msg = f"{self.errno:06d}: {self.errno}: {msg}"
        self.job_id = job_id
        self.query = query


class IntegrityError(DatabaseError):
    ...


class NotSupportedError(DatabaseError):
    ...


class OperationalError(DatabaseError):
    ...


class ProgrammingError(DatabaseError):
    ...


class ReauthenticationRequest(Exception):
    def __init__(self, cause) -> None:
        self.cause = cause


def _raise_on_closed(exc_msg, exc_class=ProgrammingError, closed_attr_name="_closed"):
    def _wrap_method(method):
        def _wrapper(self, *args, **kwargs):
            if getattr(self, closed_attr_name):
                raise exc_class(exc_msg)
            return method(self, *args, **kwargs)

        functools.update_wrapper(_wrapper, method)
        return _wrapper

    def _wrap_class(class_):
        for name in dir(class_):
            if name == "is_closed":
                continue
            if name.startswith("_") and name != "__iter__":
                continue
            member = getattr(class_, name)
            if not callable(member):
                continue
            if isinstance(class_.__dict__[name], (staticmethod, classmethod)):
                continue
            member = _wrap_method(member)
            setattr(class_, name, member)

        return class_

    return _wrap_class


_OBJECT_TYPE_ALIAS = {"database": "workspace", "warehouse": "vcluster"}


class ClickzettaCursor(cursor.Cursor):
    def __init__(self, connection) -> None:
        super().__init__(connection)
        self._ignore_executemany_error = False

    def execute(self, operation, parameters=None):
        try:
            return super().execute(operation, binding_params=parameters)
        except Exception as exc:
            if isinstance(exc, TypeError):
                raise exc
            raise ZettaparkSQLException(str(exc))
        finally:
            _logger.debug("Executed query: %s", operation)

    def executemany(self, operation: str, parameters: Sequence):
        try:
            return super().executemany(operation, seqparams=parameters)
        except BaseException:
            if not self._ignore_executemany_error:
                raise
            self.query = operation
            self.job_id = "fake_id"


class ByteCountingStream(io.IOBase):
    def __init__(self, input_stream) -> None:
        self.input_stream = input_stream
        self.bytes_read = 0

    def read(self, size=-1):
        data = self.input_stream.read(size)
        self.bytes_read += len(data)
        return data

    def readinto(self, b):
        bytes_read = self.input_stream.readinto(b)
        self.bytes_read += bytes_read
        return bytes_read

    def __getattr__(self, name):
        return getattr(self.input_stream, name)


class ClickzettaConnection(connection.Connection):
    def __init__(self, client=None) -> None:
        super().__init__(client)
        self._session_parameters = {}
        self._client_prefetch_threads = 1

    def use_object(self, object_name: str, object_type: str) -> None:
        object_type = _OBJECT_TYPE_ALIAS.get(object_type, object_type)
        getattr(self._client, object_type)
        setattr(self._client, object_type, object_name)

    def get_current_parameter(self, param: str) -> Optional[str]:
        param = _OBJECT_TYPE_ALIAS.get(param, param)
        return getattr(self._client, param)

    def is_closed(self) -> bool:
        return self._closed

    # Zettapark requires close() safe to be called multiple times
    def close(self):
        if not self._closed:
            super().close()

    @property
    def expired(self) -> bool:
        return self._closed

    def cursor(self):
        # TODO(guantao.gao) pass a cursor factory to _ConnectorConnection for creating cursor
        # in order to decouple from connector
        if self._client.username is not None and self._client.password is not None:
            self._client.refresh_token()
        new_cursor = ClickzettaCursor(self)
        self._cursors_created.add(new_cursor)
        return new_cursor

    def upload_stream(
        self,
        input_stream: IO[bytes],
        volume_location: str,
        *,
        parallel: int = 4,
        compress_data=False,
        source_compression: Optional[str] = None,
        overwrite=False,
    ) -> Dict:
        uri = _parse_volume_uri(volume_location)
        if not uri:
            raise ValueError(f"Invalid volume URI: {volume_location}")
        if uri.path.endswith("/"):
            raise ValueError(f"Invalid volume URI: not a file path: {volume_location}")

        with self.cursor() as cursor:
            cursor.execute(
                f"SELECT get_presigned_url({uri.volume_identifier}, '{uri.path}', 1800, 'PUT')",
            )
            put_url = cursor.fetchone()[0]
            # a workaround
            if "-internal.aliyuncs.com/" in put_url:
                put_url = put_url.replace("-internal.aliyuncs.com/", ".aliyuncs.com/")
            input_stream = ByteCountingStream(input_stream)
            _logger.debug(f"Uploading to {put_url}...")
            try:
                r = requests.put(put_url, data=input_stream, headers={}, timeout=60)
            except requests.exceptions.Timeout:
                raise ZettaparkUploadFileException(
                    f"Failed to upload file to {volume_location}: Timeout"
                )
            except BaseException as exc:
                raise ZettaparkUploadFileException(
                    f"Failed to upload file to {volume_location}: {str(exc)}"
                )
            if r.status_code >= 400:
                raise ZettaparkUploadFileException(
                    f"Failed to upload file to {volume_location}: {r.text}"
                )
            return {
                "source": "-",
                "target": uri.path,
                "source_size": input_stream.bytes_read,
                "target_size": input_stream.bytes_read,
                "source_compression": "NONE",
                "target_compression": "NONE",
                "status": "UPLOADED",
                "message": "",
            }


@_raise_on_closed("Operating on a closed connection")
def clickzetta_connect(**kwargs) -> ClickzettaConnection:
    conn = connection.connect(**kwargs)
    client = conn._client
    return ClickzettaConnection(client)


class MissingPandas:
    def __getattr__(self, item):
        raise ProgrammingError("pandas is not installed")


try:
    pandas = importlib.import_module("pandas")
    installed_pandas = True
except ImportError:
    pandas = MissingPandas()
    installed_pandas = False
