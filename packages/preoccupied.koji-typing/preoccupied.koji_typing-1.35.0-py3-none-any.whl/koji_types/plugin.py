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
Koji Plugin Types - typing declatations for koji data structures

:author: Christopher O'Brien <obriencj@gmail.com>
:license: GPL v3
"""


from typing import TYPE_CHECKING, Callable
from typing_extensions import Protocol, TypeAlias


if TYPE_CHECKING:
    from enum import Enum as StrEnum

else:
    try:
        from enum import StrEnum
    except ImportError:
        from enum import Enum as StrEnum


__all__ = (
    "CallbackDecorator",
    "CallbackHandler",
    "CallbackProtocol",
    "CallbackType",
)


class CallbackType(StrEnum):

    # hub
    postBuildPromote = 'postBuildPromote'
    postBuildStateChange = 'postBuildStateChange'
    postCommit = 'postCommit'
    postImport = 'postImport'
    postPackageListChange = 'postPackageListChange'
    postRPMSign = 'postRPMSign'
    postRepoDone = 'postRepoDone'
    postRepoInit = 'postRepoInit'
    postTag = 'postTag'
    postTaskStateChange = 'postTaskStateChange'
    postUntag = 'postUntag'
    preBuildPromote = 'preBuildPromote'
    preBuildStateChange = 'preBuildStateChange'
    preCommit = 'preCommit'
    preImport = 'preImport'
    prePackageListChange = 'prePackageListChange'
    preRPMSign = 'preRPMSign'
    preRepoDone = 'preRepoDone'
    preRepoInit = 'preRepoInit'
    preTag = 'preTag'
    preTaskStateChange = 'preTaskStateChange'
    preUntag = 'preUntag'

    # builder
    postCreateDistRepo = 'postCreateDistRepo'
    postCreateRepo = 'postCreateRepo'
    postSCMCheckout = 'postSCMCheckout'
    preSCMCheckout = 'preSCMCheckout'


CallbackHandler: TypeAlias = \
    Callable[[CallbackType, ...], None]  # type: ignore[misc]


class CallbackProtocol(Protocol):

    def __call__(
            self,
            cbtype: CallbackType,
            *args, **kwargs) -> None:
        ...


CallbackDecorator: TypeAlias = \
    Callable[[CallbackHandler], CallbackHandler]


# The end.
