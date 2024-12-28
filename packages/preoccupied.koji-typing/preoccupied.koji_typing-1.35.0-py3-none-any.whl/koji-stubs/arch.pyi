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
"""


from koji_types.arch import Arch
from typing import Dict, List, Tuple, Optional, overload


arches: Dict[Arch, Arch]
canonArch: Optional[Arch]
multilibArches: Dict[Arch, Tuple[Arch, ...]]


class ArchStorage:

    archlist: Arch
    basearch: Arch
    bestarch: Arch
    canonarch: Arch
    compatarches: Optional[List[Arch]]
    multilib: bool

    def __init__(self):
        ...

    def get_arch_list(
            self,
            arch: Arch) -> List[Arch]:
        ...

    def get_best_arch_from_list(
            self,
            archlist: List[Arch],
            fromarch: Optional[Arch] = None) -> Arch:
        ...

    def score(
            self,
            arch: Arch) -> int:
        ...

    def setup_arch(
            self,
            arch: Optional[Arch] = None,
            archlist_includes_compat_arch: bool = True) -> None:
        ...


def archDifference(
        myarch: Arch,
        targetarch: Arch) -> int:
    ...


def canCoinstall(
        arch1: Arch,
        arch2: Arch) -> bool:
    ...


def getArchList(
        thisarch: Optional[Arch] = None) -> List[Arch]:
    ...


def getBaseArch(
        myarch: Optional[Arch] = None) -> Arch:
    ...


def getBestArch(
        myarch: Optional[Arch] = None) -> Arch:
    ...


def getBestArchFromList(
        archlist: List[Arch],
        myarch: Optional[Arch] = None) -> Arch:
    ...


@overload
def getCanonArch(
        skipRpmPlatform: bool = False) -> Arch:
    ...


@overload
def getCanonArch(
        skipRpmPlatform: int = 0) -> Arch:
    ...


def getCanonARMArch(
        arch: Arch) -> Arch:
    ...


def getCanonPPCArch(
        arch: Arch) -> Arch:
    ...


def getCanonSPARCArch(
        arch: Arch) -> Arch:
    ...


def getCanonX86_64Arch(
        arch: Arch) -> Arch:
    ...


def getCanonX86Arch(
        arch: Arch) -> Arch:
    ...


def getMultiArchInfo(
        arch: Arch = ...) -> Optional[List[Arch]]:
    ...


def isMultiLibArch(
        arch: Optional[Arch] = None) -> bool:
    ...


def legitMultiArchesInSameLib(
        arch: Optional[Arch] = None) -> List[Arch]:
    ...


def score(
        arch: Arch) -> int:
    ...


# The end.
