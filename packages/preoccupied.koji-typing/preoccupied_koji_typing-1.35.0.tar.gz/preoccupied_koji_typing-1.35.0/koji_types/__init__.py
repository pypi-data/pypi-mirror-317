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
Koji Types - typing declatations for koji data structures

Python typing compatible definitions for the Koji dict types and
enumerations

:author: Christopher O'Brien <obriencj@gmail.com>
:license: GPL v3
"""


from datetime import datetime
from enum import IntEnum
from koji import (
    AUTHTYPES, BR_STATES, BR_TYPES, BUILD_STATES, CHECKSUM_TYPES,
    DEP_CONFLICT, DEP_ENHANCE, DEP_OBSOLETE, DEP_PROVIDE, DEP_RECOMMEND,
    DEP_REQUIRE, DEP_SUGGEST, DEP_SUPPLEMENT,
    REPO_STATES, RPM_SIGTAG_DSA, RPM_SIGTAG_GPG, RPM_SIGTAG_MD5,
    RPM_SIGTAG_PGP, RPM_SIGTAG_RSA, TASK_STATES, USERTYPES, USER_STATUS,
    ClientSession, PathInfo, )
from optparse import Values
from typing import (
    Any, Callable, Dict, Generic, Iterable, List, NewType, Optional,
    Tuple, TypeVar, Union, )
from typing_extensions import TypedDict


__all__ = (
    "ArchiveFileInfo",
    "ArchiveInfo",
    "ATypeID",
    "ATypeInfo",
    "AuthType",
    "BuildID",
    "BuildInfo",
    "BuildLogEntry",
    "BuildLogs",
    "BuildNVR",
    "BuildrootID",
    "BuildrootInfo",
    "BuildrootReference",
    "BuildrootState",
    "BuildrootType",
    "BuildState",
    "BuildSpecifier",
    "BTypeID",
    "BTypeInfo",
    "ChangelogEntry",
    "ChannelID",
    "ChannelInfo",
    "ChecksumType",
    "CGID",
    "CGInfo",
    "CGInitInfo",
    "CLIHandler",
    "CLIProtocol",
    "ExternalRepoID",
    "ExternalRepoInfo",
    "EventID",
    "EventInfo",
    "FilterOptions",
    "GOptions",
    "HistoryEntry",
    "HostID",
    "HostInfo",
    "Identifier",
    "ListTasksOptions",
    "MavenInfo",
    "NamedID",
    "NotificationID",
    "OldNew",
    "PackageID",
    "PackageInfo",
    "PermID",
    "PermInfo",
    "POMInfo",
    "QueryOptions",
    "RepoID",
    "RepoInfo",
    "RepoOptions",
    "RepoRequestID",
    "RepoState",
    "RPMFileInfo",
    "RPMID",
    "RPMInfo",
    "RPMNVRA",
    "RPMSignature",
    "RPMSigTag",
    "SearchResult",
    "SessionInfo",
    "TagBuildInfo",
    "TagExternalRepoEntry",
    "TagExternalRepos",
    "TagID",
    "TagInfo",
    "TagInheritance",
    "TagInheritanceEntry",
    "TagGroupID",
    "TagGroupInfo",
    "TagGroupPackage",
    "TagGroupReq",
    "TagPackageInfo",
    "TagPackageSimple",
    "TargetID",
    "TargetInfo",
    "TaskID",
    "TaskInfo",
    "TaskState",
    "UserData",
    "UserGroup",
    "UserID",
    "UserInfo",
    "UserStatus",
    "UserType",
    "WinInfo",
)


Identifier = NewType("Identifier", int)
"""
An int used as a unique identifier for a particular koji data type
"""

ArchiveID = NewType("ArchiveID", Identifier)
ATypeID = NewType("ATypeID", Identifier)
BuildID = NewType("BuildID", Identifier)
BuildrootID = NewType("BuildrootID", Identifier)
BTypeID = NewType("BTypeID", Identifier)
CGID = NewType("CGID", Identifier)
ChannelID = NewType("ChannelID", Identifier)
ExternalRepoID = NewType("ExternalRepoID", Identifier)
EventID = NewType("EventID", Identifier)
HostID = NewType("HostID", Identifier)
NotificationID = NewType("NotificationID", Identifier)
PackageID = NewType("PackageID", Identifier)
PermID = NewType("PermID", Identifier)
RepoID = NewType("RepoID", Identifier)
RepoRequestID = NewType("RepoRequestID", Identifier)
RPMID = NewType("RPMID", Identifier)
TagGroupID = NewType("TagGroupID", Identifier)
TagID = NewType("TagID", Identifier)
TargetID = NewType("TargetID", Identifier)
TaskID = NewType("TaskID", Identifier)
UserID = NewType("UserID", Identifier)


Data = Dict[str, Any]


class OldNew(TypedDict):
    old: str
    new: str


class NamedID(TypedDict):
    id: Identifier
    name: str


class AuthType(IntEnum):
    """
    Authentication method types

    See `koji.AUTHTYPES`
    """

    GSSAPI = AUTHTYPES['GSSAPI']
    """ user authenticated via GSSAPI """

    KERB = AUTHTYPES['KERBEROS']
    """ user authenticated via a Kerberos ticket """

    NORMAL = AUTHTYPES['NORMAL']
    """ user authenticated via password """

    SSL = AUTHTYPES['SSL']
    """ user authenticated via an SSL certificate """


class BuildrootState(IntEnum):
    """
    Values for a BuildrootInfo's br_state

    See `koji.BR_STATES`
    """

    INIT = BR_STATES['INIT']
    WAITING = BR_STATES['WAITING']
    BUILDING = BR_STATES['BUILDING']
    EXPIRED = BR_STATES['EXPIRED']


class BuildrootType(IntEnum):
    """
    Values for a BuildrootInfo's br_type

    See `koji.BR_TYPES`
    """

    STANDARD = BR_TYPES['STANDARD']
    EXTERNAL = BR_TYPES['EXTERNAL']


class BuildState(IntEnum):
    """
    Values for a BuildInfo's state.

    See `koji.BUILD_STATES`
    """

    BUILDING = BUILD_STATES["BUILDING"]
    """
    The build is still in-progress
    """

    COMPLETE = BUILD_STATES["COMPLETE"]
    """
    The build has been completed successfully
    """

    DELETED = BUILD_STATES["DELETED"]
    """
    The build has been deleted
    """

    FAILED = BUILD_STATES["FAILED"]
    """
    The build did not complete successfully due to an error
    """

    CANCELED = BUILD_STATES["CANCELED"]
    """
    The build did not complete successfully due to cancelation
    """


class ChecksumType(IntEnum):
    """
    Supported checksum types
    """

    MD5 = CHECKSUM_TYPES['md5']
    SHA1 = CHECKSUM_TYPES['sha1']
    SHA256 = CHECKSUM_TYPES['sha256']


class RepoState(IntEnum):
    INIT = REPO_STATES['INIT']
    READY = REPO_STATES['READY']
    EXPIRED = REPO_STATES['DELETED']
    PROBLEM = REPO_STATES['PROBLEM']


class RPMDepType(IntEnum):
    CONFLICT = DEP_CONFLICT
    ENHANCE = DEP_ENHANCE
    OBSOLETE = DEP_OBSOLETE
    PROVIDE = DEP_PROVIDE
    RECOMMEND = DEP_RECOMMEND
    REQUIRE = DEP_REQUIRE
    SUGGEST = DEP_SUGGEST
    SUPPLEMENT = DEP_SUPPLEMENT


class RPMSigTag(IntEnum):
    DSA = RPM_SIGTAG_DSA
    GPG = RPM_SIGTAG_GPG
    MD5 = RPM_SIGTAG_MD5
    PGP = RPM_SIGTAG_PGP
    RSA = RPM_SIGTAG_RSA


class TaskState(IntEnum):
    FREE = TASK_STATES['FREE']
    OPEN = TASK_STATES['OPEN']
    CLOSED = TASK_STATES['CLOSED']
    CANCELED = TASK_STATES['CANCELED']
    ASSIGNED = TASK_STATES['ASSIGNED']
    FAILED = TASK_STATES['FAILED']


class UserStatus(IntEnum):
    """
    Valid values for the ``'status'`` item of a `UserInfo` dict
    """

    NORMAL = USER_STATUS['NORMAL']
    """ account is enabled """

    BLOCKED = USER_STATUS['BLOCKED']
    """
    account is blocked. May not call XMLRPC endpoints requiring
    authentication
    """


class UserType(IntEnum):
    """
    Valid values for the ``'usertype'`` item of a `UserInfo` dict
    """

    NORMAL = USERTYPES['NORMAL']
    """ Account is a normal user """

    HOST = USERTYPES['HOST']
    """ Account is a build host """

    GROUP = USERTYPES['GROUP']
    """ Account is a group """


class ArchiveInfo(TypedDict):
    """
    Data representing a koji archive. These are typically obtained via
    the ``getArchive`` or ``listArchives`` XMLRPC calls.
    """

    btype: str
    """ Name of this archive's koji BType. eg. 'maven' or 'image' """

    btype_id: BTypeID
    """ ID of this archive's koji BType """

    build_id: BuildID
    """ ID of koji build owning this archive """

    buildroot_id: BuildrootID
    """ ID of the koji buildroot used to produce this archive """

    checksum: str
    """ hex representation of the checksum for this archive """

    checksum_type: ChecksumType
    """ type of cryptographic checksum used in the `checksum` field """

    extra: dict
    """ additional metadata provided by content generators """

    filename: str
    """ base filename for this archive """

    id: ArchiveID
    """ internal ID """

    metadata_only: bool

    size: int
    """ filesize in bytes """

    type_description: str
    """ this archive's type description """

    type_extensions: str
    """ space-delimited extensions shared by this archive's type """

    type_id: ATypeID
    """ ID of the archive's type """

    type_name: str
    """ name of the archive's type. eg. 'zip' or 'pom' """

    artifact_id: str
    """ Only present on maven archives. The maven artifact's name """

    group_id: str
    """ Only present on maven archives. The maven artifact's group """

    version: str
    """ Only present on maven archives. The maven artifact's version """

    platforms: List[str]
    """ Only present on Windows archives """

    relpath: str
    """ Only present on Windows archives """

    flags: str
    """ Only present on Windows archives """

    arch: str
    """ Only present on Image archives """


