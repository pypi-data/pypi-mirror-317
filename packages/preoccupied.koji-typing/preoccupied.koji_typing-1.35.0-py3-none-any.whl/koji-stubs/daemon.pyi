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


from io import BufferedReader
from koji import ClientSession
from koji.tasks import BaseTaskHandler
from koji_types import GOptions, TaskInfo
from koji_types.plugins import CallbackHandler
from logging import Logger
from types import ModuleType
from typing import (
    Any, Callable, Dict, List, Optional, Tuple, )


class SCM:

    types: Dict[str, Tuple[str, ...]]

    def __init__(
            self,
            url: str,
            allow_password: bool = False):
        ...

    def assert_allowed(
            self,
            allowed: str = '',
            session: Optional[ClientSession] = None,
            by_config: bool = True,
            by_policy: bool = False,
            policy_data: Optional[Dict] = None) -> None:
        ...

    def assert_allowed_by_config(
            self,
            allowed: str) -> None:
        ...

    def assert_allowed_by_policy(
            self,
            session: ClientSession,
            **extra_data) -> None:
        ...

    def checkout(
            self,
            scmdir: str,
            session: Optional[ClientSession] = None,
            uploadpath: Optional[str] = None,
            logfile: Optional[str] = None) -> str:
        ...

    def get_info(
            self,
            keys: Optional[List[str]] = None) -> Dict[str, Any]:
        ...

    def get_source(self) -> Dict[str, str]:
        # TODO: Add an SCMSource TypedDict for this
        ...

    @classmethod
    def is_scm_url(
            cls,
            url: str,
            strict: bool = False) -> bool:
        ...


class TaskManager:

    def __init__(
            self,
            options: GOptions,
            session: ClientSession):
        ...

    # Removed koji 1.35
    # def checkAvailDelay(
    #         self,
    #         task: TaskInfo,
    #         bin_avail
    #         our_avail) -> bool:
    #     ...

    def checkSpace(
            self) -> bool:
        ...

    # Removed koji 1.35
    # def cleanDelayTimes(
    #         self) -> None:
    #     ...

    def cleanupTask(
            self,
            task_id: int,
            wait: bool = True) -> bool:
        ...

    def findHandlers(
            self,
            vars: Dict[str, Any]) -> None:
        ...

    def forkTask(
            self,
            handler: BaseTaskHandler) -> Tuple[int, int]:
        ...

    def getNextTask(
            self) -> bool:
        ...

    def readyForTask(
            self) -> bool:
        ...

    def registerCallback(
            self,
            entry: CallbackHandler) -> None:
        ...

    def registerHandler(
            self,
            entry: BaseTaskHandler) -> None:
        ...

    def registerEntries(
            self,
            vars: Dict[str, Any]) -> None:
        ...

    def runTask(
            self,
            handler: BaseTaskHandler) -> None:
        ...

    def scanPlugin(
            self,
            plugin: ModuleType) -> None:
        ...

    def shutdown(
            self) -> None:
        ...

    def takeTask(
            self,
            task: TaskInfo) -> bool:
        ...

    def updateBuildroots(
            self,
            nolocal: bool = False) -> None:
        ...

    def updateTasks(self) -> None:
        ...


def fast_incremental_upload(
        session: ClientSession,
        fname: str,
        fd: BufferedReader,
        path: str,
        retries: int,
        logger: Optional[Logger]) -> None:
    ...


def incremental_upload(
        session: ClientSession,
        fname: str,
        fd: BufferedReader,
        path: str,
        retries: int = 5,
        logger: Optional[Logger] = None) -> None:
    ...


def log_output(
        session: ClientSession,
        path: str,
        args: List[str],
        outfile: str,
        uploadpath: str,
        cwd: Optional[str] = None,
        logerror: int = 0,
        append: int = 0,
        chroot: Optional[str] = None,
        env: Optional[Dict[str, str]] = None) -> Optional[int]:
    ...


#  The end.
