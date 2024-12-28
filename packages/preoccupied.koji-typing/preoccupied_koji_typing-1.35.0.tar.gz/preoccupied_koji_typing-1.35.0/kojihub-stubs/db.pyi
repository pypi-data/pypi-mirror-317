# This library is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This library is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this library; if not, see <http://www.gnu.org/licenses/>.


"""
Koji Hub - typing stubs

Typing annotations stub for kojihub.db

:author: Christopher O'Brien <obriencj@gmail.com>
:license: GPL v3
"""


from logging import Logger
from psycopg2.extensions import (
    connection as Connection, cursor as Cursor, )
from re import Pattern
from typing import (
    Any, Callable, Dict, Iterator, List, Optional, Sequence,
    Set, Tuple, Union, )

from koji_types import Data, EventID, UserID
from koji_types.context import ThreadLocal
from koji_types.hub import QueryProcessorOptions


NAMED_RE: Pattern
POSITIONAL_RE: Pattern

context: ThreadLocal
logger: Logger


def connect() -> "DBWrapper":
    ...

def convert_timestamp(ts: int) -> str:
    ...

def currval(sequence: str) -> int:
    ...

def db_lock(
        name: str,
        wait: bool = True) -> bool:
    ...

def getDBopts() -> Dict[str, Any]:
    ...

def get_event() -> EventID:
    ...

def nextval(sequence: str) -> int:
    ...

def provideDBopts(**opts) -> None:
    ...

def setDBopts(**opts) -> None:
    ...


class BulkInsertProcessor:

    batch: int
    columns: Set[str]
    data: List[Data]
    table: str
    strict: bool

    def __init__(
            self,
            table: str,
            data: Optional[List[Data]] = None,
            columns: Optional[List[str]] = None,
            strict: bool = True,
            batch: int = 1000) -> None:
        ...

    def add_record(
            self,
            **kwargs) -> None:
        ...

    def execute(self) -> None:
        ...


class BulkUpdateProcessor:

    data: List[Data]
    table: str
    match_keys: List[str]

    def __init__(
            self,
            table: str,
            data: Optional[List[Data]] = None,
            match_keys: Optional[List[str]] = None) -> None:
        ...

    def execute(self) -> int:
        ...

    def get_keys(self) -> Tuple[List[str], List[str]]:
        ...

    def get_sql(self) -> str:
        ...


class CursorWrapper:

    cursor: Cursor
    logger: Logger

    def __init__(self, cursor: Cursor) -> None:
        ...

    def __getattr__(self, key: str) -> Any:
        ...

    def execute(
            self,
            operation: str,
            parameters: Union[Data, Sequence] = (),
            log_errors: bool = True) -> Any:
        ...

    def fetchall(self, *args, **kwargs) -> List[Tuple]:
        ...

    def fetchone(self, *args, **kwargs) -> Optional[Tuple]:
        ...

    def preformat(
            self,
            sql: str,
            params: Union[Data, Sequence]) \
            -> Tuple[str, Union[Dict[str, Any], Sequence]]:
        ...

    def quote(
            self,
            operation: str,
            parameters: Data) -> str:
        ...


class DBWrapper:

    cnx: Connection

    def __init__(self, cnx: Connection) -> None:
        ...

    def __getattr__(self, key: str) -> Any:
        ...

    def close(self) -> None:
        ...

    def cursor(self, *args, **kw) -> CursorWrapper:
        ...


class DeleteProcessor:

    clauses: List[str]
    table: str
    values: Data

    def __init__(
            self,
            table: str,
            clauses: Optional[Sequence[str]] = None,
            values: Optional[Data] = None) -> None:
        ...

    def execute(self) -> int:
        ...

    def get_values(self) -> Dict[str, Any]:
        ...