class ArchiveFileInfo(TypedDict):
    archive_id: ArchiveID
    """ owning archive record """

    name: str
    """ filename inside of archive """

    size: int
    """ uncompressed file size """


class ATypeInfo(TypedDict):

    description: str
    """ short title of the type """

    extensions: str
    """ space separated extensions for this type """

    id: ATypeID
    """ the internal ID of the archive type """

    name: str
    """ the name of the archive type """


class BuildrootReference(TypedDict):
    create_event: EventID
    host_id: HostID
    id: BuildrootID
    state: BuildrootState


class BuildrootInfo(TypedDict):
    arch: str
    br_type: BuildrootType

    cg_id: Optional[CGID]
    cg_name: Optional[str]
    cg_version: Optional[str]

    container_arch: str
    container_type: str

    create_event_id: EventID
    create_event_time: str
    create_ts: float

    extra: Optional[dict]

    host_arch: Optional[str]
    host_id: HostID
    host_name: str
    host_os: Optional[str]

    id: BuildrootID

    repo_create_event_id: EventID
    repo_create_event_time: str

    repo_id: RepoID
    repo_state: RepoState

    retire_event_id: EventID
    retire_event_time: str
    retire_ts: float

    state: BuildrootState

    tag_id: TagID
    tag_name: str

    task_id: TaskID

    workdir: str


