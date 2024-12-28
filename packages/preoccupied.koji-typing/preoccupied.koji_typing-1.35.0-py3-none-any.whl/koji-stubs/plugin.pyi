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

Typing annotations stub for koji.plugin

:author: Christopher O'Brien <obriencj@gmail.com>
:license: GPL v3
"""


from koji_types.cli import CLIHandler
from koji_types.plugin import (
    CallbackDecorator, CallbackHandler, CallbackType, )
from types import ModuleType
from typing import Dict, List, Optional, Union


callbacks: Dict[CallbackType, List[CallbackHandler]]


class PluginTracker:

    def __init__(
            self,
            path: Optional[str] = None,
            prefix: str = '_koji_plugin__'):
        ...

    def get(self,
            name: str) -> Optional[ModuleType]:
        ...

    def load(
            self,
            name: str,
            path: Optional[str] = None,
            reload: bool = False) -> ModuleType:
        ...

    def pathlist(
            self,
            path: Union[str, List[str]]) -> List[str]:
        ...


def callback(*cbtypes: str) -> CallbackDecorator:
    ...


def convert_datetime(f: CallbackHandler) -> CallbackHandler:
    ...


def export(f: CallbackHandler) -> CallbackHandler:
    ...


def export_in(
        module: str,
        alias: Optional[str] = None) -> CallbackDecorator:
    ...


def export_as(
        alias: str) -> CallbackDecorator:
    ...


def export_cli(f: CLIHandler) -> CLIHandler:
    ...


def ignore_error(f: CallbackHandler) -> CallbackHandler:
    ...


def register_callback(
        cbtype: CallbackType,
        func: CallbackHandler) -> None:
    ...


def run_callbacks(
        cbtype: CallbackType,
        *args, **kws) -> None:
    ...


# The end.