class InsertProcessor:

    data: Data
    rawdata: Data
    table: str

    def __init__(
            self,
            table: str,
            data: Optional[Data] = None,
            rawdata: Optional[Data] = None):
        ...

    def dup_check(self) -> Optional[bool]:
        ...

    def execute(self) -> int:
        ...

    def make_create(
            self,
            event_id: Optional[EventID] = None,
            user_id: Optional[UserID] = None) -> None:
        ...

    def rawset(self, **kwargs) -> None:
        ...

    def set(self, **kwargs) -> None:
        ...


class QueryProcessor:

    aliases: List[str]
    clauses: List[str]
    colsByAlias: Dict[str, str]
    columns: List[str]
    cursors: int
    enable_group: bool
    iterchunksize: int
    joins: List[str]
    logger: Logger
    opts: QueryProcessorOptions
    order_map: Optional[Dict[str, str]]
    tables: List[str]
    transform: Callable
    values: Dict[str, Any]

    def __init__(
            self,
            columns: Optional[List[str]] = None,
            aliases: Optional[List[str]] = None,
            tables: Optional[List[str]] = None,
            joins: Optional[List[str]] = None,
            clauses: Optional[List[str]] = None,
            values: Optional[Data] = None,
            transform: Optional[Callable] = None,
            opts: Optional[QueryProcessorOptions] = None,
            enable_group: bool = False,
            order_map: Optional[Dict[str, str]] = None):
        ...

    def countOnly(self, count: bool) -> None:
        ...

    def execute(self) -> Optional[List]:
        ...

    def executeOne(self, strict: bool = False) -> Optional[List]:
        ...

    def iterate(self) -> Iterator[List]:
        ...

    def singleValue(self, strict: bool = True) -> Optional[List]:
        ...


class QueryView:

    clauses: Optional[List[str]]
    default_fields: Sequence[str]
    fieldmap: Dict[str, str]
    fields: Optional[List[str]]
    joins: List[str]
    joinmap: Dict[str, str]
    opts: Optional[QueryProcessorOptions]
    tables: List[str]

    def __init__(
            self,
            clauses: Optional[Sequence[str]] = None,
            fields: Optional[Sequence[str]] = None,
            opts: Optional[QueryProcessorOptions] = None) -> None:
        ...

    def check_opts(self) -> None:
        ...

    def execute(self) -> Optional[List]:
        ...

    def executeOne(
            self,
            strict: bool = False) -> Optional[List]:
        ...

    def get_clauses(self) -> List[str]:
        ...

    def get_fields(
            self,
            fields: Optional[List[str]]) -> Dict[str, str]:
        ...

    def get_joins(self) -> List[str]:
        ...

    def get_query(self) -> QueryProcessor:
        ...

    def iterate(self) -> Iterator[List]:
        ...

    def map_field(self, field: str) -> str:
        ...

    @property
    def query(self) -> QueryProcessor:
        ...

    def singleValue(
            self,
            strict: bool = True) -> Optional[List]:
        ...


class Savepoint:

    name: str

    def __init__(self, name: str) -> None:
        ...

    def rollback(self) -> None:
        ...


class UpdateProcessor:

    clauses: List[str]
    data: Data
    rawdata: Data
    table: str
    values: Data

    def __init__(
            self,
            table: str,
            data: Optional[Data] = None,
            rawdata: Optional[Data] = None,
            clauses: Optional[List[str]] = None,
            values: Optional[Data] = None) -> None:
        ...

    def execute(self) -> int:
        ...

    def get_values(self) -> Data:
        ...

    def make_revoke(
            self,
            event_id: Optional[EventID] = None,
            user_id: Optional[UserID] = None) -> None:
        ...

    def rawset(self, **kwargs) -> None:
        ...

    def set(self, **kwargs) -> None:
        ...


class UpsertProcessor(InsertProcessor):

    keys: Optional[List[str]]
    skip_dup: bool

    def __init__(
            self,
            table: str,
            data: Optional[Data] = None,
            rawdata: Optional[Data] = None,
            keys: Optional[List[str]] = None,
            skip_dup: bool = False) -> None:
        ...


# The end.