class BuildNVR(TypedDict):
    name: str
    """ The name component of the NVR of a build. """

    version: str
    """ version portion of the NVR for a build """

    release: str
    """ release portion of the NVR for a build """

    epoch: Optional[str]
    """ optional epoch, or None """


class BuildInfo(BuildNVR):
    """
    Data representing a koji build. These are typically obtained via
    the ``getBuild`` XMLRPC call.
    """

    build_id: BuildID
    """ The internal ID for the build record """

    cg_id: Optional[CGID]
    """ The ID of the content generator which has reserved or produced
    this build """

    cg_name: Optional[str]
    """ The name of the content generator which has reserved or produced
    this build """

    completion_time: str
    """ ISO-8601 formatted UTC datetime stamp indicating when this build
    was completed """

    completion_ts: float
    """ UTC timestamp indicating when this build was completed """

    creation_event_id: EventID
    """ koji event ID at the creation of this build record """

    creation_time: str
    """ ISO-8601 formatted UTC datetime stamp indicating when this build
    record was created """

    creation_ts: float
    """ UTC timestamp indicating when this build record was created """

    draft: bool
    """
    Whether this build is flagged as a draft

    :since: koji 1.34.0
    """

    extra: dict
    """ flexible additional information for this build, used by content
    generators """

    id: BuildID
    """ Same as build_id """

    nvr: str
    """ The unique NVR of the build, comprised of the name, version, and
    release separated by hyphens """

    owner_id: UserID
    """ ID of the koji user that owns this build """

    owner_name: str
    """ name of the koji user that owns this build """

    package_id: PackageID
    """ The corresponding package ID for this build. """

    package_name: str
    """ should match the name value """

    source: str
    start_time: str
    start_ts: float

    state: BuildState
    """ state of the build, see `BuildState` """

    task_id: Optional[TaskID]

    volume_id: int
    """ ID of the storage volume that the archives for this build will be
    stored on """

    volume_name: str
    """ name of the storage that the archives for this build will be
    stored on """

    maven_group_id: Optional[str]
    """ only present on Maven builds which have been loaded with type
    information """

    maven_artifact_id: Optional[str]
    """ only present on Maven builds which have been loaded with type
    information """

    maven_version: Optional[str]
    """ only present on Maven builds which have been loaded with type
    information """

    platform: Optional[str]
    """ only present on Windows builds which have been loaded with type
    information """


