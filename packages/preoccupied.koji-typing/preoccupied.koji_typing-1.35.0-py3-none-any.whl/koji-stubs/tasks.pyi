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

Typing annotations stub for koji.tasks

:author: Christopher O'Brien <obriencj@gmail.com>
:license: GPL v3
"""


from datetime import datetime
from koji import ClientSession
from koji.daemon import TaskManager
from koji_types import (
    BuildInfo, EventID, HostInfo, GOptions, RepoInfo, TagInfo, TaskInfo, )
from koji_types.arch import Arch
from koji_types.plugin import CallbackType
from typing import Any, Dict, List, NoReturn, Optional, Union, overload


LEGACY_SIGNATURES: Dict[str, List]


# === Exceptions ===

class RefuseTask(Exception):
    ...


class ServerExit(Exception):
    ...


class ServerRestart(Exception):
    ...


# === Classes ===

class BaseTaskHandler:

    Foreground: bool
    Methods: List[str]

    def __init__(
            self,
            id: int,
            method: str,
            params: List,
            session: ClientSession,
            options: GOptions,
            workdir: Optional[str] = None):
        ...

    def chownTree(
            self,
            dirpath: str,
            uid: int,
            gid: int) -> None:
        ...

    def createWorkdir(self) -> None:
        ...

    def find_arch(
            self,
            arch: Arch,
            host: HostInfo,
            tag: TagInfo,
            preferred_arch: Optional[Arch] = None) -> Arch:
        ...

    def getRepo(
            self,
            tag: Union[int, str],
            builds: Optional[List[str]] = None,
            wait: bool = False) -> RepoInfo:
        ...

    def getUploadDir(self) -> str:
        ...

    def handler(self) -> NoReturn:
        ...

    def localPath(self, relpath: str) -> str:
        ...

    def removeWorkdir(self) -> None:
        ...

    def run(self) -> Any:
        ...

    def run_callbacks(
            self,
            plugin: CallbackType,
            *args,
            **kwargs) -> None:
        ...

    def setManager(
            self,
            manager: TaskManager) -> None:
        ...

    def subtask(
            self,
            method: str,
            arglist: List,
            **opts) -> Any:
        ...

    def subtask2(  # type: ignore
            self,
            __taskopts: List,
            __method: str,
            *args,
            **kwargs) -> Any:
        ...

    @property
    def taskinfo(self) -> TaskInfo:
        ...

    @taskinfo.setter
    def taskinfo(self, taskinfo: TaskInfo) -> None:
        ...

    def uploadFile(
            self,
            filename: str,
            relPath: Optional[str] = None,
            remoteName: Optional[str] = None,
            volume: Optional[str] = None) -> None:
        ...

    def uploadTree(
            self,
            dirpath: str,
            flatten: bool = False,
            volume: Optional[str] = None) -> None:
        ...

    def wait(
            self,
            subtasks: Union[int, List[int], None] = None,
            all: bool = False,
            failany: bool = False,
            canfail: Optional[List[int]] = None,
            timeout: Optional[int] = None) -> Dict:
        ...

    def weight(self) -> float:
        ...


class DefaultTask(BaseTaskHandler):

    def handler(  # type: ignore[override]
            self,
            *args,
            **opts) -> NoReturn:
        ...


class DependantTask(BaseTaskHandler):

    def handler(  # type: ignore[override]
            self,
            wait_list: List[int],
            task_list: List[List]) -> None:
        ...


class FakeTask(BaseTaskHandler):

    def handler(  # type: ignore[override]
            self,
            *args) -> int:
        ...


class ForkTask(BaseTaskHandler):

    def handler(  # type: ignore[override]
            self,
            n: int = 5,
            m: int = 37) -> None:
        ...


class MultiPlatformTask(BaseTaskHandler):

    def buildWrapperRPM(
            self,
            spec_url: str,
            build_task_id: int,
            build_target: str,
            build: BuildInfo,
            repo_id: int,
            **opts) -> TaskInfo:
        ...


class RestartHostsTask(BaseTaskHandler):

    def handler(  # type: ignore[override]
            self,
            options: Optional[Dict] = None) -> None:
        ...


class RestartTask(BaseTaskHandler):

    def handler(  # type: ignore[override]
            self,
            host: HostInfo) -> str:
        ...


class RestartVerifyTask(BaseTaskHandler):

    def handler(  # type: ignore[override]
            self,
            task_id: int,
            host: HostInfo) -> None:
        ...


class ShutdownTask(BaseTaskHandler):
    ...


class SleepTask(BaseTaskHandler):

    def handler(  # type: ignore[override]
            self,
            n: int) -> None:
        ...


class SubtaskTask(BaseTaskHandler):

    def handler(  # type: ignore[override]
            self,
            n: int = 4) -> None:
        ...


class WaitrepoTask(BaseTaskHandler):

    PAUSE: int
    TIMEOUT: int

    def handler(  # type: ignore[override]
            self,
            tag: Union[str, int],
            newer_than: Union[str, datetime, None] = None,
            nvrs: Optional[List[str]] = None,
            min_event: Optional[EventID] = None) -> RepoInfo:
        # :since: koji 1.35
        ...


class WaitTestTask(BaseTaskHandler):

    def handler(  # type: ignore[override]
            self,
            count: int,
            seconds: int = 10) -> None:
        ...


# === functions ===

def parse_task_params(
        method: str,
        params: List) -> List:
    ...


def safe_rmtree(
        path: str,
        unmount: bool = False,
        strict: bool = True) -> int:
    ...


def scan_mounts(
        topdir: str) -> List[str]:
    ...


def umount_all(
        topdir: str) -> None:
    ...


# The end.
