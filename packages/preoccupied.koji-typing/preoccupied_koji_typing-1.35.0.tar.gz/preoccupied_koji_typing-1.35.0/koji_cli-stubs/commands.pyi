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
Koji CLI - commands typing stubs

Typing annotations stub for koji_cli.commands

:author: Christopher O'Brien <obriencj@gmail.com>
:license: GPL v3
"""


from koji_types import HistoryEntry
from koji_types.cli import CLIHandler
from typing import Dict, List


_table_keys: Dict[str, List[str]]


anon_handle_buildinfo: CLIHandler
anon_handle_download_build: CLIHandler
anon_handle_download_logs: CLIHandler
anon_handle_download_task: CLIHandler
anon_handle_hostinfo: CLIHandler
anon_handle_latest_build: CLIHandler
anon_handle_list_api: CLIHandler
anon_handle_list_buildroot: CLIHandler
anon_handle_list_builds: CLIHandler
anon_handle_list_channels: CLIHandler
anon_handle_list_external_repos: CLIHandler
anon_handle_list_groups: CLIHandler
anon_handle_list_history: CLIHandler
anon_handle_list_hosts: CLIHandler
anon_handle_list_notifications: CLIHandler
anon_handle_list_pkgs: CLIHandler
anon_handle_list_tag_inheritance: CLIHandler
anon_handle_list_tagged: CLIHandler
anon_handle_list_tags: CLIHandler
anon_handle_list_targets: CLIHandler
anon_handle_list_untagged: CLIHandler
anon_handle_list_users: CLIHandler
anon_handle_list_volumes: CLIHandler
anon_handle_mock_config: CLIHandler
anon_handle_repoinfo: CLIHandler
anon_handle_rpminfo: CLIHandler
anon_handle_scheduler_info: CLIHandler
anon_handle_search: CLIHandler
anon_handle_show_groups: CLIHandler
anon_handle_taginfo: CLIHandler
anon_handle_taskinfo: CLIHandler
anon_handle_userinfo: CLIHandler
anon_handle_wait_repo: CLIHandler
anon_handle_watch_logs: CLIHandler
anon_handle_watch_task: CLIHandler


handle_add_channel: CLIHandler
handle_add_external_repo: CLIHandler
handle_add_group: CLIHandler
handle_add_group_pkg: CLIHandler
handle_add_group_req: CLIHandler
handle_add_host: CLIHandler
handle_add_host_to_channel: CLIHandler
handle_add_notification: CLIHandler
handle_add_pkg: CLIHandler
handle_add_tag: CLIHandler
handle_add_tag_inheritance: CLIHandler
handle_add_target: CLIHandler
handle_add_user: CLIHandler
handle_add_volume: CLIHandler
handle_assign_task: CLIHandler
handle_block_group: CLIHandler
handle_block_group_pkg: CLIHandler
handle_block_group_req: CLIHandler
handle_block_notification: CLIHandler
handle_block_pkg: CLIHandler
handle_build: CLIHandler
handle_call: CLIHandler
handle_cancel: CLIHandler
handle_chain_build: CLIHandler
handle_clone_tag: CLIHandler
handle_disable_channel: CLIHandler
handle_disable_host: CLIHandler
handle_disable_user: CLIHandler
handle_dist_repo: CLIHandler
handle_edit_channel: CLIHandler
handle_edit_external_repo: CLIHandler
handle_edit_host: CLIHandler
handle_edit_notification: CLIHandler
handle_edit_permission: CLIHandler
handle_edit_tag: CLIHandler
handle_edit_tag_inheritance: CLIHandler
handle_edit_target: CLIHandler
handle_edit_user: CLIHandler
handle_enable_channel: CLIHandler
handle_enable_host: CLIHandler
handle_enable_user: CLIHandler
handle_free_task: CLIHandler
handle_grant_cg_access: CLIHandler
handle_grant_permission: CLIHandler
handle_image_build: CLIHandler
handle_image_build_indirection: CLIHandler
handle_import: CLIHandler
handle_import_archive: CLIHandler
handle_import_cg: CLIHandler
handle_import_comps: CLIHandler
handle_import_sig: CLIHandler
handle_list_permissions: CLIHandler
handle_list_signed: CLIHandler
handle_list_tasks: CLIHandler
handle_lock_tag: CLIHandler
handle_make_task: CLIHandler
handle_maven_build: CLIHandler
handle_maven_chain: CLIHandler
handle_moshimoshi: CLIHandler
handle_move_build: CLIHandler
handle_promote_build: CLIHandler
handle_prune_signed_copies: CLIHandler
handle_regen_repo: CLIHandler
handle_remove_external_repo: CLIHandler
handle_remove_group: CLIHandler
handle_remove_host_from_channel: CLIHandler
handle_remove_notification: CLIHandler
handle_remove_pkg: CLIHandler
handle_remove_sig: CLIHandler
handle_remove_tag: CLIHandler
handle_remove_tag_inheritance: CLIHandler
handle_remove_target: CLIHandler
handle_request_repo: CLIHandler
handle_restart_hosts: CLIHandler
handle_resubmit: CLIHandler
handle_revoke_cg_access: CLIHandler
handle_revoke_permission: CLIHandler
handle_scheduler_logs: CLIHandler
handle_set_build_volume: CLIHandler
handle_set_pkg_arches: CLIHandler
handle_set_pkg_owner: CLIHandler
handle_set_pkg_owner_global: CLIHandler
handle_set_task_priority: CLIHandler
handle_spin_appliance: CLIHandler
handle_spin_livecd: CLIHandler
handle_spin_livemedia: CLIHandler
handle_tag_build: CLIHandler
handle_unblock_group_pkg: CLIHandler
handle_unblock_group_req: CLIHandler
handle_unblock_notification: CLIHandler
handle_unblock_pkg: CLIHandler
handle_unlock_tag: CLIHandler
handle_untag_build: CLIHandler
handle_version: CLIHandler
handle_wait_repo_request: CLIHandler
handle_win_build: CLIHandler
handle_wrapper_rpm: CLIHandler
handle_write_signed_rpm: CLIHandler


def _print_histline(entry: HistoryEntry, **kwargs) -> None:
    ...


def print_group_list_req_group(group: str) -> None:
    ...


def print_group_list_req_package(pkg: str) -> None:
    ...


# The end.