class BuildLogEntry(TypedDict):
    dir: str
    """ log's immediate parent subdir """

    name: str
    """ log's file name """

    path: str
    """ log's path under topdir """


BuildLogs = List[BuildLogEntry]


BuildSpecifier = Union[str, BuildID, BuildNVR]


class TagBuildInfo(BuildInfo):
    """
    Form of BuildInfo as returned by ``listTagged``

    :since: 2.1
    """

    tag_id: TagID
    """ the ID of the tag this build was found in """

    tag_name: str
    """ the name of the tag this build was found in """


class BTypeInfo(TypedDict):
    id: BTypeID
    """ the internal ID of the btype """

    name: str
    """ the name of the btype """


class RPMNVRA(TypedDict):

    arch: str
    """ The RPM's architecture, eg. 'src' or 'x86_64' """

    name: str
    """ The RPM's name field """

    release: str
    """ The RPM's release field """

    version: str
    """ The RPM's version field """


class RPMInfo(RPMNVRA):
    """
    Data representing a koji RPM. These are typically obtained via the
    ``listRPMs`` XMLRPC call.
    """

    build_id: BuildID
    """ The ID of the build owning this RPM """

    buildroot_id: BuildrootID
    """ The buildroot used by the task which produced this RPM """

    buildtime: int
    """ UTC timestamp of the time that this RPM was produced """

    epoch: str
    """ The RPM's epoch field, or None if not defined """

    external_repo_id: ExternalRepoID
    """ The external repo ID for this RPM record, or 0 if the RPM was
    built in this koji instance rather than being a reference to an
    external repository """

    external_repo_name: str
    """ name identifying the repo that this RPM came from, or 'INTERNAL'
    if built in this koji instance """

    extra: dict
    """ Optional extra data """

    id: RPMID
    """ The internal ID for this RPM """

    metadata_only: bool

    nvr: str
    """ The NVR (Name Version and Release) of the RPM """

    payloadhash: str
    """ The MD5 in hex of the RPM's payload (the content past the
    headers) """

    size: int
    """ The file size of the unsigned copy of the RPM """


