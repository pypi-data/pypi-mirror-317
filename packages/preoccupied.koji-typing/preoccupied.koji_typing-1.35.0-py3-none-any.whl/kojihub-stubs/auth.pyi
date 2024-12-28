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

Typing annotations stub for kojihub.auth

:author: Christopher O'Brien <obriencj@gmail.com>
:license: GPL v3
"""


from .db import (
    DeleteProcessor, InsertProcessor, QueryProcessor,
    UpdateProcessor, nextval, )

from koji_types import (
    AuthType, PermID, UserData, UserID, UserStatus, UserType, )
from koji_types.hub import SessionAuth
from typing import (
    Any, Dict, List, Literal, Optional, Union, Tuple, overload, )
from logging import Logger


AUTH_METHODS: List[str]

logger: Logger
RetryWhitelist: List[str]


class Session:

    args: str
    callnum: Optional[int]
    exclusive: bool
    hostip: Optional[str]
    id: Optional[int]
    key: Optional[str]
    lockerror: Any
    logged_in: bool
    master: Optional[int]
    message: str
    user_data: Dict[str, Any]
    user_id: Optional[int]
    authtype: Optional[AuthType]

    def __init__(
            self,
            args: Optional[str] = None,
            hostip: Optional[str] = None):
        ...

    def assertLogin(self) -> None:
        ...

    def assertPerm(
            self,
            name: str) -> None:
        ...

    def assertUser(
            self,
            user_id: int) -> None:
        ...

    def checkKrbPrincipal(
            self,
            krb_principal: str) -> None:
        ...

    def checkLoginAllowed(
            self,
            user_id: UserID) -> None:
        ...

    def createSession(
            self,
            user_id: UserID,
            hostip: str,
            authtype: AuthType,
            master: Optional[int] = None,
            renew: bool = False) -> SessionAuth:
        ...

    def createUser(
            self,
            name: str,
            usertype: Optional[UserType] = None,
            status: Optional[UserStatus] = None,
            krb_principal: Optional[str] = None,
            krb_princ_check: bool = True) -> UserID:
        ...

    def createUserFromKerberos(
            self,
            krb_principal: str) -> UserID:
        ...

    def get_remote_ip(
            self,
            override: Optional[str] = None) -> str:
        ...

    def getConnInfo(self) -> Tuple[str, int, str, int]:
        ...

    def getHostId(self) -> int:
        ...

    def getPerms(self) -> Dict[str, int]:
        ...

    def getUserId(
            self,
            username: str) -> Optional[int]:
        ...

    def getUserIdFromKerberos(
            self,
            krb_principal: str) -> Optional[int]:
        ...

    @property
    def groups(self) -> Dict[int, str]:
        ...

    def hasGroup(
            self,
            group_id: int) -> bool:
        ...

    def hasPerm(self, name: str) -> bool:
        ...

    @property
    def host_id(self) -> int:
        ...

    def isUser(
            self,
            user_id: int) -> bool:
        ...

    def login(
            self,
            user,
            password,
            opts: Optional[Dict[str, Any]] = None,
            renew: bool = False,
            exclusive: bool = False) -> SessionAuth:
        ...

    def logout(
            self,
            session_id: Optional[int] = None) -> None:
        ...

    def logoutChild(
            self,
            session_id: int) -> None:
        ...

    def makeExclusive(
            self,
            force: bool = False) -> None:
        ...

    def makeShared(self) -> None:
        ...

    @property
    def perms(self) -> Dict[str, PermID]:
        ...

    def removeKrbPrincipal(
            self,
            name: Union[str, UserID],
            krb_principal: str) -> int:
        ...

    def setKrbPrincipal(
            self,
            name: Union[str, UserID],
            krb_principal: str,
            krb_princ_check: bool = True) -> int:
        ...

    def sslLogin(
            self,
            proxyuser: Optional[str] = None,
            proxyauthtype: Optional[str] = None,
            renew: bool = False,
            exclusive: Optional[bool] = None) -> SessionAuth:
        ...

    def subsession(
            self) -> SessionAuth:
        ...

    def validate(self) -> bool:
        ...


def exclusiveSession(*args, **opts) -> None:
    ...


def get_user_data(
        user_id: UserID) -> UserData:
    ...


def get_user_groups(
        user_id: UserID) -> Dict[UserID, str]:
    ...


@overload
def get_user_perms(
        user_id: int,
        with_groups: bool = True) -> List[str]:
    ...


@overload
def get_user_perms(
        user_id: int,
        with_groups: bool = True,
        *,
        inheritance_data: Literal[False]) -> List[str]:
    ...


@overload
def get_user_perms(
        user_id: int,
        with_groups: bool = True,
        *,
        inheritance_data: Literal[True]) -> Dict[str, List[str]]:
    ...


@overload
def get_user_perms(
        user_id: int,
        with_groups: bool = True,
        inheritance_data: bool = False) -> Union[List[str],
                                                 Dict[str, List[str]]]:
    ...


def login(*args, **opts) -> SessionAuth:
    ...


def logout(session_id: Optional[int] = None) -> None:
    ...


def logoutChild(session_id: int) -> None:
    ...


def sharedSession() -> None:
    ...


def sslLogin(*args, **opts) -> SessionAuth:
    ...


def subsession() -> SessionAuth:
    ...


# The end.
