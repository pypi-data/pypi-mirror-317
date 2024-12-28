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

Typing annotations stub for koji.arch

:author: Christopher O'Brien <obriencj@gmail.com>
:license: GPL v3
"""  # noqa: Y021


from json import JSONEncoder
from typing import Any, List, Optional, Tuple


class BytesJSONEncoder(JSONEncoder):

    def default(self, o: Any) -> str:
        ...


class Rpmdiff:

    ADDED: str
    REMOVED: str
    DEPFORMAT: str
    FORMAT: str
    PRCO: Tuple[str, str, str, str]
    PREREQ_FLAG: int
    TAGS: Tuple[int, ...]

    def __init__(
            self,
            old: str,
            new: str,
            ignore: Optional[List[int]] = None):
        ...

    def differs(self) -> bool:
        ...

    def kojihash(self, new: bool = False) -> str:
        ...

    def sense2str(self, sense: int) -> str:
        ...

    def textdiff(self) -> str:
        ...


# The end.