class RPMSignature(TypedDict):
    """
    Data representing an RPM signature in koji. Obtained via the
    ``queryRPMSigs`` XMLRPC API.
    """

    rpm_id: RPMID

    sigkey: str

    sighash: str


class HostInfo(TypedDict):
    """
    Data representing a koji host. These are typically obtained via the
    ``getHost`` XMLRPC call
    """

    arches: str
    """ space-separated list of architectures this host can handle """

    capacity: float
    """ maximum capacity for tasks, using the sum of the task weight
    values """

    comment: str
    """ text describing the current status or usage """

    description: str
    """ text describing this host """

    enabled: bool
    """ whether this host is configured by the hub to take tasks """

    id: HostID
    """ internal identifier """

    name: str
    """ user name of this host's account, normally FQDN. """

    ready: bool
    """ whether this host is reporting itself as active and prepared to
    accept tasks """

    task_load: float
    """ the load of currently running tasks on the host. Compared with the
    capacity and a given task's weight, this can determine whether a
    task will 'fit' on the host """

    user_id: UserID
    """ the user ID of this host's account. Hosts have a user account of
    type HOST, which is how they authenticate with the hub """


class UserGroup(TypedDict):
    """
    The results of the ``getUserGroups`` XMLRPC call

    :since: 2.2.0
    """

    id: UserID
    """ the ID of the group """

    name: str
    """ the name of the group """


class UserData(TypedDict):
    name: str
    """ the username """

    status: UserStatus
    """ status of the account. not present for members from the
    ``getGroupMembers`` call. """

    usertype: UserType
    """ type of the account """


class UserInfo(UserData):
    """
    Data representing a koji user account. These are typically
    obtained via the ``getUser`` or ``getLoggedInUser`` XMLRPC call
    """

    authtype: AuthType
    """ Only present from the ``getLoggedInUser`` call """

    groups: Optional[List[str]]
    """ names of groups that this user is a member of """

    id: UserID
    """ internal identifer """

    krb_principal: str
    """ kerberos principal associated with the user. Only used in koji
    before 1.19 or when using the ``getLoggedInUser`` call. """

    krb_principals: List[str]
    """ list of kerberos principals associated with the user. Used in koji
    from 1.19 onwards. """


class CGInfo(TypedDict):
    """
    Data representing a koji Content Generator. A dict of these are
    typically obtained via the ``listCGs`` XMLRPC call, mapping their
    friendly names to the CGInfo structure
    """

    id: CGID
    """ internal identifier """

    users: List[str]
    """ list of account names with access to perform CGImports using
    this content generator """


class CGInitInfo(TypedDict):
    """
    see ``CGInitBuild`` XMLRPC call
    """

    build_id: BuildID
    token: str


class PermInfo(TypedDict):
    id: PermID
    name: str


class RepoInfo(TypedDict):
    """
    Data representing a koji build tag's repository. These are
    typically obtained via the ``getRepo`` or ``repoInfo`` XMLRPC
    calls
    """

    create_event: EventID
    """ koji event ID representing the point that the repo's tag
    configuration was snapshot from. Note that this doesn't always
    correlate to the creation time of the repo -- koji has the ability to
    generate a repository based on older events """

    create_ts: float
    """ UTC timestamp indicating when this repo was created """

    creation_time: str
    """ ISO-8601 formatted UTC datetime stamp indicating when this repo
    was created """

    dist: bool
    """ whether this is a dist-repo or not """

    id: RepoID
    """ internal ID for this repository """

    state: RepoState
    """ the current state of this repository """

    tag_id: TagID
    """ ID of the tag from which this repo was generated. This value is not
    present in the output of the ``getRepo`` XMLRPC call as it is presumed
    that the caller already knows the tag's identity """

    tag_name: str
    """ name of the tag from which this repo was generated.  This value is
    not present in the output of the ``getRepo`` XMLRPC call as it is
    presumed that the caller already knows the tag's identity """

    task_id: TaskID
    """ ID of the task which generated this repository """


