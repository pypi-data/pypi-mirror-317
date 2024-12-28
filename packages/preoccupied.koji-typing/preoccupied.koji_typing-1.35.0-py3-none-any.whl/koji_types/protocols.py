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
Koji Types - Client Session Protocols

The majority of definitions are in the typing stub for this module,
where they can be used for static analysis without impacting
runtime. During analysis these definitions will become Protocols, with
all of the various methods listed. However, we don't want the abstract
definitions of a Protocol to prevent subclass instantiation, so at
runtime these are just empty classes.

:author: Christopher O'Brien  <obriencj@gmail.com>
:license: GPL v3
"""


__all__ = (
    "ClientSession",
    "MultiCallSession",
)


class ClientSession:
    pass


class Host:
    pass


class MultiCallSession:
    pass


class MultiCallHost:
    pass


# The end.
