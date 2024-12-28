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
Koji - typing stubs

Typing annotations stub for koji.util

:author: Christopher O'Brien <obriencj@gmail.com>
:license: GPL v3
"""


from . import ClientSession

from base64 import b64decode
from configparser import ConfigParser
from datetime import datetime
from hashlib import md5
from koji_types import (
    BuildNVR, BuildInfo, ChangelogEntry, EventID, EventInfo,
    RepoInfo, RepoRequestID, TagID, TagInfo, TaskID, )
from koji_types.rpm import RPMHeader
from logging import Logger
from optparse import Values
from re import Pattern
from types import TracebackType
from typing import (
    Any, Callable, Dict, Generic, Iterable, Iterator, List, Literal,
    Optional, Set, Tuple, Type, TypeVar, Union, overload, )
from typing_extensions import Protocol, Self, TypeAlias
from xmlrpc.client import DateTime


base64decode = b64decode
md5_constructor = md5


DATE_RE: Pattern
TIME_RE: Pattern


class _WalkFn(Protocol):
    def __call__(self, _val: Any, /, **kwargs) -> Any:
        ...


class DataWalker:

    def __init__(self,
                 data: Any,
                 callback: _WalkFn,
                 kwargs: Optional[List] = None):
        ...

    def walk(self) -> Any:
        ...


class HiddenValue:

    def __init__(self, value):
        ...


_LKT = TypeVar("_LKT")
_LVT = TypeVar("_LVT")


class LazyDict(Generic[_LKT, _LVT]):

    def __contains__(self, key: _LKT) -> bool:
        ...

    def __getitem__(self, key: _LKT) -> _LVT:
        ...

    def __setitem__(self, key: _LKT, value: _LVT) -> None:
        ...

    def copy(self) -> LazyDict[_LKT, _LVT]:
        ...

    def get(self, *args, **kwargs) -> _LVT:
        ...

    def items(self) -> List[Tuple[_LKT, _LVT]]:
        ...

    def iteritems(self) -> Iterator[Tuple[_LKT, _LVT]]:
        ...

    def itervalues(self) -> Iterator[_LVT]:
        ...

    def lazyset(self,
                key: _LKT,
                func: Callable[..., _LVT],
                args: List,
                kwargs: Optional[Dict[str, Any]] = None,
                cache: bool = False) -> None:
        ...

    def pop(self, key: _LKT, *args, **kwargs) -> _LVT:
        ...

    def popitem(self) -> Tuple[_LKT, _LVT]:
        ...

    def values(self) -> List[_LVT]:
        ...


class LazyRecord:

    def __init__(self, base: Optional[Any] = None):
        ...

    def __getattribute__(self, name: str) -> Any:
        ...


class LazyValue(Generic[_LVT]):

    def __init__(
            self,
            func: Callable[..., _LVT],
            args: List[Any],
            kwargs: Optional[Dict[str, Any]] = None,
            cache: bool = False):
        ...

    def get(self) -> _LVT:
        ...


class LazyString(LazyValue):

    def __str__(self) -> str:  # noqa: Y029
        ...


class MavenConfigOptAdapter:

    MULTILINE: List[str]
    MULTIVALUE: List[str]

    def __init__(self, conf: ConfigParser, section: str):
        ...

    def __getattr__(self, name: str) -> Any:
        ...


class RepoWatcher:

    PAUSE: int
    TIMEOUT: int

    def __init__(
            self,
            session: ClientSession,
            tag: Union[str, TagID],
            nvrs: Optional[List[str]] = None,
            min_event: Optional[EventID] = None,
            at_event: Optional[EventID] = None,
            opts: Optional[Dict[str, Any]] = None,
            logger: Optional[Logger] = None):
        ...

    def check_timeout(self) -> bool:
        ...

    def check_repo(self, repoinfo: RepoInfo) -> bool:
        ...

    def get_start(self) -> datetime:
        ...

    def getRepo(self) -> Optional[RepoInfo]:
        ...

    def pause(self) -> None:
        ...

    def request(self, min_event: Optional[EventID] = None) -> TaskID:
        ...

    def task_args(self) -> Tuple[TagInfo, None, List[str], EventID]:
        ...

    def wait_builds(self, builds: List[str]) -> None:
        ...

    def wait_request(self, req: RepoRequestID) -> RepoInfo:
        # TODO: check this against checkRequest
        ...

    def waitrepo(self, anon: bool = False) -> RepoRequestID:
        ...


class SimpleProxyLogger:

    DEBUG: int
    INFO: int
    WARNING: int
    ERROR: int

    def __init__(self, filename: str):
        ...

    def __enter__(self) -> Self:
        ...

    def __exit__(
            self,
            _type: Optional[Type[BaseException]],
            value: Optional[BaseException],
            traceback: Optional[TracebackType]) -> bool:
        ...

    def debug(self, msg: str, *args, **kwargs) -> None:
        ...

    def error(self, msg: str, *args, **kwargs) -> None:
        ...

    def info(self, msg: str, *args, **kwargs) -> None:
        ...

    def log(self,
            level,
            msg: str,
            *args: str,
            **kwargs) -> None:
        ...

    @staticmethod
    def send(filename: str, logger: Logger) -> None:
        ...

    def warning(self, msg: str, *args, **kwargs) -> None:
        ...


class adler32_constructor:

    block_size: int
    digest_size: int

    def __init__(self, arg: Union[bytes, str] = ''):
        ...

    def copy(self) -> adler32_constructor:
        ...

    def digest(self) -> int:
        ...

    def hexdigest(self) -> str:
        ...

    def update(self, arg: Union[bytes, str]) -> None:
        ...


def apply_argspec(
        argspec: Tuple[List[str], Optional[str], Optional[str], List[Any]],
        args: List[Any],
        kwargs: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    ...


@overload
def base64encode(
        s: Union[str, bytes]) -> str:
    ...


@overload
def base64encode(
        s: Union[str, bytes],
        as_bytes: Literal[False]) -> str:
    ...


@overload
def base64encode(
        s: Union[str, bytes],
        as_bytes: Literal[True]) -> bytes:
    ...


@overload
def base64encode(
        s: Union[str, bytes],
        as_bytes: bool = False) -> Union[str, bytes]:
    ...


_CallReturn = TypeVar("_CallReturn")


def call_with_argcheck(
        func: Callable[..., _CallReturn],
        args: List,
        kwargs: Optional[Dict[str, Any]] = None) -> _CallReturn:
    ...


def check_sigmd5(
        filename: str) -> bool:
    ...


def checkForBuilds(
        session: ClientSession,
        tag: Union[str, int],
        builds: List[BuildNVR],
        event: int,
        latest: bool = False) -> bool:
    ...


def decode_bytes(
        data: bytes,
        fallback: str = 'iso8859-15') -> str:
    ...


def deprecated(
        message: str) -> None:
    ...


_KeyTypes = TypeVar("_KeyTypes")


def dslice(
        dict_: Dict,
        keys: List[_KeyTypes],
        strict: bool = True) -> Dict[_KeyTypes, Any]:
    ...


def dslice_ex(
        dict_: Dict,
        keys: List,
        strict: bool = True) -> Dict:
    ...


def duration(
        start: float) -> str:
    ...


def encode_datetime(
        value: Union[str, datetime, DateTime]) -> str:
    ...


def encode_datetime_recurse(
        value: Any) -> Any:
    ...


def extract_build_task(
        binfo: BuildInfo) -> int:
    ...


def eventFromOpts(
        session: ClientSession,
        opts: Dict[str, Any]) -> Optional[EventInfo]:
    ...


def filedigestAlgo(hdr: RPMHeader) -> str:
    ...


def format_shell_cmd(
        cmd: str,
        text_width: int = 80) -> str:
    ...


def formatChangelog(
        entries: List[ChangelogEntry]) -> str:
    ...


def isSuccess(
        rv: Tuple[int, int]) -> bool:
    ...


def joinpath(
        path: str,
        *paths: str) -> str:
    ...


def lazy_eval(
        value: Any) -> Any:
    ...


def lazysetattr(
        object: Any,
        name: str,
        func: Callable,
        args: List,
        kwargs: Optional[Dict[str, Any]] = None,
        cache: bool = False) -> None:
    ...


def maven_opts(
        values: Values,
        chain: bool = False,
        scratch: bool = False) -> Dict[str, Any]:
    ...


def maven_params(
        config: ConfigParser,
        package: str,
        chain: bool = False,
        scratch: bool = False) -> Dict[str, Any]:
    ...


def move_and_symlink(
        src: str,
        dst: str,
        relative: bool = True,
        create_dir: bool = False) -> None:
    ...


def multi_fnmatch(
        s: str,
        patterns: List[str]) -> bool:
    ...


def parse_maven_chain(
        confs: List[str],
        scratch: bool = False) -> Dict[str, Dict[str, Any]]:
    ...


def parse_maven_param(
        confs: Union[str, List[str]],
        chain: bool = False,
        scratch: bool = False,
        section: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
    ...


def parse_maven_params(
        confs: List[str],
        chain: bool = False,
        scratch: bool = False) -> Dict[str, Dict[str, Any]]:
    ...


def parseTime(val: str) -> Optional[int]:
    ...


def parseStatus(
        rv: Tuple[int, int],
        prefix: Union[str, List[str], Tuple[str, ...]]) -> str:
    ...


def printList(lst: List[str]) -> str:
    ...


_Nullary: TypeAlias = TypeAlias[Callable[[], None]]


@overload
def rmtree(
        path: str,
        logger: Optional[Logger] = None) -> None:
    ...


@overload
def rmtree(
        path: str,
        logger: Optional[Logger] = None,
        *,
        background: Literal[False]) -> None:
    ...


@overload
def rmtree(
        path: str,
        logger: Optional[Logger] = None,
        *,
        background: Literal[True]) -> Tuple[int, _Nullary]:
    ...


@overload
def rmtree(
        path: str,
        logger: Optional[Logger] = None,
        background: bool = False) -> Union[None, Tuple[int, _Nullary]]:
    ...


def safer_move(src: str, dst: str) -> None:
    ...


def setup_rlimits(
        opts: Dict[str, str],
        logger: Optional[Logger] = None) -> None:
    ...


_ListVals = TypeVar("_ListVals")


def to_list(lst: Iterable[_ListVals]) -> List[_ListVals]:
    ...


def tsort(parts: Dict[str, Set[str]]) -> List[Set[str]]:
    ...


def wrapper_params(
        config: ConfigParser,
        package: str,
        chain: bool = False,
        scratch: bool = False) -> Dict[str, Any]:
    ...


# The end.