class RepoOptions(TypedDict):
    """
    opts used by ``host.repoInit`` XMLRPC call
    """

    debuginfo: bool
    separate_src: bool
    src: bool


class ExternalRepoInfo(TypedDict):

    id: ExternalRepoID

    name: str

    url: str


class TagExternalRepoEntry(TypedDict):

    arches: Optional[str]

    external_repo_id: ExternalRepoID
    external_repo_name: str

    tag_id: TagID
    tag_name: str

    merge_mode: int
    priority: int
    url: str


TagExternalRepos = List[TagExternalRepoEntry]
"""
The external repos associated with a tag.
"""


class TargetInfo(TypedDict):
    """
    Data representing a koji build target. Typically obtained via
    the ``getBuildTarget`` or ``getBuildTargets`` XMLRPC calls
    """

    build_tag: TagID
    """ internal ID of the target's build tag """

    build_tag_name: str
    """ name of the target's build tag """

    dest_tag: TagID
    """ internal ID of the target's destination tag """

    dest_tag_name: str
    """ name of the target's destination tag """

    id: TargetID
    """ internal ID of this build target """

    name: str
    """ name of this build target """


class TagInfo(TypedDict):
    """
    Data representing a koji tag. Typically obtained via the
    ``getTag`` XMLRPC call
    """

    arches: str
    """ space-separated list of architectures, or None """

    extra: Dict[str, str]
    """ inheritable additional configuration data """

    id: TagID
    """ internal ID of this tag """

    locked: bool
    """ when locked, a tag will protest against having addtional builds
    associated with it """

    maven_include_all: bool
    """ whether this tag should use the alternative maven-latest logic
    (including multiple builds of the same package name) when inherited
    by the build tag of a maven-enabled target """

    maven_support: bool
    """ whether this tag should generate a maven repository when it is
    the build tag for a target """

    name: str

    perm: str
    """ name of the required permission to associate builds with this tag,
    or None """

    perm_id: PermID
    """ ID of the required permission to associate builds with this tag,
    or None """


class TagInheritanceEntry(TypedDict):
    """
    Data representing a single inheritance element. A list of these
    represents the inheritance data for a tag. Typically obtained via
    the ``getInheritanceData`` XMLRPC call.
    """

    child_id: TagID
    """ the ID of the child tag in the inheritance link. The child tag
    inherits from the parent tag """

    intransitive: bool
    """ if true then this inheritance link would not be inherited. ie.
    this link only appears at a depth of 1, and is otherwise
    omitted. """

    maxdepth: int
    """ additional parents in the inheritance tree from this link are
    only considered up to this depth, relative from the link's current
    depth.  A maxdepth of 1 indicates that only the immediate parents
    will be inherited. A maxdepth of 0 indicates that the tag and none
    of its parents will be inherited. A value of None indicates no
    restriction. """

    name: str
    """ the parent tag's name """

    noconfig: bool
    """ if True then this inheritance link does not include tag
    configuration data, such as extras and groups """

    parent_id: TagID
    """ the parent tag's internal ID """

    pkg_filter: str
    """ a regex indicating which package entries may be inherited. If
    empty, all packages are inherited """

    priority: int
    """ the inheritance link priority, which provides an ordering for
    links at the same depth with the same child tag (ie. what order
    the parent links for a given tag are processed in). Lower
    priorities are processed first. """


TagInheritance = List[TagInheritanceEntry]
""" As returned by the ``getInheritanceData`` XMLRPC call. A list of
inheritance elements for a tag.  """


