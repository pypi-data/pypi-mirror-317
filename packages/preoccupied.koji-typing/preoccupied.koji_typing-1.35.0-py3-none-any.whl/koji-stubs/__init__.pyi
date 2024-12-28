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

Typing annotations stub for koji

:author: Christopher O'Brien <obriencj@gmail.com>
:license: GPL v3
"""


from configparser import ConfigParser, RawConfigParser
from datetime import datetime
from io import BufferedReader, BufferedRWPair, RawIOBase
from logging import Handler, Logger
from re import Pattern
from requests import Session
from types import ModuleType
from typing import (
    Any, Callable, Dict, Generic, Iterable, List, Literal,
    NoReturn, Optional, Tuple, Type, TypeVar, Union, Set, overload, )
from typing_extensions import Buffer, Protocol, Self, TypeAlias
from weakref import ReferenceType
from xmlrpc.client import DateTime

from koji_types import (
    ArchiveInfo, BuildInfo, BuildNVR, FaultInfo, MavenInfo, POMInfo,
    RepoInfo, RPMInfo, RPMSignature, RPMSigTag, TagInfo, TagGroupInfo,
    TaskInfo,)
from koji_types.protocols import (
    ClientSession as ClientSessionProtocol,
    MultiCallSession as MultiCallSessionProtocol, )
from koji_types.rpm import RPMHeader


__version_info__: Tuple[int, ...]

pathinfo: PathInfo

# Koji 1.34.0 intentionally broke API compatibility and removed these.
# https://pagure.io/koji/pull-request/3818

# AUTHTYPE_NORMAL: int
# AUTHTYPE_KERB: int
# AUTHTYPE_SSL: int
# AUTHTYPE_GSSAPI: int

API_VERSION: int
BASEDIR: str
CONTROL_CHARS: List[str]
DEFAULT_AUTH_TIMEOUT: int
DEFAULT_REQUEST_TIMEOUT: int

DEP_CONFLICT: int
DEP_ENHANCE: int
DEP_OBSOLETE: int
DEP_PROVIDE: int
DEP_RECOMMEND: int
DEP_REQUIRE: int
DEP_SUGGEST: int
DEP_SUPPLEMENT: int

DRAFT_RELEASE_DELIMITER: str
DRAFT_RELEASE_FORMAT: str
ENTITY_RE: Pattern
NONPRINTABLE_CHARS: str
NONPRINTABLE_CHARS_TABLE: Dict[int, str]
PRIO_DEFAULT: int
PROFILE_MODULES: Dict[str, Any]

REPO_DELETED: int
REPO_EXPIRED: int
REPO_INIT: int
REPO_PROBLEM: int
REPO_READY: int

REPO_MERGE_MODES: Set[str]

RPM_FILEDIGESTALGO_IDS: Dict[Optional[int], str]
RPM_HEADER_MAGIC: bytes

RPM_SIGTAG_DSA: int
RPM_SIGTAG_GPG: int
RPM_SIGTAG_MD5: int
RPM_SIGTAG_PGP: int
RPM_SIGTAG_RSA: int

RPM_TAG_FILEDIGESTALGO: int
RPM_TAG_HEADERSIGNATURES: int

RPMSENSE_EQUAL: int
RPMSENSE_GREATER: int
RPMSENSE_LESS: int

SUPPORTED_OPT_DEP_HDRS: Dict[str, bool]


# === Enums ===

AUTHTYPES: Enum
BR_STATES: Enum
BR_TYPES: Enum
BUILD_STATES: Enum
CHECKSUM_TYPES: Enum
REPO_STATES: Enum
TAG_UPDATE_TYPES: Enum
TASK_STATES: Enum
USERTYPES: Enum
USER_STATUS: Enum


# === Exceptions ===

PythonImportError: TypeAlias = TypeAlias[ImportError]


class GenericError(Exception):
    faultCode: int
    fromFault: bool


class ActionNotAllowed(GenericError):
    ...


class ApplianceError(GenericError):
    ...


class AuthError(GenericError):
    ...


class AuthExpired(AuthError):
    ...


class AuthLockError(AuthError):
    ...


class BuildError(GenericError):
    ...


class BuildrootError(BuildError):
    ...


class CallbackError(GenericError):
    ...


class ConfigurationError(GenericError):
    ...


class FunctionDeprecated(GenericError):
    ...


class GSSAPIAuthError(AuthError):
    ...


class ImportError(GenericError):
    ...


class LiveCDError(GenericError):
    ...


class LiveMediaError(GenericError):
    ...


class LockError(GenericError):
    ...


class MultiCallNotReady(Exception):
    ...


class NameValidationError(GenericError):
    ...


class ParameterError(GenericError):
    ...


class PluginError(GenericError):
    ...


class PostBuildError(BuildError):
    ...


class PreBuildError(BuildError):
    ...


class RetryError(AuthError):
    ...


class ServerOffline(GenericError):
    ...


class SequenceError(AuthError):
    ...


class TagError(GenericError):
    ...


# === Classes ===

class ClientSession(ClientSessionProtocol):

    auth_method: Optional[str]
    authtype: Optional[str]
    baseurl: str
    exclusive: bool
    logger: Logger
    multicall: MultiCallHack
    opts: Dict[str, Any]
    rsession: Optional[Session]

    def __init__(
            self,
            baseurl: str,
            opts: Optional[Dict[str, Any]] = None,
            sinfo: Optional[Dict[str, Any]] = None,
            auth_method: Optional[str] = None):
        ...

    def __del__(self):
        ...

    def __getattr__(self, name: str) -> VirtualMethod:
        ...

    def callMethod(
            self,
            name: str,
            *args,
            **kwds) -> Any:
        ...

    def exclusiveSession(
            self,
            force: bool = False) -> None:
        ...

    def fastUpload(
            self,
            localfile: str,
            path: str,
            name: Optional[str] = None,
            callback: Optional[Callable[[int, int, int, int, int],
                                        None]] = None,
            blocksize: Optional[int] = None,
            overwrite: bool = False,
            volume: Optional[str] = None) -> None:
        ...

    def gssapi_login(
            self,
            principal: Optional[str] = None,
            keytab: Optional[str] = None,
            ccache: Optional[str] = None,
            proxyuser: Optional[str] = None,
            proxyauthtype: Optional[str] = None,
            renew: bool = False) -> bool:
        ...

    @property
    def hub_version(self) -> Tuple[int, ...]:
        # :since: koji 1.35
        ...

    @property
    def hub_version_str(self) -> str:
        # :since: koji 1.35
        ...

    def login(
            self,
            opts: Optional[Dict[str, Any]] = None,
            renew: bool = False) -> bool:
        ...

    def logout(
            self,
            session_id: Optional[int] = None) -> None:
        ...

    def multiCall(
            self,
            strict: bool = False,
            batch: Optional[int] = None) -> List[Union[FaultInfo,
                                                       List[Any]]]:
        ...

    def new_session(self) -> None:
        ...

    def renew_expired_session(
            func) -> Callable:
        ...

    def setSession(
            self,
            sinfo: Session) -> None:
        ...

    def ssl_login(
            self,
            cert: Optional[str] = None,
            ca: Optional[str] = None,
            serverca: Optional[str] = None,
            proxyuser: Optional[str] = None,
            proxyauthtype: Optional[int] = None,
            renew: bool = False) -> bool:
        ...

    def subsession(self) -> ClientSession:
        ...

    def uploadWrapper(
            self,
            localfile: str,
            path: str,
            name: Optional[str] = None,
            callback: Optional[Callable[[int, int, int, int, int],
                                        None]] = None,
            blocksize: Optional[int] = None,
            overwrite: bool = True,
            volume: Optional[str] = None) -> None:
        ...


class Enum(dict):

    def __init__(
            self,
            args: Iterable[str]):
        ...

    @overload
    def get(self,
            key: int,
            default: Any = None) -> Optional[str]:
        ...

    @overload
    def get(self,
            key: str,
            default: Any = None) -> Optional[int]:
        ...

    def getnum(
            self,
            key: Union[str, int],
            default: Optional[int] = None) -> int:
        ...

    def clear(self, *args, **opts) -> NoReturn:
        ...

    def getvalue(self, *args, **opts) -> NoReturn:
        ...

    def pop(self, *args, **opts) -> NoReturn:
        ...

    def popitem(self, *args, **opts) -> NoReturn:
        ...

    def setdefault(self, *args, **opts) -> NoReturn:
        ...

    def update(self, *args, **opts) -> NoReturn:
        ...


class Fault:

    def __init__(
            self,
            faultCode: int,
            faultString: str,
            **extra: Dict[str, Any]):
        ...


class MultiCallSession(MultiCallSessionProtocol):

    def __init__(
            self,
            session: ClientSession,
            strict: bool = False,
            batch: Optional[int] = None):
        ...

    def __enter__(self) -> Self:
        ...

    def __exit__(self, _tp, _tv, _tb) -> bool:
        ...

    def __getattr__(self, name: str) -> VirtualMethod[VirtualCall]:
        ...

    def call_all(
            self,
            strict: Optional[bool] = None,
            batch: Optional[int] = None) -> List[Union[FaultInfo,
                                                       List[Any]]]:
        ...

    def callMethod(
            self,
            name: str,
            *args,
            **kwds) -> VirtualCall:
        ...

    multiCall = call_all

    @property
    def multicall(self) -> bool:
        ...


class MultiCallHack:

    def __init__(self, session: ReferenceType[ClientSession]):
        ...

    def __set__(self, obj: ClientSession, value: bool) -> None:
        # not present at runtime, but used to fix assignments
        ...

    def __bool__(self) -> bool:
        ...

    def __nonzero__(self) -> bool:
        ...

    @overload
    def __call__(
            self,
            *,
            strict: Optional[bool] = False,
            batch: Optional[int] = None) -> MultiCallSession:
        ...

    @overload
    def __call__(
            self,
            **kw) -> MultiCallSession:
        ...


class MultiCallInProgress:
    ...


class PathInfo:

    topdir: str
    ASCII_CHARS: List[str]

    def __init__(
            self,
            topdir: Optional[str] = None):
        ...

    def build(
            self,
            build: BuildInfo) -> str:
        ...

    def build_logs(
            self,
            build: BuildInfo) -> str:
        ...

    def distrepo(
            self,
            repo_id: int,
            tag: TagInfo,
            volume: Optional[str] = None) -> str:
        ...

    def imagebuild(
            self,
            build: BuildInfo) -> str:
        ...

    def mavenbuild(
            self,
            build: BuildInfo) -> str:
        ...

    def mavenfile(
            self,
            maveninfo: ArchiveInfo) -> str:
        ...

    def mavenrepo(
            self,
            maveninfo: ArchiveInfo) -> str:
        ...

    def repo(
            self,
            repo_id: int,
            tag_str: str) -> str:
        ...

    def repocache(
            self,
            tag_str: str) -> str:
        ...

    def rpm(
            self,
            rpminfo: RPMInfo) -> str:
        ...

    def scratch(
            self) -> str:
        ...


    def sighdr(
            self,
            rpminfo: RPMInfo,
            sigkey: str) -> str:
        ...

    def signed(
            self,
            rpminfo: RPMInfo,
            sigkey: str) -> str:
        ...

    def task(
            self,
            task_id: int,
            volume: Optional[str] = None) -> str:
        ...

    def taskrelpath(
            self,
            task_id: int) -> str:
        ...

    def tmpdir(
            self,
            volume: Optional[str] = None) -> str:
        ...

    def typedir(
            self,
            build: BuildInfo,
            btype: str) -> str:
        ...

    def volumedir(
            self,
            volume: str) -> str:
        ...

    def winbuild(
            self,
            build: BuildInfo) -> str:
        ...

    def winfile(
            self,
            wininfo: ArchiveInfo) -> str:
        ...

    def work(
            self,
            volume: Optional[str] = None) -> str:
        ...


class RawHeader:

    def __init__(
            self,
            data: bytes,
            decode: bool = False):
        ...

    def __getitem__(
            self,
            key: int) -> Any:
        ...

    def decode_bytes(
            self,
            value: str) -> bytes:
        ...

    def dump(
            self,
            sig: Optional[bool] = None) -> None:
        ...

    def get(self,
            key: int,
            default: Any = None,
            decode: Optional[bool] = None,
            single: bool = False) -> Any:
        ...

    def version(self) -> int:
        ...


class SplicedSigStreamReader(RawIOBase):

    def __init__(
            self,
            path: str,
            sighdr: bytes,
            bufsize: int):
        ...

    def generator(self) -> Iterable[bytes]:
        ...

    def readable(self) -> bool:
        ...

    def readinto(
            self,
            b: Buffer) -> int:
        ...


_VirtualCallResult = TypeVar("_VirtualCallResult")


class VirtualCall(Generic[_VirtualCallResult]):

    def __init__(self, method: str, args, kwargs):
        ...

    def format(self) -> str:
        ...

    @property
    def result(self) -> _VirtualCallResult:
        ...


_VirtualMethodReturn = TypeVar("_VirtualMethodReturn")


class VirtualMethod(Generic[_VirtualMethodReturn]):

    def __init__(
            self,
            func: Callable[[str, List, Dict], Any],
            name: str,
            session: Optional[ClientSession] = None):
        ...

    def __call__(self, *args, **kwds) -> _VirtualMethodReturn:
        ...

    @property
    def __doc__(self) -> Optional[str]:  # type: ignore
        ...

    def __getattr__(self, name: str) -> VirtualMethod[_VirtualMethodReturn]:
        ...


# === Functions ===

def _fix_print(
        value: Union[str, bytes]) -> str:
    ...


def _open_text_file(
        path: str,
        mode: str = 'rt'):
    ...


def add_file_logger(
        logger: str,
        fn: str) -> None:
    ...


def add_mail_logger(
        logger: str,
        addr: str) -> None:
    ...


def add_stderr_logger(
        logger: str) -> None:
    ...


def add_sys_logger(
        logger: str) -> None:
    ...


def buildLabel(
        buildInfo: BuildNVR,
        showEpoch: bool = False) -> str:
    ...


def canonArch(
        arch: str) -> str:
    ...


def check_NVR(
        nvr: Union[str, Dict[str, Union[str, int]]],
        strict: bool = False) -> bool:
    ...


def check_NVRA(
        nvra: Union[str, Dict[str, Union[str, int]]],
        strict: bool = False) -> bool:
    ...


def check_rpm_file(
        rpmfile: Union[str, BufferedReader]) -> None:
    ...


def config_directory_contents(
        dir_name: str,
        strict: bool = False) -> List[str]:
    ...


def convertFault(fault: Fault) -> GenericError:
    ...


def daemonize() -> None:
    ...


def decode_args(*args) -> Tuple[Tuple[Any, ...], Dict[str, Any]]:
    ...


def decode_args2(
        args: List[Any],
        names: List[str],
        strict: bool = True) -> Dict[str, Any]:
    ...


def decode_int(n: Any) -> int:
    ...


def downloadFile(
        url: str,
        path: Optional[str] = None,
        fo: Optional[BufferedRWPair] = None) -> None:
    ...


def dump_json(
        filepath: str,
        data: Any,
        indent: int = 4,
        sort_keys: bool = False) -> None:
    ...


def encode_args(*args, **opts) -> Tuple[Any, ...]:
    ...


def ensuredir(
        directory: str) -> None:
    ...


def find_rpm_sighdr(path: str) -> Tuple[int, int]:
    ...


def fix_encoding(
        value: str,
        fallback: str = 'iso8859-15',
        remove_nonprintable: bool = False) -> str:
    ...


def fixEncoding(
        value: Optional[str],
        fallback: str = 'iso8859-15',
        remove_nonprintable: bool = False) -> str:
    ...


def fixEncodingRecurse(
        value: Any,
        fallback: str = 'iso8859-15',
        remove_nonprintable: bool = False) -> str:
    ...


def format_exc_plus() -> str:
    ...


def formatTime(
        value: Union[int, float, datetime, DateTime]) -> str:
    ...


def formatTimeLong(
        value: Union[int, float, datetime, DateTime]) -> str:
    ...


def genMockConfig(
        name: str,
        arch: str,
        managed: bool = False,
        repoid: Optional[int] = None,
        tag_name: Optional[str] = None,
        **opts) -> str:
    ...


def gen_draft_release(
        target_release: str,
        build_id: int) -> str:
    ...


def generate_comps(
        groups: List[TagGroupInfo],
        expand_groups: bool = False) -> str:
    ...


def get_header_field(
        hdr: RPMHeader,
        name: str,
        src_arch: bool = False) -> Union[str, List[str]]:
    ...


def get_header_fields(
        X: Union[bytes, str],
        fields: Optional[List[str]] = None,
        src_arch: bool = False) -> Dict[str, Union[str, List[str]]]:
    ...


def get_profile_module(
        profile_name: str,
        config: Optional[ConfigParser] = None) -> ModuleType:
    ...


def get_rpm_header(
        f: Union[bytes, str],
        ts: Optional[int] = None) -> RPMHeader:
    ...


def get_sighdr_key(sighdr: bytes) -> RPMSigTag:
    ...


def get_sigpacket_key_id(
        sigpacket: str) -> str:
    ...


def grab_session_options(
        options: Union[Dict[str, Any], Any]) -> Dict[str, Any]:
    ...


def hex_string(s: str) -> str:
    ...


def is_conn_error(e: Exception) -> bool:
    ...


def is_debuginfo(
        name: str) -> bool:
    ...


def is_requests_cert_error(
        e: Exception) -> bool:
    ...


def load_json(filepath: str) -> Any:
    ...


def make_groups_spec(
        grplist: List[TagGroupInfo],
        name: str = 'buildsys-build',
        buildgroup: Optional[str] = None) -> str:
    ...


def maven_info_to_nvr(
        maveninfo: Dict[str, Any]) -> Dict[str, Any]:
    ...


def mavenLabel(maveninfo: MavenInfo) -> str:
    ...


def multibyte(data: bytes) -> int:
    ...


def openRemoteFile(
        relpath: str,
        topurl: Optional[str] = None,
        topdir: Optional[str] = None,
        tempdir: Optional[str] = None):
    ...


def parse_NVR(nvr: str) -> Dict[str, Union[str, int]]:
    ...


def parse_NVRA(nvra: str) -> Dict[str, Union[str, int]]:
    ...


@overload
def parse_arches(
        arches: Union[str, List[str]],
        strict: bool = False,
        allow_none: bool = False) -> str:
    ...


@overload
def parse_arches(
        arches: Union[str, List[str]],
        to_list: Literal[False],
        strict: bool = False,
        allow_none: bool = False) -> str:
    ...


@overload
def parse_arches(
        arches: Union[str, List[str]],
        to_list: Literal[True],
        strict: bool = False,
        allow_none: bool = False) -> List[str]:
    ...


@overload
def parse_arches(
        arches: Union[str, List[str]],
        to_list: bool = False,
        strict: bool = False,
        allow_none: bool = False) -> Union[str, List[str]]:
    ...


def parse_pom(
        path: Optional[str] = None,
        contents: Optional[str] = None) -> POMInfo:
    ...


def parse_target_release(
        draft_release: str) -> str:
    ...


def pom_to_maven_info(
        pominfo: POMInfo) -> MavenInfo:
    ...


def read_config(
        profile_name: str,
        user_config: Optional[str] = None) -> Dict[str, Any]:
    ...


@overload
def read_config_files(
        config_files: List[Union[str, Tuple[str, bool]]]) -> ConfigParser:
    ...


@overload
def read_config_files(
        config_files: List[Union[str, Tuple[str, bool]]],
        raw: Literal[False]) -> ConfigParser:
    ...


@overload
def read_config_files(
        config_files: List[Union[str, Tuple[str, bool]]],
        raw: Literal[True]) -> RawConfigParser:
    ...


@overload
def read_config_files(
        config_files: List[Union[str, Tuple[str, bool]]],
        raw: bool = False) -> Union[RawConfigParser, ConfigParser]:
    ...


def remove_log_handler(
        logger: str,
        handler: Handler) -> None:
    ...


def removeNonprintable(value: str) -> str:
    ...


def request_with_retry(
        retries: int = 3,
        backoff_factor: float = 0.3,
        status_forcelist: Tuple[int, ...] = (500, 502, 504, 408, 429),
        session: Optional[Session] = None) -> Session:
    ...


def rip_rpm_hdr(src: str) -> bytes:
    ...


def rip_rpm_sighdr(src: str) -> bytes:
    ...


def rpm_hdr_size(
        f: Union[str, BufferedReader],
        ofs: Optional[int] = None,
        pad: bool = False) -> int:
    ...


def safe_xmlrpc_loads(s: str) -> Union[Fault, Any]:
    ...


def splice_rpm_sighdr(
        sighdr: bytes,
        src: str,
        dst: Optional[str] = None,
        bufsize: int = 8192,
        callback: Optional[Callable[[bytes], None]] = None) -> str:
    ...


def spliced_sig_reader(
        path: str,
        sighdr: bytes,
        bufsize: int = 8192) -> BufferedReader:
    ...


def taskLabel(taskInfo: TaskInfo) -> str:
    ...


# The end.
