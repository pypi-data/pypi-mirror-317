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

Typing annotations stub for kojihub.kojixmlrpc

:author: Christopher O'Brien <obriencj@gmail.com>
:license: GPL v3
"""


from datetime import datetime
from koji.policy import SimpleRuleSet
from koji.plugin import PluginTracker
from koji.xmlrpcplug import ExtendedMarshaller
from logging import Formatter, Handler
from threading import Lock
from typing import (
    Any, Callable, Dict, List, NoReturn, Optional, Tuple, Type, )


GLOBAL_HEADERS: List[Tuple[str, str]]

firstcall: bool
firstcall_lock: Lock
log_handler: Handler

_default_policies: Dict[str, str]


class HandlerAccess:

    def __init__(self, registry: HandlerRegistry):
        ...

    def call(
            self,
            __name: str,
            *args,
            **kwargs) -> Any:
        ...

    def get(self,
            name: str) -> Callable:
        ...


class HandlerRegistry:

    def __init__(self):
        ...

    def get(self,
            name: str) -> Callable:
        ...

    def getargspec(
            self,
            func: Callable) -> Tuple:
        # TODO: return type is getfullargspec
        ...

    def list_api(self) -> Dict[str, Any]:
        # TODO: new APIInfo TypedDict ?
        ...

    def register_function(
            self,
            function: Callable,
            name: Optional[str] = None) -> None:
        ...

    def register_instance(
            self,
            instance: Any) -> None:
        ...

    def register_module(
            self,
            instance: Any,
            prefix: Optional[str] = None) -> None:
        ...

    def register_plugin(
            self,
            plugin: Any) -> None:
        ...

    def system_listMethods(
            self) -> List[str]:
        ...

    def system_methodHelp(
            self,
            method: str) -> str:
        ...

    def system_methodSignature(
            self,
            method: str) -> NoReturn:
        ...


class HubFormatter(Formatter):
    ...


class Marshaller(ExtendedMarshaller):

    dispatch: Dict[Type, Callable]

    def dump_datetime(
            self,
            value: datetime,
            write: Callable) -> None:
        ...


class ModXMLRPCRequestHandler:

    def __init__(self, handlers: HandlerRegistry):
        ...

    def check_session(self) -> None:
        ...

    def enforce_lockout(self) -> None:
        ...

    def handle_request(
            self,
            req) -> None:
        ...

    def handle_rpc(
            self,
            environ: Dict[str, Any]) -> Any:
        ...

    def handle_upload(
            self,
            environ: Dict[str, Any]) -> Dict[str, Any]:
        ...

    def multiCall(
            self,
            calls: List[Dict[str, Any]]) -> Any:
        # TODO: a type for the call dict
        ...


def application(
        environ: Dict[str, Any],
        start_response: Callable[[str, Dict[str, str]], None]) -> List[str]:
    ...


def error_reply(
        start_response: Callable,
        status: int,
        response: str,
        extra_headers: Optional[Dict[str, str]] = None) -> List[str]:
    ...


def get_memory_usage() -> int:
    ...


def get_policy(
        opts: Dict[str, Any],
        plugins: PluginTracker) -> Dict[str, SimpleRuleSet]:
    ...


def get_registry(
        opts: Dict[str, Any],
        plugins: PluginTracker) -> HandlerRegistry:
    ...


def load_config(environ: Dict[str, Any]) -> Dict[str, Any]:
    ...


def load_plugins(opts: Dict[str, Any]) -> PluginTracker:
    ...


def offline_reply(
        start_response: Callable,
        msg: Optional[str] = None) -> List[str]:
    ...


def server_setup(environ: Dict[str, Any]) -> None:
    ...


def setup_logging1() -> None:
    ...


def setup_logging2(opts: Dict[str, Any]) -> None:
    ...


# The end.