class TagFullInheritanceEntry(TagInheritanceEntry):

    currdepth: int
    """ only present from the ``getFullInheritance`` call. The
    inheritance depth this link occurs at. A depth of 1 indicates that
    the child tag would be the one originally queried for its
    inheritance tree """

    filter: list
    """ only present from the ``getFullInheritance`` call. """

    nextdepth: int
    """ only present from the ``getFullInheritance`` call. """


TagFullInheritance = List[TagFullInheritanceEntry]
""" As returned by the ``getFullInheritance`` XMLRPC call. A list of
inheritance elements for a tag.  """


class PackageInfo(TypedDict):
    """
    ``getPackage`` XMLRPC call.
    """

    id: PackageID
    """
    the internal ID for this package
    """

    name: str
    """
    the package name
    """


class TagPackageSimple(TypedDict):
    """
    ``listPackagesSimple`` XMLRPC call.
    """

    package_id: PackageID
    """ ID of the package """

    package_name: str
    """ name of the package """


class TagPackageInfo(TagPackageSimple):
    """
    ``listPackages`` XMLRPC call.
    """

    blocked: bool
    """ if True this entry represents a block """

    extra_arches: str
    """ additional architectures, separated by spaces """

    owner_id: UserID
    """ ID of the user who is the owner of the package for this tag """

    owner_name: str
    """ name of the user who is the owner of the package for this tag """

    tag_id: TagID
    """ ID of the package listing's tag """

    tag_name: str
    """ name of the package listing's tag """


class TagGroupPackage(TypedDict):
    basearchonly: str
    blocked: bool
    group_id: int
    package: str
    requires: str
    tag_id: TagID
    type: str


class TagGroupReq(TypedDict):
    blocked: bool
    group_id: int
    is_metapkg: bool
    name: str
    req_id: int
    tag_id: TagID
    type: str


class TagGroupInfo(TypedDict):
    """
    ``getTagGroups`` XMLRPC call
    """

    biarchonly: bool
    blocked: bool
    description: str
    display_name: str
    exported: bool
    group_id: TagGroupID
    grouplist: List[TagGroupReq]
    is_default: bool
    langonly: str
    name: str
    packagelist: List[TagGroupPackage]
    tag_id: TagID
    uservisible: bool


class TaskInfo(TypedDict):
    """
    ``getTaskInfo`` XMLRPC call
    """

    arch: str
    """ task architecture, or 'noarch' """

    awaited: Union[bool, None]
    """ True if this task is currently being waiting-for by its parent
    task.  False if this task is no longer being waited-for. None if
    the task was never waited-for. """

    channel_id: ChannelID
    """ internal ID of the channel from which a host will be selected to
    take this task """

    completion_time: str
    """ ISO-8601 formatted UTC datetime stamp indicating when this task
    was completed, or None if not completed """

    completion_ts: float
    """ UTC timestamp indicating when this task was completed, or None if
    not completed """

    create_time: str
    """ ISO-8601 formatted UTC datetime stamp indicating when this task
    was created """

    create_ts: float
    """ UTC timestamp indicating when this task was created """

    host_id: HostID
    """ host which has taken this task, or None """

    id: TaskID
    """ internal task ID """

    label: str
    """ task label, or None """

    method: str
    """ task method, indicates the type of work to be done """

    owner: int
    """ ID of the user that initiated this task """

    parent: Optional[TaskID]
    """ ID of the parent task, or None """

    priority: int

    start_time: str
    """ ISO-8601 formatted UTC datetime stamp indicating when this task
    was started by a host, or None if not yet started """

    start_ts: float
    """ UTC timestamp indicating when this task was started by a host, or
    None if not yet started """

    state: TaskState
    """ the current state of this task """

    waiting: Union[bool, None]
    """ True if this task is currently waiting for any of its subtasks to
    complete. False if this task is not waiting, or None if the task
    never needed to wait. """

    weight: float
    """ value which ascribes the general resources needed to perform this
    task. hosts have a limit to the number of resources which can be used
    to run tasks in parallel """

    request: List[Any]
    """ The task request info. Only present when the request parameter to
    the ``getTaskInfo`` call is `True`. Note that the `as_taskinfo`
    function does set that parameter to True. """


