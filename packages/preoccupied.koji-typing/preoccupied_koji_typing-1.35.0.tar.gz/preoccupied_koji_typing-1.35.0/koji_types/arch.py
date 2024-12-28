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
Koji Types - Architectures

:author: Christopher O'Brien <obriencj@gmail.com>
:license: GPL v3
"""


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from enum import Enum as StrEnum

else:
    try:
        from enum import StrEnum
    except ImportError:
        from enum import Enum as StrEnum


__all__ = (
    "Arch",
)


class Arch(StrEnum):
    noarch = "noarch"
    athlon = "athlon"
    i686 = "i686"
    geode = "geode"
    i586 = "i586"
    i486 = "i486"
    i386 = "i386"
    x86_64 = "x86_64"
    amd64 = "amd64"
    ia32e = "ia32e"
    ppc64le = "ppc64le"
    ppc64p7 = "ppc64p7"
    ppc64pseries = "ppc64pseries"
    ppc64iseries = "ppc64iseries"
    ppc64 = "ppc64"
    ppc = "ppc"
    s390x = "s390x"
    s390 = "s390"
    sparc64v = "sparc64v"
    sparc64 = "sparc64"
    sparcv9v = "sparcv9v"
    sparcv9 = "sparcv9"
    sparcv8 = "sparcv8"
    sparc = "sparc"
    alphaev7 = "alphaev7"
    alphaev68 = "alphaev68"
    alphaev67 = "alphaev67"
    alphaev6 = "alphaev6"
    alphapca56 = "alphapca56"
    alphaev56 = "alphaev56"
    alphaev5 = "alphaev5"
    alphaev45 = "alphaev45"
    alphaev4 = "alphaev4"
    alpha = "alpha"
    armv7l = "armv7l"
    armv6l = "armv6l"
    armv5tejl = "armv5tejl"
    armv5tel = "armv5tel"
    armv7hnl = "armv7hnl"
    armv7hl = "armv7hl"
    armv6hl = "armv6hl"
    arm64 = "arm64"
    sh4a = "sh4a"
    sh4 = "sh4"
    sh3 = "sh3"
    ia64 = "ia64"


# The end.
