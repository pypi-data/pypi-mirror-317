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

Typing annotations stub for kojihub.kojihub

:author: Christopher O'Brien <obriencj@gmail.com>
:license: GPL v3
"""


from datetime import datetime
from koji import ParameterError
from koji.policy import BaseSimpleTest, MatchTest
from koji_types import (
    ArchiveFileInfo, ArchiveID, ArchiveInfo,
    ATypeID, ATypeInfo, BTypeInfo, BuildID, BuildInfo, BuildLogs,
    BuildNVR, BuildrootID, BuildrootInfo, BuildrootReference,
    BuildrootState, BuildSpecifier, BuildState, CGID, CGInfo,
    CGInitInfo, ChangelogEntry, ChannelID, ChannelInfo, ChecksumType,
    Data, EventID, EventInfo, ExternalRepoID, ExternalRepoInfo,
    FaultInfo, FilterOptions, HistoryEntry, HostID, HostInfo,
    Identifier, ListTasksOptions, MavenInfo, NamedID, NotificationID,
    OldNew, PackageID, PackageInfo, PermID, PermInfo, POMInfo,
    QueryOptions, RepoID, RepoInfo, RepoOptions, RepoState,
    RPMDepInfo, RPMDepType, RPMFileInfo, RPMID, RPMInfo, RPMNVRA,
    RPMSignature, RPMSigTag, SearchResult, SessionInfo, TagBuildInfo,
    TagExternalRepos, TagFullInheritance, TagFullInheritanceEntry,
    TagGroupID, TagGroupInfo, TagID, TagInfo, TagInheritance,
    TagPackageInfo, TagPackageSimple, TargetID, TargetInfo, TaskID,
    TaskInfo, TaskState, UserGroup, UserID, UserInfo, UserStatus,
    UserType, WinInfo, )
from koji_types.arch import Arch
from logging import ERROR, INFO, WARNING, Logger
from typing import (
    Any, Callable, Dict, Iterator, List, Literal, NoReturn, Optional, Set,
    Tuple, Type, TypeVar, Union, overload, )


NUMERIC_TYPES: Tuple[Type, ...]

logger: Logger


# === Policy Classes ===

class BuildTagInheritsFromTest(BaseSimpleTest):
    ...


class BuildTagTest(BaseSimpleTest):
    ...


class BuildTypeTest(BaseSimpleTest):
    ...


class CGMatchAllTest(BaseSimpleTest):
    ...


class CGMatchAnyTest(BaseSimpleTest):
    ...


class ChildTaskTest(MatchTest):
    ...


class HasTagTest(BaseSimpleTest):
    ...


class HasPermTest(BaseSimpleTest):
    ...


class ImportedTest(BaseSimpleTest):
    ...


class IsBuildOwnerTest(BaseSimpleTest):
    ...


class IsDraftTest(BaseSimpleTest):
    ...


class MethodTest(MatchTest):
    ...


class NewPackageTest(BaseSimpleTest):
    ...


class OperationTest(MatchTest):
    ...


class PackageTest(MatchTest):
    ...


class PolicyTest(BaseSimpleTest):
    ...


class ReleaseTest(MatchTest):
    ...


class SkipTagTest(BaseSimpleTest):
    ...


class SourceTest(MatchTest):
    ...


class TagTest(MatchTest):

    def get_tag(self, data: Data) -> TagInfo:
        ...


class UserInGroupTest(BaseSimpleTest):
    ...


class UserTest(MatchTest):
    ...


class VersionTest(MatchTest):
    ...


class VMTest(MatchTest):
    ...


class VolumeTest(MatchTest):
    ...


class FromTagTest(TagTest):

    def get_tag(self, data: Data) -> TagInfo:
        ...


# === Other Classes ===

class BuildRoot:

    def __init__(
            self,
            id: Optional[BuildrootID] = None):
        ...

    def assertHost(self, host_id: HostID) -> None:
        ...

    def assertStandard(self) -> None:
        ...

    def assertTask(self, task_id: TaskID) -> None:
        ...

    def cg_new(
            self,
            data: BuildrootInfo) -> BuildrootID:
        # TODO: new TypedDict for CGBuildrootInfo
        ...

    def getArchiveList(
            self,
            queryOpts: Optional[QueryOptions] = None) -> List[ArchiveInfo]:
        ...

    def getList(self) -> List[RPMInfo]:
        ...

    def load(
            self,
            id: BuildrootID) -> None:
        ...

    def new(self,
            host: HostID,
            repo: RepoID,
            arch: Arch,
            task_id: Optional[TaskID] = None,
            ctype: str = 'chroot') -> BuildrootID:
        ...

    def setList(
            self,
            rpmlist: List[RPMInfo]) -> None:
        ...

    def setState(
            self,
            state: BuildrootState) -> None:
        ...

    def setTools(
            self,
            tools: Optional[List[NamedID]]) -> None:
        ...

    def updateArchiveList(
            self,
            archives: List[ArchiveInfo],
            project: bool = False) -> None:
        ...

    def updateList(
            self,
            rpmlist: List[RPMInfo]) -> None:
        ...

    def verifyHost(self, host_id: HostID) -> bool:
        ...

    def verifyTask(self, task_id: TaskID) -> bool:
        ...


class CG_Importer:

    def __init__(self):
        ...

    def assert_cg_access(self) -> None:
        ...

    def assert_policy(self) -> None:
        ...

    def check_build_dir(
            self,
            delete: bool = False) -> None:
        ...

    def do_import(
            self,
            metadata: Union[str, Data, None],
            directory: str,
            token: Optional[str] = None) -> BuildInfo:
        ...

    def get_build(
            self,
            token: Optional[str] = None) -> BuildInfo:
        ...

    def get_metadata(
            self,
            metadata: Union[str, Dict, None],
            directory: str) -> Data:
        ...

    @classmethod
    def get_task_id_from_metadata(
            cls,
            metadata: Data) -> TaskID:
        ...

    def import_archive(
            self,
            buildinfo: BuildInfo,
            brinfo: BuildrootInfo,
            fileinfo: Data) -> None:
        ...

    def import_brs(self) -> None:
        ...

    def import_buildroot(
            self,
            entry: Data) -> BuildRoot:
        ...

    def import_components(
            self,
            archive_id: ArchiveID,
            fileinfo: Data) -> None:
        ...

    def import_log(
            self,
            buildinfo: BuildInfo,
            fileinfo: Data) -> None:
        ...

    def import_metadata(self) -> None:
        ...

    def import_outputs(self) -> None:
        ...

    def import_rpm(
            self,
            buildinfo: BuildInfo,
            brinfo: BuildrootInfo,
            fileinfo: Data) -> None:
        ...

    def log(self,
            msg: str,
            level: int = WARNING) -> None:
        ...

    def log_error(
            self,
            msg: str,
            *,
            level: int = ERROR) -> None:
        ...

    def log_info(
            self,
            msg: str,
            *,
            level: int = INFO) -> None:
        ...

    def log_warning(
            self,
            msg: str,
            *,
            level: int = WARNING) -> None:
        ...

    def match_components(
            self,
            components: List[Data]) \
            -> Tuple[List[Dict], List[Dict]]:
        ...

    def match_file(
            self,
            comp: Dict) -> Optional[ArchiveInfo]:
        ...

    def match_kojifile(
            self,
            comp: Dict) -> Optional[ArchiveInfo]:
        ...

    def match_rpm(
            self,
            comp: Dict) -> Optional[RPMInfo]:
        ...

    def move_cg_log_file(self) -> None:
        ...

    def prep_archive(
            self,
            fileinfo: ArchiveInfo) -> None:
        ...

    def prep_brs(self) -> None:
        ...

    def prep_build(
            self,
            token: Optional[str] = None) -> BuildInfo:
        ...

    def prep_buildroot(
            self,
            brdata: Data) -> Data:
        # TODO: TypedDict for this?
        ...

    def prep_outputs(self) -> None:
        ...

    def set_volume(self) -> None:
        ...

    def update_build(self) -> BuildInfo:
        ...


class HostExports:

    def assertPolicy(
            self,
            name,
            data: Data,
            default: str = 'deny') -> None:
        ...

    def checkPolicy(
            self,
            name: str,
            data: Data,
            default: str = 'deny',
            strict: bool = False) -> Tuple[bool, str]:
        ...

    def closeTask(
            self,
            task_id: TaskID,
            response: Any) -> None:
        ...

    def completeBuild(
            self,
            task_id: TaskID,
            build_id: BuildID,
            srpm: str,
            rpms: List[str],
            brmap: Optional[Dict[str, BuildrootID]] = None,
            logs: Optional[Dict[Arch, List[str]]] = None) -> BuildInfo:
        ...

    def completeImageBuild(
            self,
            task_id: TaskID,
            build_id: BuildID,
            results: Dict[str, Data]) -> None:
        ...

    def completeMavenBuild(
            self,
            task_id: TaskID,
            build_id: BuildID,
            maven_results: Any,
            rpm_results: Any) -> None:
        ...

    def completeWinBuild(
            self,
            task_id: TaskID,
            build_id: BuildID,
            results: Dict[str, Data],
            rpm_results: Any) -> None:
        ...

    def createMavenBuild(
            self,
            build_info: BuildInfo,
            maven_info: MavenInfo) -> None:
        ...

    def distRepoMove(
            self,
            repo_id: RepoID,
            uploadpath: str,
            arch: Arch) -> None:
        ...

    def evalPolicy(
            self,
            name: str,
            data: Data) -> str:
        ...

    def failBuild(
            self,
            task_id: TaskID,
            build_id: BuildID) -> None:
        ...

    def failTask(
            self,
            task_id: TaskID,
            response: Any) -> None:
        ...

    def freeTasks(
            self,
            tasks: List[TaskID]) -> None:
        ...

    def getID(self) -> HostID:
        ...

    def getHost(self) -> Tuple[List[HostID], List[TaskID]]:
        ...

    def getHostTasks(
            self) -> List[TaskInfo]:
        ...

    def getLoadData(
            self) -> Tuple[List[HostInfo], List[TaskInfo]]:
        ...

    def getTasks(
            self) -> List[TaskInfo]:
        ...

    def importArchive(
            self,
            filepath: str,
            buildinfo: BuildInfo,
            type: str,
            typeInfo: Data) -> None:
        ...

    def importImage(
            self,
            task_id: TaskID,
            build_info: BuildInfo,
            results: Dict[str, Data]) -> None:
        ...

    def importWrapperRPMs(
            self,
            task_id: TaskID,
            build_id: BuildID,
            rpm_results: Dict[str, List[str]]) -> None:
        ...

    def initBuild(
            self,
            data: Data) -> BuildID:
        ...

    def initImageBuild(
            self,
            task_id: TaskID,
            build_info: BuildInfo) -> BuildInfo:
        ...

    def initMavenBuild(
            self,
            task_id: TaskID,
            build_info: BuildInfo,
            maven_info: MavenInfo) -> BuildInfo:
        ...

    def initWinBuild(
            self,
            task_id: TaskID,
            build_info: BuildInfo,
            win_info: WinInfo) -> BuildInfo:
        ...

    def isEnabled(self) -> bool:
        ...

    def moveBuildToScratch(
            self,
            task_id: TaskID,
            srpm: str,
            rpms: List[str],
            logs: Optional[Dict[str, List[str]]] = None) -> None:
        ...

    def moveImageBuildToScratch(
            self,
            task_id: TaskID,
            results: Data) -> None:
        ...

    def moveMavenBuildToScratch(
            self,
            task_id: TaskID,
            results: Data,
            rpm_results: Data) -> None:
        ...

    def moveWinBuildToScratch(
            self,
            task_id: TaskID,
            results: Data,
            rpm_results: Data) -> None:
        ...

    def newBuildRoot(
            self,
            repo: RepoID,
            arch: Arch,
            task_id: Optional[TaskID] = None) -> BuildrootID:
        ...

    def openTask(
            self,
            task_id: TaskID) -> Optional[Data]:
        ...

    def refuseTask(
            self,
            task_id: TaskID,
            soft: bool = True,
            msg: str = '') -> None:
        ...

    def repoDone(
            self,
            repo_id: RepoID,
            data: Dict[Arch, Tuple[str, List[str]]],
            expire: bool = False,
            repo_json_updates: Optional[Data] = None) -> None:
        ...

    def repoInit(
            self,
            tag: Union[str, TagID],
            task_id: Optional[TaskID] = None,
            event: Optional[EventID] = None,
            opts: Optional[RepoOptions] = None) -> Tuple[RepoID, EventID]:
        ...

    def setBuildRootList(
            self,
            brootid: BuildrootID,
            rpmlist: List[RPMInfo],
            task_id: Optional[TaskID] = None) -> None:
        ...

    def setBuildRootState(
            self,
            brootid: BuildrootID,
            state: BuildrootState,
            task_id: Optional[TaskID] = None) -> None:
        ...

    def setHostData(
            self,
            hostdata: Data) -> None:
        ...

    def setTaskWeight(
            self,
            task_id: TaskID,
            weight: float) -> None:
        ...

    def subtask(
            self,
            method: str,
            arglist: List,
            parent: TaskID,
            **opts) -> TaskID:
        ...

    def subtask2(
            self,
            __parent: TaskID,
            __taskopts: Data,
            __method: str,
            *args,
            **opts) -> TaskID:
        ...

    def tagBuild(
            self,
            task_id: TaskID,
            tag: Union[str, TagID],
            build: BuildSpecifier,
            force: bool = False,
            fromtag: Union[str, TagID, None] = None) -> None:
        ...

    def tagNotification(
            self,
            is_successful: bool,
            tag_id: Union[str, TagID, None],
            from_id: Union[str, TagID, None],
            build_id: BuildID,
            user_id: Union[str, UserID, None],
            ignore_success: bool = False,
            failure_msg: str = '') -> None:
        ...

    def taskSetWait(
            self,
            parent: TaskID,
            tasks: Optional[List[TaskID]]) -> None:
        ...

    def taskWait(
            self,
            parent: TaskID) -> Tuple[List[int], List[int]]:
        ...

    def taskWaitResults(
            self,
            parent: TaskID,
            tasks: Optional[List[TaskID]],
            canfail: Optional[List[int]] = None) -> List[Tuple[int, Any]]:
        ...

    def updateBuildrootArchives(
            self,
            brootid: BuildrootID,
            task_id: TaskID,
            archives: List[ArchiveInfo],
            project: bool = False) -> None:
        ...

    def updateBuildRootList(
            self,
            brootid: BuildrootID,
            rpmlist: List[RPMInfo],
            task_id: Optional[TaskID] = None) -> None:
        ...

    def updateHost(
            self,
            task_load: float,
            ready: bool,
            data: Optional[Data] = None) -> None:
        ...

    def updateMavenBuildRootList(
            self,
            brootid: BuildrootID,
            task_id: TaskID,
            mavenlist: List[Data],
            ignore: Optional[List[Union[int, str]]] = None,
            project: bool = False,
            ignore_unknown: bool = False,
            extra_deps: Optional[List[Union[int, str]]] = None) -> None:
        ...

    def writeSignedRPM(
            self,
            an_rpm: str,
            sigkey: str,
            force: bool = False) -> None:
        ...


class Host:

    def __init__(
            self,
            id: Optional[HostID] = None):
        ...

    def getHostTasks(self) -> List[TaskInfo]:
        # TODO: maybe a new TaskStatus
        ...

    def getLoadData(self) -> Tuple[List[HostID], List[TaskID]]:
        # TODO: double check TaskID and not TaskInfo
        ...

    def isEnabled(self) -> bool:
        ...

    def taskSetWait(
            self,
            parent: TaskID,
            tasks: List[TaskID]) -> None:
        ...

    def taskUnwait(
            self,
            parent: TaskID) -> None:
        ...

    def taskWait(
            self,
            parent: TaskID) -> Tuple[List[TaskID], List[TaskID]]:
        ...

    def taskWaitCheck(
            self,
            parent: TaskID) -> Tuple[List[TaskID], List[TaskID]]:
        ...

    def taskWaitResults(
            self,
            parent: TaskID,
            tasks: List[TaskID],
            canfail: Optional[List[TaskID]] = None) \
            -> List[Tuple[TaskID, str]]:
        ...

    def updateHost(
            self,
            task_load: float,
            ready: bool) -> None:
        ...

    def verify(self) -> bool:
        ...


class MultiSum:

    def __init__(
            self,
            checksum_types: List[ChecksumType]):
        ...

    def update(self, buf: bytes) -> None:
        ...

    def to_hexdigest(self) -> Dict[ChecksumType, str]:
        ...


class RootExports:

    host: HostExports

    @staticmethod
    def CGImport(
            metadata: Union[str, Data],
            directory: str,
            token: Optional[str] = None) -> BuildInfo:
        ...

    @staticmethod
    def CGInitBuild(
            cg: str,
            data: Data) -> CGInitInfo:
        ...

    @staticmethod
    def CGRefundBuild(
            cg: str,
            build_id: BuildID,
            token: str,
            state: BuildState = BuildState.FAILED) -> None:
        ...

    @staticmethod
    def addArchiveType(
            name: str,
            description: str,
            extensions: str,
            compression_type: Optional[str] = None) -> None:
        ...

    @staticmethod
    def addBType(
            name: str) -> None:
        ...

    @staticmethod
    def addChannel(
            channel_name: str,
            description: Optional[str] = None) -> ChannelID:
        ...

    def addExternalRepoToTag(
            self,
            tag_info: Union[str, TagID],
            repo_info: Union[str, ExternalRepoID],
            priority: int,
            merge_mode: str = 'koji',
            arches: Optional[List[Arch]] = None) -> None:
        ...

    def addExternalRPM(
            self,
            rpminfo: Data,
            external_repo: Union[str, ExternalRepoID],
            strict: bool = True) -> None:
        ...

    @staticmethod
    def addGroupMember(
            group: Union[str, UserID],
            user: Union[str, UserID],
            strict: bool = True) -> None:
        ...

    def addHost(
            self,
            hostname: str,
            arches: List[Arch],
            krb_principal: Optional[str] = None,
            force: bool = False) -> HostID:
        ...

    @staticmethod
    def addHostToChannel(
            hostname: Union[str, HostID],
            channel_name: str,
            create: bool = False,
            force: bool = False) -> None:
        ...

    def addRPMSig(
            self,
            an_rpm: str,
            data: bytes) -> None:
        ...

    def addUserKrbPrincipal(
            self,
            user: Union[str, UserID],
            krb_principal: str) -> int:
        ...

    @staticmethod
    def addVolume(
            name: str,
            strict: bool = True) -> NamedID:
        ...

    def applyVolumePolicy(
            self,
            build: BuildSpecifier,
            strict: bool = False) -> None:
        ...

    @staticmethod
    def assignTask(
            task_id: TaskID,
            host: str,
            force: bool = False,
            override: bool = False) -> bool:
        ...

    def build(
            self,
            src: str,
            target: str,
            opts: Optional[Data] = None,
            priority: Optional[int] = None,
            channel: Optional[str] = None) -> int:
        ...

    def buildImage(
            self,
            name: str,
            version: str,
            arch: Arch,
            target: str,
            ksfile: str,
            img_type: str,
            opts: Optional[Data] = None,
            priority: Optional[int] = None) -> int:
        ...

    def buildImageIndirection(
            self,
            opts: Optional[Data] = None,
            priority: Optional[int] = None) -> TaskID:
        ...

    def buildImageOz(
            self,
            name: str,
            version: str,
            arches: List[Arch],
            target: str,
            inst_tree: str,
            opts: Optional[Data] = None,
            priority: Optional[int] = None) -> TaskID:
        ...

    def buildReferences(
            self,
            build: BuildID,
            limit: Optional[int] = None,
            lazy: bool = False) -> Data:
        ...

    def cancelBuild(
            self,
            buildID: BuildID,
            strict: bool = False) -> bool:
        ...

    def cancelTask(
            self,
            task_id: TaskID,
            recurse: bool = True) -> None:
        ...

    def cancelTaskChildren(
            self,
            task_id: TaskID) -> None:
        ...

    def cancelTaskFull(
            self,
            task_id: TaskID,
            strict: bool = True) -> None:
        ...

    def chainBuild(
            self,
            srcs: List[str],
            target: str,
            opts: Optional[Data] = None,
            priority: Optional[int] = None,
            channel: Optional[str] = None) -> int:
        ...

    def chainMaven(
            self,
            builds: List[Data],
            target: str,
            opts: Optional[Data] = None,
            priority: Optional[int] = None,
            channel: str = 'maven') -> int:
        ...

    @staticmethod
    def changeBuildVolume(
            build: Union[str, BuildID],
            volume: str,
            strict: bool = True) -> None:
        ...

    @staticmethod
    def checkTagAccess(
            tag_id: Union[str, TagID],
            user_id: Union[str, UserID, None] = None) \
            -> Tuple[bool, bool, str]:
        ...

    def checkTagPackage(
            self,
            tag: Union[str, TagID],
            pkg: Union[str, PackageID]) -> bool:
        ...

    def checkUpload(
            self,
            path: str,
            name: str,
            verify: Optional[ChecksumType] = None,
            tail: Optional[int] = None,
            volume: Optional[str] = None) -> Data:
        ...

    def count(
            self,
            methodName: str,
            *args: Any,
            **kw: Any) -> int:
        ...

    @overload
    def countAndFilterResults(
            self,
            methodName: str,
            *args,
            filterOpts: FilterOptions,
            **kw) -> Tuple[int, List[Data]]:
        ...

    @overload
    def countAndFilterResults(
            self,
            methodName: str,
            *args,
            **kw) -> Tuple[int, List[Data]]:
        ...

    @staticmethod
    def createBuildTarget(
            name: str,
            build_tag: Union[str, TagID],
            dest_tag: Union[str, TagID]) -> None:
        ...

    def createEmptyBuild(
            self,
            name: str,
            version: str,
            release: str,
            epoch: str,
            owner: Union[str, UserID, None] = None,
            draft: bool = False) -> BuildID:
        ...

    @staticmethod
    def createExternalRepo(
            name: str,
            url: str) -> ExternalRepoInfo:
        ...

    def createImageBuild(
            self,
            build_info: BuildSpecifier) -> None:
        ...

    def createMavenBuild(
            self,
            build_info: BuildSpecifier,
            maven_info: MavenInfo) -> None:
        ...

    def createNotification(
            self,
            user_id: UserID,
            package_id: PackageID,
            tag_id: TagID,
            success_only: bool) -> None:
        ...

    def createNotificationBlock(
            self,
            user_id: UserID,
            package_id: Optional[PackageID] = None,
            tag_id: Optional[TagID] = None) -> None:
        ...

    @staticmethod
    def createTag(
            name: str,
            parent: Optional[Union[str, TagID]] = None,
            arches: Optional[str] = None,
            perm: Optional[str] = None,
            locked: bool = False,
            maven_support: bool = False,
            maven_include_all: bool = False,
            extra: Optional[Dict[str, str]] = None) -> TagID:
        ...

    def createUser(
            self,
            username: str,
            status: Optional[UserStatus] = None,
            krb_principal: Optional[str] = None) -> UserID:
        ...

    def createWinBuild(
            self,
            build_info: BuildSpecifier,
            win_info: WinInfo) -> None:
        ...

    @staticmethod
    def deleteBuild(
            build: BuildSpecifier,
            strict: bool = True,
            min_ref_age: int = 604800) -> bool:
        ...

    @staticmethod
    def deleteBuildTarget(
            buildTargetInfo: Union[str, TargetID]) -> None:
        ...

    @staticmethod
    def deleteExternalRepo(
            info: Union[str, ExternalRepoID]) -> None:
        ...

    def deleteNotification(
            self,
            id: int) -> None:
        ...

    def deleteNotificationBlock(
            self,
            id: int) -> None:
        ...

    def deleteRPMSig(
            self,
            rpminfo: Union[str, RPMID, RPMNVRA],
            sigkey: Optional[str] = None,
            all_sigs: bool = False) -> None:
        ...

    @staticmethod
    def deleteTag(
            tagInfo: Union[str, TagID]) -> None:
        ...

    def disableChannel(
            self,
            channelname: Union[str, ChannelID],
            comment: Optional[str] = None) -> None:
        ...

    def disableHost(
            self,
            hostname: Union[str, HostID]) -> None:
        ...

    def disableUser(
            self,
            username: Union[str, UserID]) -> None:
        ...

    def distRepo(
            self,
            tag: Union[str, TagID],
            keys: List[str],
            **task_opts) -> TaskID:
        ...

    def downloadTaskOutput(
            self,
            taskID: TaskID,
            fileName: str,
            offset: int = 0,
            size: int = -1,
            volume: Optional[str] = None) -> str:
        ...

    @staticmethod
    def dropGroupMember(
            group: Union[str, UserID],
            user: Union[str, UserID]) -> None:
        ...

    def echo(self, *args) -> List:
        ...

    @staticmethod
    def editBuildTarget(
            buildTargetInfo: Union[str, TargetID],
            name: str,
            build_tag: Union[str, TagID],
            dest_tag: Union[str, TagID]) -> None:
        ...

    @staticmethod
    def editChannel(
            channelInfo: Union[str, ChannelID],
            **kw) -> bool:
        ...

    @staticmethod
    def editExternalRepo(
            info: Union[str, ExternalRepoID],
            name: Optional[str] = None,
            url: Optional[str] = None) -> None:
        ...

    @staticmethod
    def editHost(
            hostInfo: Union[str, HostID],
            **kw) -> bool:
        ...

    def editPermission(
            self,
            permission: Union[str, PermID],
            description: str) -> None:
        ...

    @staticmethod
    def editTag(
            tagInfo: Union[str, TagID],
            name: Optional[str],
            arches: Optional[str],
            locked: Optional[bool],
            permissionID: Optional[PermID],
            extra: Optional[Dict[str, str]] = None) -> None:
        ...

    @staticmethod
    def editTag2(
            tagInfo: Union[str, TagID],
            **kwargs) -> None:
        ...

    @staticmethod
    def editTagExternalRepo(
            tag_info: Union[str, TagID],
            repo_info: Union[str, ExternalRepoID],
            priority: Optional[int] = None,
            merge_mode: Optional[str] = None,
            arches: Optional[str] = None) -> bool:
        ...

    @staticmethod
    def editUser(
            userInfo: Union[str, UserID],
            name: Optional[str] = None,
            krb_principal_mappings: Optional[List[OldNew]] = None) -> None:
        ...

    def enableChannel(
            self,
            channelname: str,
            comment: Optional[str] = None) -> None:
        ...

    def enableHost(
            self,
            hostname: str) -> None:
        ...

    def enableUser(
            self,
            username: Union[str, UserID]) -> None:
        ...

    def error(self) -> NoReturn:
        ...

    @staticmethod
    def evalPolicy(
            name: str,
            data: Data) -> str:
        ...

    def fault(self) -> NoReturn:
        ...

    @overload
    def filterResults(
            self,
            methodName: str,
            *args,
            filterOpts: FilterOptions,
            **kw) -> List[Data]:
        ...

    @overload
    def filterResults(
            self,
            methodName: str,
            *args,
            **kw) -> List[Data]:
        ...

    @staticmethod
    def findBuildID(
            X: BuildSpecifier,
            strict: bool = False) -> Optional[BuildID]:
        ...

    def freeTask(
            self,
            task_id: TaskID) -> None:
        ...

    @staticmethod
    def getActiveRepos() -> List[RepoInfo]:
        ...

    @staticmethod
    def getAllArches() -> List[Arch]:
        ...

    def getAllPerms(self) -> List[PermInfo]:
        ...

    def getAPIVersion(self) -> int:
        ...

    @staticmethod
    def getArchive(
            archive_id: ArchiveID,
            strict: bool = False) -> Optional[ArchiveInfo]:
        ...

    @staticmethod
    def getArchiveFile(
            archive_id: ArchiveID,
            filename: str,
            strict: bool = False) -> Optional[ArchiveFileInfo]:
        ...

    @staticmethod
    def getArchiveType(
            filename: Optional[str] = None,
            type_name: Optional[str] = None,
            type_id: Optional[ATypeID] = None,
            strict: bool = False) -> Optional[ATypeInfo]:
        ...

    @staticmethod
    def getArchiveTypes() -> List[ATypeInfo]:
        ...

    def getAverageBuildDuration(
            self,
            package: Union[str, PackageID],
            age: Optional[int] = None) -> Optional[float]:
        ...

    @staticmethod
    def getBuild(
            buildInfo: BuildSpecifier,
            strict: bool = False) -> Optional[BuildInfo]:
        ...

    def getBuildConfig(
            self,
            tag: Union[str, TagID],
            event: Optional[EventID] = None) -> TagInfo:
        ...

    @staticmethod
    def getBuildLogs(
            build: BuildSpecifier) -> BuildLogs:
        ...

    def getBuildNotification(
            self,
            id: int,
            strict: bool = False) -> Optional[Data]:
        ...

    def getBuildNotificationBlock(
            self,
            id: int,
            strict: bool = False) -> Optional[Data]:
        ...

    def getBuildNotificationBlocks(
            self,
            userID: Union[str, UserID, None] = None) -> Data:
        ...

    def getBuildNotifications(
            self,
            userID: Union[str, UserID, None] = None) -> Data:
        ...

    @staticmethod
    def getBuildroot(
            buildrootID: BuildrootID,
            strict: bool = False) -> Optional[BuildrootInfo]:
        ...

    def getBuildrootListing(
            self,
            id: BuildrootID) -> List[RPMInfo]:
        ...

    @staticmethod
    def getBuildTarget(
            info: Union[str, TargetID],
            event: Optional[EventID] = None,
            strict: bool = False) -> Optional[TargetInfo]:
        ...

    @staticmethod
    def getBuildTargets(
            info: Union[str, TargetID, None] = None,
            event: Optional[EventID] = None,
            buildTagID: Union[str, TagID, TagInfo, None] = None,
            destTagID: Union[str, TagID, TagInfo, None] = None,
            queryOpts: Optional[QueryOptions] = None) -> List[TargetInfo]:
        ...

    @staticmethod
    def getBuildType(
            buildInfo: BuildSpecifier,
            strict: bool = False) -> Dict[str, dict]:
        ...

    def getChangelogEntries(
            self,
            buildID: Optional[int] = None,
            taskID: Optional[int] = None,
            filepath: Optional[str] = None,
            author: Optional[str] = None,
            before: Union[datetime, str, int, None] = None,
            after: Union[datetime, str, int, None] = None,
            queryOpts: Optional[QueryOptions] = None,
            strict: bool = False) -> List[ChangelogEntry]:
        ...

    @staticmethod
    def getChannel(
            channelInfo: Union[str, ChannelID],
            strict: bool = False) -> ChannelInfo:
        ...

    @overload
    def getEvent(
            self,
            id: EventID) -> Optional[EventInfo]:
        ...

    @overload
    def getEvent(
            self,
            id: EventID,
            strict: Literal[True]) -> EventInfo:
        # :since: koji 1.35
        ...

    @overload
    def getEvent(
            self,
            id: EventID,
            strict: bool = False) -> Optional[EventInfo]:
        # :since: koji 1.35
        ...

    @staticmethod
    def getExternalRepo(
            info: Union[str, ExternalRepoID],
            strict: bool = False,
            event: Optional[EventID] = None) -> ExternalRepoInfo:
        ...

    @staticmethod
    def getExternalRepoList(
            tag_info: Union[str, TagID],
            event: Optional[EventID] = None) -> TagExternalRepos:
        ...


    def getFullInheritance(
            self,
            tag: Union[str, TagID],
            event: Optional[EventID] = None,
            reverse: bool = False) -> TagInheritance:
        ...

    @staticmethod
    def getGroupMembers(
            group: Union[str, UserID]) -> List[UserInfo]:
        ...

    @staticmethod
    def getHost(
            hostInfo: Union[str, HostID],
            strict: bool = False,
            event: Optional[EventID] = None) -> HostInfo:
        ...

    @staticmethod
    def getImageArchive(
            archive_id: ArchiveID,
            strict: bool = False) -> Optional[ArchiveInfo]:
        ...

    @staticmethod
    def getImageBuild(
            buildInfo: BuildSpecifier,
            strict: bool = False) -> Optional[Dict[str, BuildID]]:
        ...

    def getInheritanceData(
            self,
            tag: Union[str, TagID],
            event: Optional[EventID] = None) -> TagInheritance:
        ...

    def getKojiVersion(self) -> str:
        # :since: koji 1.23
        ...

    @overload
    def getLastEvent(
            self,
            before: Union[int, float, None] = None) -> EventInfo:
        ...

    @overload
    def getLastEvent(
            self,
            before: Union[int, float, None] = None,
            strict: bool = True) -> EventInfo:
        # :since: koji 1.35
        ...

    @overload
    def getLastHostUpdate(
            self,
            hostID: HostID) -> Union[str, None]:
        ...

    @overload
    def getLastHostUpdate(
            self,
            hostID: HostID,
            ts: Literal[False]) -> Union[str, None]:
        ...

    @overload
    def getLastHostUpdate(
            self,
            hostID: HostID,
            ts: Literal[True]) -> Union[float, None]:
        ...

    @overload
    def getLastHostUpdate(
            self,
            hostID: HostID,
            ts: bool = False) -> Union[str, float, None]:
        ...

    @overload
    def getLatestBuilds(
            self,
            tag: Union[str, TagID],
            event: Optional[EventID] = None,
            package: Optional[str] = None,
            type: Optional[str] = None) -> List[TagBuildInfo]:
        ...

    @overload
    def getLatestBuilds(
            self,
            tag: Union[str, TagID],
            event: Optional[EventID] = None,
            package: Optional[str] = None,
            type: Optional[str] = None,
            draft: Optional[bool] = None) -> List[TagBuildInfo]:
        # :since: koji 1.34
        ...

    def getLatestMavenArchives(
            self,
            tag: Union[int, str],
            event: Optional[int] = None,
            inherit: bool = True) -> List[ArchiveInfo]:
        ...

    @overload
    def getLatestRPMS(
            self,
            tag: Union[str, TagID],
            package: Optional[str] = None,
            arch: Union[Arch, List[Arch], None] = None,
            event: Optional[EventID] = None,
            rpmsigs: bool = False,
            type: Optional[str] = None) -> Tuple[List[RPMInfo],
                                                 List[BuildInfo]]:
        ...

    @overload
    def getLatestRPMS(
            self,
            tag: Union[str, TagID],
            package: Optional[str] = None,
            arch: Union[Arch, List[Arch], None] = None,
            event: Optional[EventID] = None,
            rpmsigs: bool = False,
            type: Optional[str] = None,
            draft: Optional[bool] = None) -> Tuple[List[RPMInfo],
                                                   List[BuildInfo]]:
        # :since: koji 1.34
        ...

    def getLoggedInUser(self) -> UserInfo:
        ...

    @staticmethod
    def getMavenArchive(
            archive_id: ArchiveID,
            strict: bool = False) -> ArchiveInfo:
        ...

    @staticmethod
    def getMavenBuild(
            buildInfo: Union[str, BuildID],
            strict: bool = False) -> Data:
        # TODO: need a return typedict
        ...

    @staticmethod
    def getNextRelease(
            build_info: BuildNVR,
            incr: int = 1) -> str:
        ...

    @staticmethod
    def getPackage(
            info: Union[str, PackageID],
            strict: bool = False,
            create: bool = False) -> Optional[NamedID]:
        ...

    def getPackageConfig(
            self,
            tag: Union[str, TagID],
            pkg: Union[str, PackageID],
            event: Optional[EventID] = None) -> Optional[TagPackageInfo]:
        ...

    def getPackageID(
            self,
            name: str,
            strict: bool = False) -> Optional[PackageID]:
        ...

    def getPerms(self) -> List[str]:
        ...

    @overload
    @staticmethod
    def getRepo(
            tag: Union[str, TagID],
            state: Optional[RepoState] = None,
            event: Optional[EventID] = None,
            dist: bool = False) -> RepoInfo:
        ...

    @overload
    @staticmethod
    def getRepo(
            tag: Union[str, TagID],
            state: Optional[RepoState] = None,
            event: Optional[EventID] = None,
            dist: bool = False,
            min_event: Optional[EventID] = None) -> RepoInfo:
        # :since: koji 1.35
        ...

    @overload
    @staticmethod
    def getRPM(
            rpminfo: Union[str, RPMID, RPMNVRA],
            strict: bool = False) -> Optional[RPMInfo]:
        ...

    @overload
    @staticmethod
    def getRPM(
            rpminfo: Union[str, RPMID, RPMNVRA],
            strict: bool = False,
            *,
            multi: Literal[False]) -> Optional[RPMInfo]:
        ...

    @overload
    @staticmethod
    def getRPM(
            rpminfo: Union[str, RPMID, RPMNVRA],
            strict: bool = False,
            *,
            multi: Literal[True]) -> List[RPMInfo]:
        ...

    @overload
    @staticmethod
    def getRPM(
            rpminfo: Union[str, RPMID, RPMNVRA],
            strict: bool = False,
            multi: bool = False) -> Union[RPMInfo, List[RPMInfo], None]:
        ...

    def getRPMChecksums(
            self,
            rpm_id: RPMID,
            checksum_types: Optional[List[ChecksumType]] = None,
            cacheonly: bool = False) -> Dict[ChecksumType, str]:
        ...

    def getRPMDeps(
            self,
            rpmID: RPMID,
            depType: Optional[RPMDepType] = None,
            queryOpts: Optional[QueryOptions] = None,
            strict: bool = False) -> List[RPMDepInfo]:
        ...

    def getRPMFile(
            self,
            rpmID: RPMID,
            filename: str,
            strict: bool = False) -> Optional[RPMFileInfo]:
        ...

    @overload
    def getRPMHeaders(
            self,
            rpmID: Optional[RPMID] = None,
            taskID: Optional[TaskID] = None,
            filepath: Optional[str] = None,
            headers: Optional[List[str]] = None) -> Data:
        ...

    @overload
    def getRPMHeaders(
            self,
            rpmID: Optional[RPMID] = None,
            taskID: Optional[TaskID] = None,
            filepath: Optional[str] = None,
            headers: Optional[List[str]] = None,
            strict: Optional[bool] = False) -> Data:
        # :since: koji 1.29
        ...

    def getSessionInfo(
            self,
            details: bool = False,
            user_id: Optional[UserID] = None) -> Union[None, SessionInfo,
                                                       List[SessionInfo]]:
        ...

    @staticmethod
    def getTag(
            tagInfo: Union[str, TagID],
            strict: bool = False,
            event: Optional[EventID] = None,
            blocked: bool = False) -> Optional[TagInfo]:
        ...

    @staticmethod
    def getTagID(
            info: Union[str, TagID, Data],
            strict: bool = False,
            create: bool = False) -> Optional[TagID]:
        ...

    @staticmethod
    def getTagExternalRepos(
            tag_info: Union[str, TagID, None] = None,
            repo_info: Union[str, ExternalRepoID, None] = None,
            event: Optional[EventID] = None) -> TagExternalRepos:
        ...

    @staticmethod
    def getTagGroups(
            tag: Union[str, TagID],
            event: Optional[EventID] = None,
            inherit: bool = True,
            incl_pkgs: bool = True,
            incl_reqs: bool = True,
            incl_blocked: bool = False) -> List[TagGroupInfo]:
        ...

    def getTaskChildren(
            self,
            task_id: TaskID,
            request: Optional[bool] = False,
            strict: Optional[bool] = False) -> List[TaskInfo]:
        ...

    def getTaskDescendents(
            self,
            task_id: TaskID,
            request: bool = False) -> Dict[str, List[TaskInfo]]:
        ...

    @overload
    def getTaskInfo(
            self,
            task_id: List[TaskID],
            request: bool = False,
            strict: bool = False) -> List[TaskInfo]:
        ...

    @overload
    def getTaskInfo(
            self,
            task_id: TaskID,
            request: bool = False,
            strict: bool = False) -> TaskInfo:
        ...

    def getTaskRequest(
            self,
            taskId: TaskID) -> Data:
        ...

    def getTaskResult(
            self,
            taskId: TaskID,
            raise_fault: bool = True) -> Any:
        ...

    @overload
    @staticmethod
    def getUser(
            userInfo: Union[str, UserID, None] = None,
            strict: bool = False,
            krb_princs: bool = True) -> UserInfo:
        ...

    @overload
    @staticmethod
    def getUser(
            userInfo: Union[str, UserID, None] = None,
            strict: bool = False,
            krb_princs: bool = True,
            groups: bool = False) -> UserInfo:
        # :since: koji 1.34
        ...

    def getUserGroups(
            self,
            user: Union[int, str]) -> List[UserGroup]:
        # :since: koji 1.35
        ...

    @overload
    def getUserPerms(
            self,
            userID: Union[str, UserID, None] = None) -> List[str]:
        ...

    @overload
    def getUserPerms(
            self,
            userID: Union[str, UserID, None] = None,
            with_groups: bool = True) -> List[str]:
        # :since: koji 1.34
        ...

    def getUserPermsInheritance(
            self,
            userID: Union[str, UserID]) -> Dict[str, List[str]]:
        # :since: koji 1.34
        ...

    def getVolume(
            self,
            volume: str,
            strict: bool = False) -> Optional[NamedID]:
        ...

    @staticmethod
    def getWinArchive(
            archive_id: ArchiveID,
            strict: bool = False) -> ArchiveInfo:
        ...

    @staticmethod
    def getWinBuild(
            buildInfo: Union[str, BuildID],
            strict: bool = False) -> Data:
        ...

    @staticmethod
    def grantCGAccess(
            user: Union[str, UserID],
            cg: Union[str, CGID],
            create: bool = False) -> None:
        ...

    def grantPermission(
            self,
            userinfo: Union[str, UserID],
            permission: Union[str, PermID],
            create: bool = False,
            description: Optional[str] = None) -> None:
        ...

    @staticmethod
    def groupListAdd(
            taginfo: Union[str, TagID],
            grpinfo: Union[str, TagGroupID],
            block: bool = False,
            force: bool = False,
            **opts) -> None:
        ...

    @staticmethod
    def groupListBlock(
            taginfo: Union[str, TagID],
            grpinfo: Union[str, TagGroupID]) -> None:
        ...

    @staticmethod
    def groupListRemove(
            taginfo: Union[str, TagID],
            grpinfo: Union[str, TagGroupID],
            force: bool = False) -> None:
        ...

    @staticmethod
    def groupListUnblock(
            taginfo: Union[str, TagID],
            grpinfo: Union[str, TagGroupID]) -> None:
        ...

    @staticmethod
    def groupPackageListAdd(
            taginfo: Union[str, TagID],
            grpinfo: Union[str, TagGroupID],
            pkg_name: str,
            block: bool = False,
            force: bool = False,
            **opts) -> None:
        ...

    @staticmethod
    def groupPackageListBlock(
            taginfo: Union[str, TagID],
            grpinfo: Union[str, TagGroupID],
            pkg_name: str) -> None:
        ...

    @staticmethod
    def groupPackageListRemove(
            taginfo: Union[str, TagID],
            grpinfo: Union[str, TagGroupID],
            pkg_name: str) -> None:
        ...

    @staticmethod
    def groupPackageListUnblock(
            taginfo: Union[str, TagID],
            grpinfo: Union[str, TagGroupID],
            pkg_name: str) -> None:
        ...

    @staticmethod
    def groupReqListAdd(
            taginfo: Union[str, TagID],
            grpinfo: Union[str, TagGroupID],
            reqinfo: str,
            block: bool = False,
            force: bool = False,
            **opts) -> None:
        ...

    @staticmethod
    def groupReqListBlock(
            taginfo: Union[str, TagID],
            grpinfo: Union[str, TagGroupID],
            reqinfo: str) -> None:
        ...

    @staticmethod
    def groupReqListRemove(
            taginfo: Union[str, TagID],
            grpinfo: Union[str, TagGroupID],
            reqinfo: str,
            force: Optional[bool] = None) -> None:
        ...

    @staticmethod
    def groupReqListUnblock(
            taginfo: Union[str, TagID],
            grpinfo: Union[str, TagGroupID],
            reqinfo: str) -> None:
        ...

    def hasPerm(
            self,
            perm: str,
            strict: bool = False) -> bool:
        ...

    def hello(
            self,
            *args) -> str:
        ...

    def importArchive(
            self,
            filepath: str,
            buildinfo: BuildInfo,
            type: str,
            typeInfo: Data) -> ArchiveInfo:
        ...

    def importRPM(
            self,
            path: str,
            basename: str) -> RPMInfo:
        ...

    @staticmethod
    def listArchives(
            buildID: Optional[BuildID] = None,
            buildrootID: Optional[BuildrootID] = None,
            componentBuildrootID: Optional[BuildrootID] = None,
            hostID: Optional[HostID] = None,
            type: Optional[str] = None,
            filename: Optional[str] = None,
            size: Optional[int] = None,
            checksum: Optional[str] = None,
            checksum_type: Optional[ChecksumType] = None,
            typeInfo: Optional[Data] = None,
            queryOpts: Optional[QueryOptions] = None,
            imageID: Optional[int] = None,
            archiveID: Optional[ArchiveID] = None,
            strict: bool = False) -> List[ArchiveInfo]:
        ...

    @staticmethod
    def listArchiveFiles(
            archive_id: ArchiveID,
            queryOpts: Optional[QueryOptions] = None,
            strict: bool = False) -> List[ArchiveFileInfo]:
        ...

    @staticmethod
    def listBTypes(
            query: Optional[NamedID] = None,
            queryOpts: Optional[QueryOptions] = None) -> List[BTypeInfo]:
        ...

    def listBuildRPMs(
            self,
            build: BuildSpecifier) -> List[RPMInfo]:
        ...

    @staticmethod
    def listBuildroots(
            hostID: Optional[HostID] = None,
            tagID: Optional[TagID] = None,
            state: Union[BuildrootState, List[BuildrootState], None] = None,
            rpmID: Optional[RPMID] = None,
            archiveID: Optional[ArchiveID] = None,
            taskID: Optional[TaskID] = None,
            buildrootID: Optional[BuildrootID] = None,
            repoID: Optional[RepoID] = None,
            queryOpts: Optional[QueryOptions] = None) -> List[BuildrootInfo]:
        ...

    def listBuilds(
            self,
            packageID: Optional[PackageID] = None,
            userID: Optional[UserID] = None,
            taskID: Optional[TaskID] = None,
            prefix: Optional[str] = None,
            state: Optional[BuildState] = None,
            volumeID: Optional[int] = None,
            source: Optional[str] = None,
            createdBefore: Optional[str] = None,
            createdAfter: Optional[str] = None,
            completeBefore: Optional[str] = None,
            completeAfter: Optional[str] = None,
            type: Optional[str] = None,
            typeInfo: Optional[Dict] = None,
            queryOpts: Optional[QueryOptions] = None,
            pattern: Optional[str] = None,
            cgID: Optional[CGID] = None,
            draft: Optional[bool] = None) -> List[BuildInfo]:
        ...

    @staticmethod
    def listCGs() -> Dict[str, CGInfo]:
        ...

    @staticmethod
    def listChannels(
            hostID: Optional[HostID] = None,
            event: Optional[EventID] = None,
            enabled: Optional[bool] = None) -> List[ChannelInfo]:
        ...

    @staticmethod
    def listExternalRepos(
            info: Union[str, ExternalRepoID, None] = None,
            url: Optional[str] = None,
            event: Optional[EventID] = None,
            queryOpts: Optional[QueryOptions] = None) \
            -> List[ExternalRepoInfo]:
        ...

    def listHosts(
            self,
            arches: Optional[List[str]] = None,
            channelID: Optional[ChannelID] = None,
            ready: Optional[bool] = None,
            enabled: Optional[bool] = None,
            userID: Optional[UserID] = None,
            queryOpts: Optional[QueryOptions] = None) -> List[HostInfo]:
        ...

    def listPackages(
            self,
            tagID: Optional[TagID] = None,
            userID: Optional[UserID] = None,
            pkgID: Optional[PackageID] = None,
            prefix: Optional[str] = None,
            inherited: bool = False,
            with_dups: bool = False,
            event: Optional[EventID] = None,
            queryOpts: Optional[QueryOptions] = None,
            with_owners: bool = True,
            with_blocked: bool = True) -> List[TagPackageInfo]:
        ...

    def listPackagesSimple(
            self,
            prefix: Optional[str] = None,
            queryOpts: Optional[QueryOptions] = None) \
            -> List[TagPackageSimple]:
        ...

    def listRPMFiles(
            self,
            rpmID: RPMID,
            queryOpts: Optional[QueryOptions] = None) -> List[RPMFileInfo]:
        ...

    @staticmethod
    def listRPMs(
            buildID: Optional[BuildID] = None,
            buildrootID: Optional[BuildrootID] = None,
            imageID: Optional[int] = None,
            componentBuildrootID: Optional[BuildrootID] = None,
            hostID: Optional[HostID] = None,
            arches: Union[Arch, List[Arch], None] = None,
            queryOpts: Optional[QueryOptions] = None,
            draft: Optional[bool] = None) -> List[RPMInfo]:
        ...

    def listTagged(
            self,
            tag: Union[str, TagID],
            event: Optional[EventID] = None,
            inherit: bool = False,
            prefix: Optional[str] = None,
            latest: bool = False,
            package: Optional[str] = None,
            owner: Optional[Union[str, UserID]] = None,
            type: Optional[str] = None,
            strict: bool = True,
            extra: bool = False,
            draft: Optional[bool] = None) -> List[TagBuildInfo]:
        ...

    def listTaggedArchives(
            self,
            tag: Union[str, TagID],
            event: Optional[EventID] = None,
            inherit: bool = False,
            latest: bool = False,
            package: Optional[str] = None,
            type: Optional[str] = None,
            strict: bool = True,
            extra: bool = True) -> Tuple[List[ArchiveInfo],
                                         List[BuildInfo]]:
        ...

    @overload
    def listTaggedRPMS(
            self,
            tag: Union[str, TagID],
            event: Optional[EventID] = None,
            inherit: bool = False,
            latest: bool = False,
            package: Optional[str] = None,
            arch: Optional[Arch] = None,
            rpmsigs: bool = False,
            owner: Union[str, UserID, None] = None,
            type: Optional[str] = None,
            strict: bool = True,
            extra: bool = True) -> Tuple[List[RPMInfo], List[BuildInfo]]:
        ...

    @overload
    def listTaggedRPMS(
            self,
            tag: Union[str, TagID],
            event: Optional[EventID] = None,
            inherit: bool = False,
            latest: bool = False,
            package: Optional[str] = None,
            arch: Optional[Arch] = None,
            rpmsigs: bool = False,
            owner: Union[str, UserID, None] = None,
            type: Optional[str] = None,
            strict: bool = True,
            extra: bool = True,
            draft: Optional[bool] = None) \
            -> Tuple[List[RPMInfo], List[BuildInfo]]:
        # :since: koji 1.34
        ...

    @staticmethod
    def listTags(
            build: Optional[BuildSpecifier] = None,
            package: Union[str, PackageID, None] = None,
            perms: bool = True,
            queryOpts: Optional[QueryOptions] = None,
            pattern: Optional[str] = None) -> List[TagInfo]:
        ...

    @staticmethod
    def listTaskOutput(
            taskID: TaskID,
            stat: bool = False,
            all_volumes: bool = False,
            strict: bool = False) \
            -> Union[List[str],
                     Dict[str, List[str]],
                     Dict[str, Data],
                     Dict[str, Dict[str, Data]]]:
        ...

    def listTasks(
            self,
            opts: Optional[ListTasksOptions] = None,
            queryOpts: Optional[QueryOptions] = None) -> List[TaskInfo]:
        ...

    @overload
    def listUsers(
            self,
            userType: UserType = UserType.NORMAL,
            prefix: Optional[str] = None,
            queryOpts: Optional[QueryOptions] = None) -> List[UserInfo]:
        ...

    @overload
    def listUsers(
            self,
            userType: UserType = UserType.NORMAL,
            prefix: Optional[str] = None,
            queryOpts: Optional[QueryOptions] = None,
            perm: Optional[str] = None,
            inherited_perm: bool = False) -> List[UserInfo]:
        # :since: koji 1.35
        ...

    @staticmethod
    def listVolumes() -> List[NamedID]:
        ...

    def makeTask(
            self,
            *args,
            **opts) -> TaskID:
        ...

    def massTag(
            self,
            tag: Union[str, TagID],
            builds: List[Union[str, BuildID]]) -> None:
        # :since: koji 1.30
        ...

    def mavenBuild(
            self,
            url: str,
            target: str,
            opts: Optional[Data] = None,
            priority: Optional[int] = None,
            channel: str = 'maven') -> TaskID:
        ...

    def mavenEnabled(self) -> bool:
        ...

    def mergeScratch(
            self,
            task_id: TaskID) -> BuildID:
        ...

    def moveAllBuilds(
            self,
            tag1: Union[str, TagID],
            tag2: Union[str, TagID],
            package: Union[str, PackageID],
            force: bool = False) -> TaskID:
        ...

    def moveBuild(
            self,
            tag1: Union[str, TagID],
            tag2: Union[str, TagID],
            build: BuildSpecifier,
            force: bool = False) -> TaskID:
        ...

    @staticmethod
    def newGroup(
            name: str) -> UserID:
        ...

    def newRepo(
            self,
            tag: Union[str, TagID],
            event: Optional[EventID] = None,
            src: bool = False,
            debuginfo: bool = False,
            separate_src: bool = False) -> TaskID:
        ...

    @staticmethod
    def packageListAdd(
            taginfo: Union[str, TagID],
            pkginfo: Union[str, PackageID],
            owner: Union[str, UserID, None] = None,
            block: Optional[bool] = None,
            extra_arches: Optional[str] = None,
            force: bool = False,
            update: bool = False) -> None:
        ...

    @staticmethod
    def packageListBlock(
            taginfo: Union[str, TagID],
            pkginfo: Union[str, PackageID],
            force: bool = False) -> None:
        ...

    @staticmethod
    def packageListRemove(
            taginfo: Union[str, TagID],
            pkginfo: Union[str, PackageID],
            force: bool = False) -> None:
        ...

    @staticmethod
    def packageListSetArches(
            taginfo: Union[str, TagID],
            pkginfo: Union[str, PackageID],
            arches: str,
            force: bool = False) -> None:
        ...

    @staticmethod
    def packageListSetOwner(
            taginfo: Union[str, TagID],
            pkginfo: Union[str, PackageID],
            owner: Union[str, UserID],
            force: bool = False) -> None:
        ...

    @staticmethod
    def packageListUnblock(
            taginfo: Union[str, TagID],
            pkginfo: Union[str, PackageID],
            force: bool = False) -> None:
        ...

    @staticmethod
    def promoteBuild(
            build: Union[str, BuildID],
            force: bool = False) -> BuildInfo:
        ...

    @staticmethod
    def queryHistory(
            tables: Optional[List[str]] = None,
            **kwargs: Any) -> Dict[str, List[Data]]:
        ...

    @staticmethod
    def queryRPMSigs(
            rpm_id: Union[RPMID, str, BuildNVR, None] = None,
            sigkey: Optional[str] = None,
            queryOpts: Optional[QueryOptions] = None) -> List[RPMSignature]:
        ...

    def removeExternalRepoFromTag(
            self,
            tag_info: Union[str, TagID],
            repo_info: int) -> None:
        ...

    @staticmethod
    def removeHostFromChannel(
            hostname: str,
            channel_name: str) -> None:
        ...

    def removeUserKrbPrincipal(
            self,
            user: Union[str, UserID],
            krb_principal: str) -> UserID:
        ...

    @staticmethod
    def removeVolume(
            volume: str) -> None:
        ...

    @staticmethod
    def renameChannel(
            old: str,
            new: str) -> None:
        ...

    def repoDelete(
            self,
            repo_id: RepoID) -> int:
        ...

    def repoExpire(
            self,
            repo_id: RepoID) -> None:
        ...

    @staticmethod
    def repoInfo(
            repo_id: RepoID,
            strict: bool = False) -> RepoInfo:
        ...

    def repoProblem(
            self,
            repo_id: RepoID) -> None:
        ...

    @staticmethod
    def resetBuild(
            build: Union[str, BuildID]) -> None:
        ...

    def restartHosts(
            self,
            priority: int = 5,
            options: Optional[Data] = None) -> TaskID:
        ...

    def resubmitTask(
            self,
            taskID: TaskID) -> TaskID:
        ...

    @staticmethod
    def revokeCGAccess(
            user: Union[str, UserID],
            cg: Union[str, CGID]) -> None:
        ...

    def revokePermission(
            self,
            userinfo: Union[str, UserID],
            permission: Union[str, PermID]) -> None:
        ...

    def search(
            self,
            terms: str,
            type: str,
            matchType: str,
            queryOpts: Optional[QueryOptions] = None) -> List[SearchResult]:
        ...

    def setBuildOwner(
            self,
            build: BuildSpecifier,
            user: Union[str, UserID]) -> None:
        ...

    def setBuildTimestamp(
            self,
            build: BuildSpecifier,
            ts: Union[int, float]) -> None:
        ...

    def setInheritanceData(
            self,
            tag: Union[str, TagID],
            data: TagInheritance,
            clear: bool = False) -> None:
        ...

    def setTaskPriority(
            self,
            task_id: TaskID,
            priority: int,
            recurse: bool = True) -> None:
        ...

    @overload
    def showOpts(self) -> str:
        ...

    @overload
    def showOpts(
            self,
            as_string: Literal[True]) -> str:
        ...

    @overload
    def showOpts(
            self,
            as_string: Literal[False]) -> Data:
        ...

    @overload
    def showOpts(
            self,
            as_string: bool = True) -> Union[str, Data]:
        ...

    def showSession(self) -> str:
        ...

    def snapshotTag(
            self,
            src: Union[str, TagID],
            dst: Union[str, TagID],
            config: bool = True,
            pkgs: bool = True,
            builds: bool = True,
            groups: bool = True,
            latest_only: bool = True,
            inherit_builds: bool = True,
            event: Optional[EventID] = None,
            force: bool = False) -> None:
        ...

    def snapshotTagModify(
            self,
            src: Union[str, TagID],
            dst: Union[str, TagID],
            config: bool = True,
            pkgs: bool = True,
            builds: bool = True,
            groups: bool = True,
            latest_only: bool = True,
            inherit_builds: bool = True,
            event: Optional[EventID] = None,
            force: bool = False,
            remove: bool = False) -> None:
        ...

    def tagBuild(
            self,
            tag: Union[str, TagID],
            build: Union[str, BuildID],
            force: bool = False,
            fromtag: Union[str, TagID, None] = None) -> None:
        ...

    def tagBuildBypass(
            self,
            tag: Union[str, TagID],
            build: Union[str, BuildID],
            force: bool = False,
            notify: bool = False) -> None:
        ...

    @staticmethod
    def tagChangedSinceEvent(
            event: EventID,
            taglist: List[TagID]) -> bool:
        ...

    @staticmethod
    def tagFirstChangeEvent(
            tag: Union[str, TagID],
            after: Optional[EventID] = None,
            inherit: bool = True) -> Optional[EventID]:
        ...

    @staticmethod
    def tagLastChangeEvent(
            tag: Union[str, TagID],
            before: Optional[EventID] = None,
            inherit: bool = True) -> Optional[EventID]:
        ...

    def taskFinished(
            self,
            taskId: TaskID) -> bool:
        ...

    def untagBuild(
            self,
            tag: Union[str, TagID],
            build: Union[str, BuildID],
            strict: bool = True,
            force: bool = False) -> None:
        ...

    def untagBuildBypass(
            self,
            tag: Union[str, TagID],
            build: Union[str, BuildID],
            strict: bool = True,
            force: bool = False,
            notify: bool = False) -> None:
        ...

    @staticmethod
    def untaggedBuilds(
            name: Optional[str] = None,
            queryOpts: Optional[QueryOptions] = None,
            draft: Optional[bool] = None) -> List[BuildNVR]:
        ...

    def updateNotification(
            self,
            id: NotificationID,
            package_id: Union[str, PackageID, None],
            tag_id: Union[str, TagID, None],
            success_only: bool) -> None:
        ...

    def uploadFile(
            self,
            path: str,
            name: str,
            size: int,
            md5sum: str,
            offset: int,
            data: str,
            volume: Optional[str] = None,
            checksum: Union[str, Tuple[ChecksumType, str], None] = None) \
            -> bool:
        ...

    def winBuild(
            self,
            vm: str,
            url: str,
            target: str,
            opts: Optional[Data] = None,
            priority: Optional[int] = None,
            channel: str = 'vm') -> int:
        ...

    def winEnabled(self) -> bool:
        ...

    def wrapperRPM(
            self,
            build: Union[int, str],
            url: str,
            target: str,
            priority: Optional[int] = None,
            channel: str = 'maven',
            opts: Optional[Data] = None) -> TaskID:
        ...

    def writeSignedRPM(
            self,
            an_rpm: str,
            sigkey: str,
            force: bool = False) -> None:
        ...


class Task:

    fields: Tuple[Tuple[str, str], ...]
    id: TaskID
    logger: Logger

    def __init__(
            self,
            id: TaskID):
        ...

    def _close(
            self,
            result: Any,
            state: TaskState) -> bool:
        ...

    def _split_fields(
            self,
            fields: Optional[Tuple[Tuple[str, str], ...]] = None) \
            -> Tuple[List[str], List[str]]:
        ...

    def assertHost(
            self,
            host_id: HostID) -> None:
        ...

    def assertOwner(
            self,
            user_id: Optional[UserID] = None) -> None:
        ...

    def assign(
            self,
            host_id: HostID,
            force: bool = False) -> bool:
        ...

    def cancel(
            self,
            recurse: bool = True) -> bool:
        ...

    def cancelChildren(self) -> None:
        ...

    def cancelFull(
            self,
            strict: bool = True) -> None:
        ...

    def close(
            self,
            result: str) -> None:
        ...

    def fail(self,
             result: str) -> None:
        ...

    def free(self) -> bool:
        ...

    def getChildren(
            self,
            request: bool = False) -> List[TaskInfo]:
        ...

    def getInfo(
            self,
            strict: bool = True,
            request: bool = False) -> Optional[TaskInfo]:
        ...

    def getOwner(self) -> UserID:
        ...

    def getRequest(self) -> Data:
        ...

    def getResult(
            self,
            raise_fault: bool = True) -> str:
        ...

    def getState(self) -> TaskState:
        ...

    def isCanceled(self) -> bool:
        ...

    def isFailed(self) -> bool:
        ...

    def isFinished(self) -> bool:
        ...

    def lock(
            self,
            host_id: HostID,
            newstate: str = 'OPEN',
            force: bool = False) -> bool:
        ...

    def open(
            self,
            host_id: HostID) -> Optional[Data]:
        ...

    def runCallbacks(
            self,
            cbtype: str,
            old_info: TaskInfo,
            attr: str,
            new_val: Any) -> None:
        ...

    def setPriority(
            self,
            priority: int,
            recurse: bool = False) -> None:
        ...

    def setWeight(
            self,
            weight: float) -> None:
        ...

    def verifyHost(
            self,
            host_id: Optional[HostID] = None) -> bool:
        ...

    def verifyOwner(
            self,
            user_id: Optional[UserID] = None) -> bool:
        ...


# === functions ===


def _create_build_target(
        name: str,
        build_tag: Union[str, TagID],
        dest_tag: Union[str, TagID]) -> None:
    ...


def _delete_build(
        binfo: BuildInfo) -> None:
    ...


def _delete_build_symlinks(
        binfo: BuildInfo) -> None:
    ...


def _delete_event_id() -> None:
    ...


def _edit_build_target(
        buildTargetInfo: Union[str, TargetID],
        name: str,
        build_tag: Union[str, TagID],
        dest_tag: Union[str, TagID]) -> None:
    ...


def _get_build_target(
        task_id: TaskID) -> Optional[TargetInfo]:
    ...


def _import_wrapper(
        task_id: TaskID,
        build_info: BuildInfo,
        rpm_results: Dict[str, List[str]]) -> None:
    ...


def _promote_build(
        build: Union[str, BuildID],
        force: bool = False) -> BuildInfo:
    ...


def _scan_sighdr(
        sighdr: bytes,
        fn: str) -> Tuple[str, str]:
    ...


def _writeInheritanceData(
        tag_id: TagID,
        changes: TagInheritance,
        clear: bool = False) -> None:
    ...


def add_archive_type(
        name: str,
        description: str,
        extensions: str,
        compression_type: Optional[str] = None) -> None:
    ...


def add_btype(
        name: str) -> None:
    ...


def add_channel(
        channel_name: str,
        description: Optional[str] = None) -> ChannelID:
    ...


def add_external_repo_to_tag(
        tag_info: Union[str, TagID],
        repo_info: Union[str, ExternalRepoID],
        priority: int,
        merge_mode: str = 'koji',
        arches: Optional[str] = None) -> None:
    ...


def add_external_rpm(
        rpminfo: Data,
        external_repo: Union[str, ExternalRepoID],
        strict: bool = True) -> RPMInfo:
    ...


def add_group_member(
        group: Union[str, UserID],
        user: Union[str, UserID],
        strict: bool = True) -> None:
    ...


def add_host_to_channel(
        hostname: Union[str, HostID],
        channel_name: str,
        create: bool = False,
        force: bool = False) -> None:
    ...


def add_rpm_sig(
        an_rpm: str,
        sighdr: bytes) -> None:
    ...


def add_volume(
        name: str,
        strict: bool = True) -> NamedID:
    ...


@overload
def apply_volume_policy(
        build: BuildInfo,
        strict: bool = False) -> None:
    ...


@overload
def apply_volume_policy(
        build: BuildInfo,
        strict: bool = False,
        *,
        dry_run: Literal[False]) -> None:
    ...


@overload
def apply_volume_policy(
        build: BuildInfo,
        strict: bool = False,
        *,
        dry_run: Literal[True]) -> str:
    ...


@overload
def apply_volume_policy(
        build: BuildInfo,
        strict: bool = False,
        dry_run: bool = False) -> Optional[str]:
    ...


def assert_cg(
        cg: str,
        user: Union[str, UserID, None] = None) -> None:
    ...


def assert_policy(
        name: str,
        data: Data,
        default: str = 'deny',
        force: bool = False) -> None:
    ...


def assert_tag_access(
        tag_id: Union[str, TagID],
        user_id: Union[str, UserID, None] = None,
        force: bool = False) -> None:
    ...


def build_notification(
        task_id: TaskID,
        build_id: BuildID) -> None:
    ...


def build_references(
        build_id: BuildID,
        limit: Optional[int] = None,
        lazy: bool = False) -> Data:
    # TODO: create a TypedDict
    ...


def calculate_chsum(
        path: str,
        checksum_types: List[ChecksumType]) -> Dict[ChecksumType, str]:
    ...


def cancel_build(
        build_id: BuildSpecifier,
        cancel_task: bool = True) -> bool:
    ...


def cg_import(
        metadata: Union[str, Data],
        directory: str,
        token: Optional[str] = None) -> BuildInfo:
    ...


def cg_init_build(
        cg: str,
        data: Data) -> CGInitInfo:
    ...


def cg_refund_build(
        cg: str,
        build_id: BuildID,
        token: str,
        state: BuildState = BuildState.FAILED) -> None:
    ...


def change_build_volume(
        build: Union[str, BuildID],
        volume: str,
        strict: bool = True) -> None:
    ...


def check_noarch_rpms(
        basepath: str,
        rpms: List[str],
        logs: Optional[Dict[Arch, List[str]]] = None) -> List[str]:
    ...


def check_policy(
        name: str,
        data: Data,
        default: str = 'deny',
        strict: bool = False,
        force: bool = False) -> Tuple[bool, str]:
    ...


def check_rpm_sig(
        an_rpm: str,
        sigkey: str,
        sighdr: bytes) -> None:
    ...


def check_tag_access(
        tag_id: Union[str, TagID],
        user_id: Union[str, UserID, None] = None) -> Tuple[bool, bool, str]:
    ...


def check_volume_policy(
        data: Data,
        strict: bool = False,
        default: Optional[str] = None) -> Optional[NamedID]:
    ...


def clear_reservation(
        build_id: BuildID) -> None:
    ...


_CVT = TypeVar("_CVT")


@overload
def convert_value(
        value: Any,
        cast: _CVT,
        message: Optional[str] = None,
        exc_type: Type[BaseException] = ParameterError,
        none_allowed: bool = False,
        check_only: bool = False) -> Optional[_CVT]:
    ...


@overload
def convert_value(
        value: Any,
        *,
        message: Optional[str] = None,
        exc_type: Type[BaseException] = ParameterError,
        none_allowed: bool = False,
        check_only: bool = False) -> Any:
    ...


def create_build_target(
        name: str,
        build_tag: Union[str, TagID],
        dest_tag: Union[str, TagID]) -> None:
    ...


def create_external_repo(
        name: str,
        url: str) -> ExternalRepoInfo:
    ...


def create_rpm_checksum(
        rpm_id: RPMID,
        sigkey: str,
        chsum_dict: Dict[ChecksumType, str]) -> None:
    ...


def create_rpm_checksums_output(
        query_result: Data,
        list_chsum_sigkeys: List[ChecksumType]) \
        -> Dict[str, Dict[ChecksumType, str]]:
    ...


def create_tag(
        name: str,
        parent: Union[str, TagID, None] = None,
        arches: Optional[str] = None,
        perm: Union[str, PermID, None] = None,
        locked: bool = False,
        maven_support: bool = False,
        maven_include_all: bool = False,
        extra: Optional[Dict[str, str]] = None) -> TagID:
    ...


def delete_build(
        build: BuildSpecifier,
        strict: bool = True,
        min_ref_age: int = 604800) -> bool:
    ...


def delete_build_target(
        buildTargetInfo: Union[str, TargetID]) -> None:
    ...


def delete_external_repo(
        info: Union[str, ExternalRepoID]) -> None:
    ...


def delete_rpm_sig(
        rpminfo: Union[str, RPMID, RPMNVRA],
        sigkey: Optional[str] = None,
        all_sigs: bool = False) -> None:
    ...


def delete_tag(
        tagInfo: Union[str, TagID]) -> None:
    ...


def dist_repo_init(
        tag: Union[str, TagID],
        keys: List[str],
        task_opts: Data) -> Tuple[int, int]:
    ...


def draft_clause(
        draft: bool,
        table: Optional[str] = None) -> str:
    ...


def drop_group_member(
        group: Union[str, UserID],
        user: Union[str, UserID]) -> None:
    ...


def edit_build_target(
        buildTargetInfo: Union[str, TargetID],
        name: str,
        build_tag: Union[str, TagID],
        dest_tag: Union[str, TagID]) -> None:
    ...


def edit_channel(
        channelInfo: Union[str, ChannelID],
        **kw) -> bool:
    ...


def edit_external_repo(
        info: Union[str, ExternalRepoID],
        name: Optional[str] = None,
        url: Optional[str] = None) -> None:
    ...


def edit_host(
        hostInfo: Union[str, HostID],
        **kw) -> bool:
    ...


def edit_tag(
        tagInfo: Union[str, TagID],
        **kwargs) -> None:
    ...


def edit_tag_external_repo(
        tag_info: Union[str, TagID],
        repo_info: Union[str, ExternalRepoID],
        priority: Optional[int] = None,
        merge_mode: Optional[str] = None,
        arches: Optional[str] = None) -> bool:
    ...


def edit_user(
        userInfo: Union[str, UserID],
        name: Optional[str] = None,
        krb_principal_mappings: Optional[List[OldNew]] = None) -> None:
    ...


def ensure_volume_symlink(
        binfo: BuildInfo) -> None:
    ...


def eval_policy(
        name: str,
        data: Data) -> str:
    ...


def eventCondition(
        event: EventID,
        table: Optional[str] = None) -> str:
    ...


def find_build_id(
        X: BuildSpecifier,
        strict: bool = False) -> BuildID:
    ...


def generate_token(
        nbytes: int = 32) -> str:
    ...


def get_active_repos() -> List[RepoInfo]:
    ...


def get_all_arches() -> List[Arch]:
    ...


def get_archive(
        archive_id: ArchiveID,
        strict: bool = False) -> Optional[ArchiveInfo]:
    ...


def get_archive_file(
        archive_id: ArchiveID,
        filename: str,
        strict: bool = False) -> Optional[ArchiveFileInfo]:
    ...


def get_archive_type(
        filename: Optional[str] = None,
        type_name: Optional[str] = None,
        type_id: Optional[ATypeID] = None,
        strict: bool = False) -> ATypeInfo:
    ...


def get_archive_types() -> List[ATypeInfo]:
    ...


def get_build(
        buildInfo: BuildSpecifier,
        strict: bool = False) -> BuildInfo:
    ...


def get_build_logs(
        build: BuildSpecifier) -> BuildLogs:
    ...


def get_build_notifications(
        user_id: UserID) -> Data:
    # TODO: need a new TypedDict
    ...


def get_build_notification_blocks(
        user_id: UserID) -> Data:
    ...


def get_build_target(
        info: Union[str, TargetID],
        event: Optional[EventID] = None,
        strict: bool = False) -> Optional[TargetInfo]:
    ...


def get_build_target_id(
        info: Union[str, TargetID, Data],
        strict: bool = False,
        create: bool = False) -> Optional[TargetID]:
    ...


def get_build_targets(
        info: Union[str, TargetID, None] = None,
        event: Optional[EventID] = None,
        buildTagID: Union[str, TagID, TagInfo, None] = None,
        destTagID: Union[str, TagID, TagInfo, None] = None,
        queryOpts: Optional[QueryOptions] = None) -> List[TargetInfo]:
    ...


def get_build_type(
        buildInfo: Union[str, BuildID, BuildNVR, BuildInfo],
        strict: bool = False) -> Optional[BTypeInfo]:
    ...


def get_buildroot(
        buildrootID: BuildrootID,
        strict: bool = False) -> Optional[BuildrootInfo]:
    ...


def get_channel(
        channelInfo: Union[str, ChannelID],
        strict: bool = False) -> Optional[ChannelInfo]:
    ...


def get_channel_id(
        info: Union[str, ChannelID, Data],
        strict: bool = False,
        create: bool = False) -> Optional[ChannelID]:
    ...


def get_external_repo(
        info: Union[str, ExternalRepoID],
        strict: bool = False,
        event: Optional[EventID] = None) -> ExternalRepoInfo:
    ...


def get_external_repo_id(
        info: Union[str, ExternalRepoID, Data],
        strict: bool = False,
        create: bool = False) -> Optional[ExternalRepoID]:
    ...


def get_external_repo_list(
        tag_info: Union[str, TagID],
        event: Optional[EventID] = None) -> TagExternalRepos:
    ...


def get_external_repos(
        info: Union[str, ExternalRepoID, None] = None,
        url: Optional[str] = None,
        event: Optional[EventID] = None,
        queryOpts: Optional[QueryOptions] = None) -> List[ExternalRepoInfo]:
    ...


def get_group_id(
        info: Union[str, UserID, Data],
        strict: bool = False,
        create: bool = False) -> Optional[UserID]:
    ...


def get_group_members(
        group: Union[str, UserID]) -> List[UserInfo]:
    ...


def get_host(
        hostInfo: Union[str, HostID],
        strict: bool = False,
        event: Optional[EventID] = None) -> Optional[HostInfo]:
    ...


def get_id(
        table: str,
        info: Union[str, Identifier, Data],
        strict: bool = False,
        create: bool = False) -> Optional[Identifier]:
    ...


def get_image_archive(
        archive_id: ArchiveID,
        strict: bool = False) -> Optional[ArchiveInfo]:
    ...


def get_image_build(
        buildInfo: BuildSpecifier,
        strict: bool = False) -> Optional[Dict[str, BuildID]]:
    ...


def get_maven_archive(
        archive_id: ArchiveID,
        strict: bool = False) -> Optional[ArchiveInfo]:
    ...


def get_maven_build(
        buildInfo: Union[str, BuildID],
        strict: bool = False) -> Optional[Data]:
    # TODO: need a return typedict
    ...


def get_next_build(
        build_info: BuildNVR) -> BuildID:
    ...


def get_next_release(
        build_info: BuildNVR,
        incr: int = 1) -> str:
    ...


def get_notification_recipients(
        build: Optional[BuildInfo],
        tag_id: Optional[TagID],
        state: BuildState) -> List[str]:
    ...


def get_package_id(
        info: Union[str, PackageID, Data],
        strict: bool = False,
        create: bool = False) -> Optional[PackageID]:
    ...


def get_perm_id(
        info: Union[str, PermID, Data],
        strict: bool = False,
        create: bool = False) -> Optional[PermID]:
    ...


def get_reservation_token(
        build_id: BuildID) -> Optional[str]:
    ...


def get_rpm(
        rpminfo: Union[str, RPMID, RPMNVRA],
        strict: bool = False,
        multi: bool = False) -> Union[RPMInfo, List[RPMInfo], None]:
    ...


def get_tag(
        tagInfo: Union[str, TagID],
        strict: bool = False,
        event: Optional[EventID] = None,
        blocked: bool = False) -> Optional[TagInfo]:
    ...


def get_tag_external_repos(
        tag_info: Union[str, TagID, None] = None,
        repo_info: Union[str, ExternalRepoID, None] = None,
        event: Optional[EventID] = None) -> TagExternalRepos:
    ...


def get_tag_extra(
        tagInfo: Union[TagInfo, NamedID],
        event: Optional[EventID] = None,
        blocked: bool = False) -> Dict[str, Union[str, Tuple[bool, str]]]:
    ...


def get_tag_groups(
        tag: Union[str, TagID],
        event: Optional[EventID] = None,
        inherit: bool = True,
        incl_pkgs: bool = True,
        incl_reqs: bool = True) -> Dict[TagGroupID, TagGroupInfo]:
    ...


def get_tag_id(
        info: Union[str, TagID, Data],
        strict: bool = False,
        create: bool = False) -> Optional[TagID]:
    ...


def get_task_descendents(
        task: Task,
        childMap: Optional[Dict[str, List[TaskInfo]]] = None,
        request: bool = False) -> Dict[str, List[TaskInfo]]:
    ...


def get_upload_path(
        reldir: str,
        name: str,
        create: bool = False,
        volume: Optional[str] = None) -> str:
    ...


def get_user(
        userInfo: Union[str, UserID, None] = None,
        strict: bool = False,
        krb_princs: bool = True,
        groups: bool = False) -> Optional[UserInfo]:
    ...


def get_user_by_krb_principal(
        krb_principal: str,
        strict: bool = False,
        krb_princs: bool = True) -> Optional[UserInfo]:
    ...


def get_verify_class(
        verify: Optional[ChecksumType]) -> Optional[Callable]:
    ...


def get_win_archive(
        archive_id: ArchiveID,
        strict: bool = False) -> Optional[ArchiveInfo]:
    ...


def get_win_build(
        buildInfo: Union[str, BuildID],
        strict: bool = False) -> Optional[Data]:
    # TODO: need a return typedict
    ...


@overload
def grant_cg_access(
        user: Union[str, UserID],
        cg: Union[str, CGID]) -> None:
    ...


@overload
def grant_cg_access(
        user: Union[str, int],
        cg: Union[str, int],
        create: Literal[False]) -> None:
    ...


@overload
def grant_cg_access(
        user: Union[str, int],
        cg: str,
        create: Literal[True]) -> None:
    ...


@overload
def grant_cg_access(
        user: Union[str, int],
        cg: Union[str, int],
        create: bool = False) -> None:
    ...


def grp_pkg_add(
        taginfo: Union[str, TagID],
        grpinfo: Union[str, TagGroupID],
        pkg_name: str,
        block: bool = False,
        force: bool = False,
        **opts) -> None:
    ...


def grp_pkg_block(
        taginfo: Union[str, TagID],
        grpinfo: Union[str, TagGroupID],
        pkg_name: str) -> None:
    ...


def grp_pkg_remove(
        taginfo: Union[str, TagID],
        grpinfo: Union[str, TagGroupID],
        pkg_name: str) -> None:
    ...


def grp_pkg_unblock(
        taginfo: Union[str, TagID],
        grpinfo: Union[str, TagGroupID],
        pkg_name: str) -> None:
    ...


def grp_req_add(
        taginfo: Union[str, TagID],
        grpinfo: Union[str, TagGroupID],
        reqinfo: str,
        block: bool = False,
        force: bool = False,
        **opts) -> None:
    ...


def grp_req_block(
        taginfo: Union[str, TagID],
        grpinfo: Union[str, TagGroupID],
        reqinfo: str) -> None:
    ...


def grp_req_remove(
        taginfo: Union[str, TagID],
        grpinfo: Union[str, TagGroupID],
        reqinfo: str,
        force: Optional[bool] = None) -> None:
    ...


def grp_req_unblock(
        taginfo: Union[str, TagID],
        grpinfo: Union[str, TagGroupID],
        reqinfo: str) -> None:
    ...


def grplist_add(
        taginfo: Union[str, TagID],
        grpinfo: Union[str, TagGroupID],
        block: bool = False,
        force: bool = False,
        **opts) -> None:
    ...


def grplist_block(
        taginfo: Union[str, TagID],
        grpinfo: Union[str, TagGroupID]) -> None:
    ...


def grplist_remove(
        taginfo: Union[str, TagID],
        grpinfo: Union[str, TagGroupID],
        force: bool = False) -> None:
    ...


def grplist_unblock(
        taginfo: Union[str, TagID],
        grpinfo: Union[str, TagGroupID]) -> None:
    ...


def handle_upload(
        environ: Data) -> Data:
    ...


def import_archive(
        filepath: str,
        buildinfo: BuildInfo,
        type: str,
        typeInfo: Data,
        buildroot_id: Optional[BuildrootID] = None) -> ArchiveInfo:
    ...


def import_archive_internal(
        filepath: str,
        buildinfo: BuildInfo,
        type: str,
        typeInfo: Data,
        buildroot_id: Optional[int] = None,
        fileinfo: Optional[Data] = None) -> ArchiveInfo:
    ...


def import_build(
        srpm: str,
        rpms: List[str],
        brmap: Optional[Dict[str, BuildrootID]] = None,
        task_id: Optional[TaskID] = None,
        build_id: Optional[BuildID] = None,
        logs: Optional[Dict[Arch, List[str]]] = None) -> BuildInfo:
    ...


def import_build_log(
        fn: str,
        buildinfo: BuildInfo,
        subdir: Optional[str] = None) -> None:
    ...


def import_rpm(
        fn: str,
        buildinfo: Optional[BuildInfo] = None,
        brootid: Optional[int] = None,
        wrapper: bool = False,
        fileinfo: Optional[Data] = None) -> RPMInfo:
    ...


def import_rpm_file(
        fn: str,
        buildinfo: BuildInfo,
        rpminfo: RPMInfo) -> None:
    ...


def importImageInternal(
        task_id: TaskID,
        build_info: BuildInfo,
        imgdata: Data) -> None:
    ...


def list_archive_files(
        archive_id: ArchiveID,
        queryOpts: Optional[QueryOptions] = None,
        strict: bool = False) -> List[ArchiveFileInfo]:
    ...


def list_archives(
        buildID: Optional[BuildID] = None,
        buildrootID: Optional[BuildrootID] = None,
        componentBuildrootID: Optional[BuildrootID] = None,
        hostID: Optional[HostID] = None,
        type: Optional[str] = None,
        filename: Optional[str] = None,
        size: Optional[int] = None,
        checksum: Optional[int] = None,
        checksum_type: Optional[ChecksumType] = None,
        typeInfo: Optional[Data] = None,
        queryOpts: Optional[QueryOptions] = None,
        imageID: Optional[int] = None,
        archiveID: Optional[ArchiveID] = None,
        strict: bool = False) -> List[ArchiveInfo]:
    ...


def list_btypes(
        query: Optional[NamedID] = None,
        queryOpts: Optional[QueryOptions] = None) -> List[BTypeInfo]:
    ...


def list_channels(
        hostID: Optional[HostID] = None,
        event: Optional[EventID] = None,
        enabled: Optional[bool] = None) -> List[ChannelInfo]:
    ...


def list_cgs() -> Dict[str, CGInfo]:
    ...


def list_rpms(
        buildID: Optional[BuildID] = None,
        buildrootID: Optional[BuildrootID] = None,
        imageID: Optional[int] = None,
        componentBuildrootID: Optional[BuildrootID] = None,
        hostID: Optional[int] = None,
        arches: Union[Arch, List[Arch], None] = None,
        queryOpts: Optional[QueryOptions] = None,
        draft: Optional[bool] = None) -> List[RPMInfo]:
    ...


def list_tags(
        build: Optional[BuildSpecifier] = None,
        package: Union[str, PackageID, None] = None,
        perms: bool = True,
        queryOpts: Optional[QueryOptions] = None,
        pattern: Optional[str] = None) -> List[TagInfo]:
    # TODO: this can optionally be a slightly modified TagInfo if
    # package is specified, so we might need an overload
    ...


def list_task_output(
        taskID: TaskID,
        stat: bool = False,
        all_volumes: bool = False,
        strict: bool = False) -> Union[List[str],
                                       Dict[str, List[str]],
                                       Dict[str, Data],
                                       Dict[str, Dict[str, Data]]]:
    # TODO: oh my god the overload for this is going to be a mess
    ...


def list_user_krb_principals(
        user_info: Union[str, UserID, None] = None) -> List[str]:
    ...


def list_volumes() -> List[NamedID]:
    ...


def log_error(
        msg: str) -> None:
    ...


def lookup_build_target(
        info: str,
        strict: bool = False,
        create: bool = False) -> Optional[NamedID]:
    ...


def lookup_channel(
        info: Union[str, ChannelID, Data],
        strict: bool = False,
        create: bool = False) -> Optional[NamedID]:
    ...


def lookup_group(
        info: str,
        strict: bool = False,
        create: bool = False) -> Optional[NamedID]:
    ...


def lookup_name(
        table: str,
        info: Union[str, int, Data],
        strict: bool = False,
        create: bool = False) -> Optional[NamedID]:
    ...


def lookup_package(
        info: Union[str, PackageID, Data],
        strict: bool = False,
        create: bool = False) -> Optional[NamedID]:
    ...


def lookup_perm(
        info: Union[str, PermID, Data],
        strict: bool = False,
        create: bool = False) -> Optional[NamedID]:
    ...


def lookup_tag(
        info: Union[str, TaskID, Data],
        strict: bool = False,
        create: bool = False) -> Optional[NamedID]:
    ...


def make_task(
        method: str,
        arglist: List,
        **opts) -> TaskID:
    ...


def maven_tag_archives(
        tag_id: TagID,
        event_id: Optional[EventID] = None,
        inherit: bool = True) -> Iterator[ArchiveInfo]:
    ...


def merge_scratch(
        task_id: TaskID) -> BuildID:
    ...


_NameOrID = TypeVar("_NameOrID", str, int)


@overload
def name_or_id_clause(
        table: str,
        info: _NameOrID) -> Tuple[str, Dict[str, _NameOrID]]:
    ...


@overload
def name_or_id_clause(
        table: str,
        info: Data) -> Tuple[str, Data]:
    ...


def new_build(
        data: Data,
        strict: bool = False) -> Optional[BuildID]:
    ...


def new_group(
        name: str) -> UserID:
    ...


def new_image_build(
        build_info: BuildSpecifier) -> None:
    ...


def new_maven_build(
        build: BuildSpecifier,
        maven_info: MavenInfo) -> None:
    ...


def new_package(
        name: str,
        strict: bool = True) -> Optional[PackageID]:
    ...


def new_typed_build(
        build_info: BuildSpecifier,
        btype: str) -> None:
    ...


def new_win_build(
        build_info: BuildSpecifier,
        win_info: WinInfo) -> None:
    ...


def old_edit_tag(
        tagInfo: Union[str, TagID],
        name: Optional[str],
        arches: Optional[str],
        locked: Optional[bool],
        permissionID: Optional[PermID],
        extra: Optional[Dict[str, str]] = None) -> None:
    ...


def parse_json(
        value: Optional[str],
        desc: Optional[str] = None,
        errstr: Optional[str] = None) -> Any:
    ...


def pkglist_add(
        taginfo: Union[str, TagID],
        pkginfo: Union[str, PackageID],
        owner: Union[str, UserID, None] = None,
        block: Optional[bool] = None,
        extra_arches: Optional[str] = None,
        force: bool = False,
        update: bool = False) -> None:
    ...


def pkglist_block(
        taginfo: Union[str, TagID],
        pkginfo: Union[str, PackageID],
        force: bool = False) -> None:
    ...


def pkglist_remove(
        taginfo: Union[str, TagID],
        pkginfo: Union[str, PackageID],
        force: bool = False) -> None:
    ...


def pkglist_setarches(
        taginfo: Union[str, TagID],
        pkginfo: Union[str, PackageID],
        arches: str,
        force: bool = False) -> None:
    ...


def pkglist_setowner(
        taginfo: Union[str, TagID],
        pkginfo: Union[str, PackageID],
        owner: Union[str, UserID],
        force: bool = False) -> None:
    ...


def pkglist_unblock(
        taginfo: Union[str, TagID],
        pkginfo: Union[str, PackageID],
        force: bool = False) -> None:
    ...


def policy_data_from_task(
        task_id: TaskID) -> Data:
    ...


def policy_data_from_task_args(
        method: str,
        arglist: List) -> Data:
    ...


def policy_get_brs(
        data: Data) -> Set[Optional[BuildrootID]]:
    ...


@overload
def policy_get_build_tags(
        data: Data) -> List[str]:
    ...


@overload
def policy_get_build_tags(
        data: Data,
        taginfo: Literal[False]) -> List[str]:
    ...


@overload
def policy_get_build_tags(
        data: Data,
        taginfo: Literal[True]) -> List[TagInfo]:
    ...


@overload
def policy_get_build_tags(
        data: Data,
        taginfo: bool = False) -> Union[List[TagInfo], List[str]]:
    ...


def policy_get_build_types(
        data: Data) -> Set[str]:
    ...


def policy_get_cgs(
        data: Data) -> Set[Optional[str]]:
    ...


def policy_get_pkg(
        data: Data) -> PackageInfo:
    ...


def policy_get_release(
        data: Data) -> str:
    ...


def policy_get_user(
        data: Data) -> Optional[UserInfo]:
    ...


def policy_get_version(
        data: Data) -> str:
    ...


def query_buildroots(
        hostID: Optional[int] = None,
        tagID: Optional[TagID] = None,
        state: Union[BuildrootState, List[BuildrootState], None] = None,
        rpmID: Optional[RPMID] = None,
        archiveID: Optional[ArchiveID] = None,
        taskID: Optional[TaskID] = None,
        buildrootID: Optional[BuildrootID] = None,
        repoID: Optional[RepoID] = None,
        queryOpts: Optional[QueryOptions] = None) -> List[BuildrootInfo]:
    ...


def query_history(
        tables: Optional[List[str]] = None,
        **kwargs) -> List[HistoryEntry]:
    ...


def query_rpm_sigs(
        rpm_id: Union[RPMID, str, BuildNVR, None] = None,
        sigkey: Optional[str] = None,
        queryOpts: Optional[QueryOptions] = None) -> List[RPMSignature]:
    ...


def readDescendantsData(
        tag_id: TagID,
        event: Optional[EventID] = None) -> TagInheritance:
    ...


def readFullInheritance(
        tag_id: TagID,
        event: Optional[EventID] = None,
        reverse: bool = False) -> TagFullInheritance:
    ...


def readFullInheritanceRecurse(
        tag_id: TagID,
        event: EventID,
        order: TagFullInheritance,
        top: TagFullInheritanceEntry,
        hist: Dict[int, TagFullInheritance],
        currdepth: int,
        maxdepth: int,
        noconfig: bool,
        pfilter: List[str],
        reverse: bool) -> TagFullInheritance:
    ...


def readInheritanceData(
        tag_id: TagID,
        event: Optional[EventID] = None) -> TagInheritance:
    ...


def readPackageList(
        tagID: Optional[TagID] = None,
        userID: Optional[UserID] = None,
        pkgID: Optional[PackageID] = None,
        event: Optional[EventID] = None,
        inherit: bool = False,
        with_dups: bool = False,
        with_owners: bool = True,
        with_blocked: bool = True) -> Dict[PackageID, TagPackageInfo]:
    ...


def readTaggedArchives(
        tag: TagID,
        package: Union[str, PackageID, None] = None,
        event: Optional[EventID] = None,
        inherit: bool = False,
        latest: bool = True,
        type: Optional[str] = None,
        extra: bool = True) -> Tuple[List[ArchiveInfo], List[BuildInfo]]:
    ...


def readTaggedBuilds(
        tag: TagID,
        event: Optional[EventID] = None,
        inherit: bool = False,
        latest: bool = False,
        package: Optional[str] = None,
        owner: Optional[str] = None,
        type: Optional[str] = None,
        extra: bool = False,
        draft: Optional[bool] = None) -> List[BuildInfo]:
    ...


@overload
def readTaggedRPMS(
        tag: Union[str, TagID],
        package: Optional[str] = None,
        arch: Union[Arch, List[Arch], None] = None,
        event: Optional[EventID] = None,
        inherit: bool = False,
        latest: Union[bool, int] = True,
        rpmsigs: bool = False,
        owner: Optional[str] = None,
        type: Optional[str] = None,
        extra: bool = True) -> Tuple[List[RPMInfo], List[BuildInfo]]:
    ...


@overload
def readTaggedRPMS(
        tag: Union[str, TagID],
        package: Optional[str] = None,
        arch: Union[Arch, List[Arch], None] = None,
        event: Optional[EventID] = None,
        inherit: bool = False,
        latest: Union[bool, int] = True,
        rpmsigs: bool = False,
        owner: Optional[str] = None,
        type: Optional[str] = None,
        extra: bool = True,
        draft: Optional[bool] = None) \
        -> Tuple[List[RPMInfo], List[BuildInfo]]:
    # :since: koji 1.34
    ...


def readTagGroups(
        tag: Union[str, TagID],
        event: Optional[EventID] = None,
        inherit: bool = True,
        incl_pkgs: bool = True,
        incl_reqs: bool = True,
        incl_blocked: bool = False) -> List[TagGroupInfo]:
    ...


def recycle_build(
        old: BuildInfo,
        data: BuildInfo) -> None:
    ...


@overload
def reject_draft(
        data: BuildInfo,
        *,
        error: Optional[Type[BaseException]] = None) -> None:
    ...


@overload
def reject_draft(
        data: BuildInfo,
        is_rpm: Literal[False],
        error: Optional[Type[BaseException]] = None) -> None:
    ...


@overload
def reject_draft(
        data: RPMInfo,
        is_rpm: Literal[True],
        error: Optional[Type[BaseException]] = None) -> None:
    ...


@overload
def reject_draft(
        data: Union[BuildInfo, RPMInfo],
        is_rpm: bool = False,
        error: Optional[Type[BaseException]] = None) -> None:
    ...


def remove_external_repo_from_tag(
        tag_info: Union[str, TagID],
        repo_info: int) -> None:
    ...


def remove_host_from_channel(
        hostname: str,
        channel_name: str) -> None:
    ...


def remove_volume(
        volume: str) -> None:
    ...


def rename_channel(
        old: str,
        new: str) -> None:
    ...


def repo_delete(
        repo_id: RepoID) -> int:
    ...


def repo_expire(
        repo_id: RepoID) -> None:
    ...


def repo_expire_older(
        tag_id: TagID,
        event_id: EventID,
        dist: Optional[bool] = None) -> None:
    ...


def repo_info(
        repo_id: RepoID,
        strict: bool = False) -> Optional[RepoInfo]:
    ...


def repo_init(
        tag: Union[str, TagID],
        task_id: Optional[TaskID] = None,
        event: Optional[EventID] = None,
        opts: Optional[RepoOptions] = None) -> Tuple[RepoID, EventID]:
    ...


def repo_problem(
        repo_id: RepoID) -> None:
    ...


def repo_ready(
        repo_id: RepoID) -> None:
    ...


def repo_references(
        repo_id: RepoID) -> List[BuildrootReference]:
    ...


def repo_set_state(
        repo_id: RepoID,
        state: RepoState,
        check: bool = True) -> None:
    ...


def reset_build(
        build: Union[str, BuildID]) -> None:
    ...


def revoke_cg_access(
        user: Union[str, UserID],
        cg: Union[str, CGID]) -> None:
    ...


def rpmdiff(
        basepath: str,
        rpmlist: List[str],
        hashes: Dict[int, Dict[str, str]]) -> None:
    ...


def set_channel_enabled(
        channelname: str,
        enabled: bool = True,
        comment: Optional[str] = None) -> None:
    ...


def set_host_enabled(
        hostname: str,
        enabled: bool = True) -> None:
    ...


def set_tag_update(
        tag_id: TagID,
        utype: int,
        event_id: Optional[EventID] = None,
        user_id: Optional[UserID] = None) -> None:
    ...


def set_user_status(
        user: UserInfo,
        status: UserStatus) -> None:
    ...


def tag_changed_since_event(
        event: EventID,
        taglist: List[TagID]) -> bool:
    ...


def tag_first_change_event(
        tag: Union[str, TagID],
        after: Optional[EventID] = None,
        inherit: bool = True) -> Optional[EventID]:
    ...


def tag_last_change_event(
        tag: Union[str, TagID],
        before: Optional[EventID] = None,
        inherit: bool = True) -> Optional[EventID]:
    ...


def tag_notification(
        is_successful: bool,
        tag_id: Union[str, TagID, None],
        from_id: Union[str, TagID, None],
        build_id: BuildID,
        user_id: Union[str, UserID, None],
        ignore_success: bool = False,
        failure_msg: str = '') -> None:
    ...


def untagged_builds(
        name: Optional[str] = None,
        queryOpts: Optional[QueryOptions] = None,
        draft: Optional[bool] = None) -> List[BuildNVR]:
    ...


def verify_host_name(
        name: str) -> None:
    ...


def verify_name_internal(
        name: str) -> None:
    ...


def verify_name_user(
        name: Optional[str] = None,
        krb: Optional[str] = None) -> None:
    ...


def write_signed_rpm(
        an_rpm: str,
        sigkey: str,
        force: bool = False) -> None:
    ...


def writeInheritanceData(
        tag_id: TagID,
        changes: TagInheritance,
        clear: bool = False) -> None:
    ...


def xform_user_krb(
        entry: UserInfo) -> UserInfo:
    ...


# The end.
