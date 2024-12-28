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

Typing annotations stub for koji.xmlrpcplus

:author: Christopher O'Brien <obriencj@gmail.com>
:license: GPL v3
"""


from re import Pattern
from typing import (
    Any, Callable, Dict, Generator, List, Tuple, Optional,
    Union, overload, )
from xmlrpc.client import (
    DateTime, Fault, Marshaller, getparser, loads, )


class ExtendedMarshaller(Marshaller):

    MAXI8: int
    MINI8: int

    def dump_generator(
            self,
            value: Generator,
            write: Callable[[str], Any]) -> None:
        ...

    def dump_int(
            self,
            value: int,
            write: Callable[[str], Any]) -> None:
        ...

    def dump_re(
            self,
            value: Pattern,
            write: Callable[[str], Any]) -> None:
        ...


@overload
def dumps(
        params: Union[Fault, Tuple],
        methodname: Optional[str] = None,
        methodresponse: bool = False,
        encoding: Optional[str] = None,
        allow_none: bool = True,
        marshaller: Optional[Marshaller] = None) -> str:
    ...


@overload
def dumps(
        params: Union[Fault, Tuple],
        methodname: Optional[str] = None,
        methodresponse: Optional[bool] = None,
        encoding: Optional[str] = None,
        allow_none: int = 1,
        marshaller: Optional[Marshaller] = None) -> str:
    ...


# The end.
