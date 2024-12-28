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
Koji CLI - commands typing stubs

Typing annotations stub for koji_cli.commands

:author: Christopher O'Brien <obriencj@gmail.com>
:license: GPL v3
"""  # noqa: Y021


from json import JSONEncoder
from koji import ClientSession
from koji_types import (
    ArchiveInfo, BuildInfo, BuildNVR, GOptions, TagInheritanceEntry,
    RPMInfo, TaskInfo, )
from optparse import Option, OptionParser, Values
from typing import (
    Any, Callable, Dict, List, NoReturn, Optional, Tuple, Type, )


categories: Dict[str, str]
greetings: Tuple[str, ...]

ARGMAP: Dict[str, Optional[bool]]


class DatetimeJSONEncoder(JSONEncoder):
    def default(self, o: Any) -> Any:
        ...


class TaskWatcher:

    def __init__(
            self,
            task_id: int,
            session: ClientSession,
            level: int = 0,
            quiet: bool = False,
            topurl: Optional[str] = None):
        ...

    def display_state(self, info: TaskInfo, level: int = 0) -> str:
        ...

    def get_failure(self) -> str:
        ...

    def is_done(self) -> bool:
        ...

    def is_success(self) -> bool:
        ...

    def str(self) -> str:
        ...

    def update(self) -> bool:
        ...


class TimeOption(Option):
    TYPES: Tuple[str, ...]
    TYPE_CHECKER: Dict[str, Any]

    @classmethod
    def get_help(cls: Type) -> str:
        ...


def activate_session(
        session: ClientSession,
        options: GOptions) -> None:
    ...


def arg_filter(arg: str, parse_json: bool = False) -> Any:
    ...


def bytes_to_stdout(contents: bytes) -> None:
    ...


def display_task_results(tasks: Dict[int, TaskInfo]) -> None:
    ...


def display_tasklist_status(tasks: Dict[int, TaskInfo]) -> None:
    ...


def download_archive(
        build: BuildInfo,
        archive: ArchiveInfo,
        topurl: str,
        quiet: bool = False,
        noprogress: bool = False,
        num: Optional[int] = None,
        size: Optional[int] = None) -> None:
    ...


def download_file(
        url: str,
        relpath: str,
        quiet: bool = False,
        noprogress: bool = False,
        size: Optional[int] = None,
        num: Optional[int] = None,
        filesize: Optional[int] = None) -> None:
    ...


def download_rpm(
        build: BuildInfo,
        rpm: RPMInfo,
        topurl: str,
        sigkey: Optional[str] = None,
        quiet: bool = False,
        noprogress: bool = False,
        num: Optional[int] = None,
        size: Optional[int] = None) -> None:
    ...


def get_epilog_str(progname: Optional[str] = None) -> str:
    ...


def get_usage_str(usage: str) -> str:
    ...


def ensure_connection(
        session: ClientSession,
        options: Optional[GOptions] = None) -> None:
    ...


def error(
        msg: Optional[str] = None,
        code: int = 1) -> NoReturn:
    ...


def format_inheritance_flags(parent: TagInheritanceEntry) -> str:
    ...


def linked_upload(
        localfile: str,
        path: str,
        name: Optional[str] = None) -> None:
    ...


def list_task_output_all_volumes(
        session: ClientSession,
        task_id: int) -> Dict[str, List[str]]:
    ...


def print_task(
        task: TaskInfo,
        depth: int = 0) -> None:
    ...


def print_task_headers() -> None:
    ...


def print_task_recurse(
        task: TaskInfo,
        depth: int = 0) -> None:
    ...


def truncate_string(
        s: str,
        length: int = 47) -> str:
    ...


def unique_path(prefix: str) -> str:
    ...


def wait_repo(
        session: ClientSession,
        tag_id: int,
        builds: List[BuildNVR],
        poll_interval: int = 5,
        timeout: int = 120):
    ...


def warn(msg: str) -> None:
    ...


def watch_logs(
        session: ClientSession,
        tasklist: List[int],
        opts: Values,
        poll_interval: int) -> None:
    ...


def watch_tasks(
        session: ClientSession,
        tasklist: List[int],
        quiet: bool = False,
        poll_interval: int = 60,
        ki_handler: Optional[Callable[[str, List[int], bool], None]] = None,
        topurl: Optional[str] = None) -> int:
    ...


# The end.