class ChannelInfo(TypedDict):
    id: ChannelID
    """ internal channel ID """

    name: str
    """ channel name """


class SearchResult(TypedDict):
    """ as returned by the ``search`` XMLRPC call """

    id: int
    """ result ID """

    name: str
    """ result name """


class GOptions(Values):
    """
    Represents the koji client configuration options as provided by the
    baseline koji CLI.

    `Values` instances with these fields are fed to a `CLIHandler`

    Returned by the ``get_options`` function from within the koji CLI
    utility, which cannot be imported normally. Default values for
    these are pulled from the profile configuration if unspecified as
    base CLI arguments.
    """

    authtype: str
    cert: Optional[str]
    debug: bool
    force_auth: bool
    keytab: Optional[str]
    noauth: bool
    password: Optional[str]
    plugin_paths: Optional[str]
    principal: Optional[str]
    profile: str
    quiet: bool
    runas: Optional[str]
    server: str
    skip_main: bool
    topdir: str
    topurl: str
    user: str
    weburl: str


HistoryEntry = Tuple[int, str, bool, Data]


class QueryOptions(TypedDict, total=False):
    """
    Various API calls use queryOpts dictionary for altering output
    format
    """

    asList: bool
    countOnly: bool
    group: str
    limit: int
    order: str
    offset: int


class FilterOptions(TypedDict, total=False):
    """
    the ``filterOpts`` argument for for ``filterResults`` and
    ``countAndFilterResults` XMLRPC calls
    """

    order: str
    offset: int
    limit: int
    noneGreatest: bool


class ListTasksOptions(TypedDict, total=False):
    """
    Specific filter dictionary for listTasks API call
    """

    arch: List[str]
    not_arch: List[str]
    state: List[int]
    not_state: List[int]
    owner: Union[int, List[int]]
    not_owner: Union[int, List[int]]
    host_id: Union[int, List[int]]
    not_host_id: Union[int, List[int]]
    channel_id: Union[int, List[int]]
    not_channel_id: Union[int, List[int]]
    parent: Union[int, List[int]]
    not_parent: Union[int, List[int]]
    decode: bool
    method: str
    createdBefore: Union[float, str]
    createdAfter: Union[float, str]
    startedBefore: Union[float, str]
    startedAfter: Union[float, str]
    completeBeforer: Union[float, str]
    completeAfter: Union[float, str]


class FaultInfo(TypedDict):
    faultCode: int
    faultString: str


class MavenInfo(TypedDict):
    group_id: str
    artifact_id: str
    version: str


class WinInfo(TypedDict):
    platform: str


class POMInfo(TypedDict):
    groupId: str
    artifactId: str
    version: str


class ChangelogEntry(TypedDict):
    author: str
    date: datetime
    date_ts: int
    text: str


class EventInfo(TypedDict):
    id: EventID
    ts: int


class SessionInfo(TypedDict):
    # TODO: incomplete

    user_id: UserID
    expired: bool
    master: int
    authtype: AuthType
    callnum: Optional[int]
    exclusive: bool


class RPMFileInfo(TypedDict):
    """
    Information about a file embedded inside an RPM's CPIO archive
    """

    digest: str
    digest_algo: ChecksumType  # TODO: see filedigestAlgo
    md5: str
    name: str
    size: int
    flags: int
    user: int
    group: int
    mtime: int
    mode: int

    rpm_id: Optional[RPMID]
    """
    the RPMInfo for the RPM that contains this file
    """


class RPMDepInfo(TypedDict):
    """
    ``getRPMDeps`` XMLRPC result
    """

    name: str
    version: str
    flags: int
    type: RPMDepType


# The end.
