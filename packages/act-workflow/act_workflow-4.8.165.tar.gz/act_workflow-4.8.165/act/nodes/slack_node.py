import os
import json
import logging
from typing import Dict, Any, List
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SlackNode:
    def __init__(self, sandbox_timeout=None):
        logger.info("Initializing SlackNode")
        self.sandbox_timeout = sandbox_timeout

        self.client = None

    def extract_text(self, input_text: str) -> str:
        try:
            parsed = json.loads(input_text)
            if isinstance(parsed, dict):
                return str(parsed.get('value', input_text))
            elif isinstance(parsed, str):
                return parsed
        except json.JSONDecodeError:
            pass
        return input_text

    def resolve_path_placeholders(self, text: str, node_data: Dict[str, Any]) -> str:
        pattern = re.compile(r"\{\{(.*?)\}\}")
        matches = pattern.findall(text)
        
        for match in matches:
            parts = match.split('.')
            node_id = parts[0]
            path = '.'.join(parts[1:])
            value = self.fetch_value(node_id, path, node_data)
            if value is not None:
                text = text.replace(f"{{{{{match}}}}}", str(value))
        
        return text

    def fetch_value(self, node_id: str, path: str, node_data: Dict[str, Any]) -> Any:
        try:
            node_result = node_data.get('input', {}).get('result', {})
            for part in path.split('.'):
                node_result = node_result.get(part, None)
                if node_result is None:
                    break
            return node_result
        except Exception as e:
            logger.error(f"Failed to fetch value for {node_id}.{path}: {str(e)}")
            return None

    def execute(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("Starting execution of SlackNode")
        logger.info(f"Received node_data: {json.dumps(self.log_safe_node_data(node_data), indent=2)}")
        
        slack_token = node_data.get('slack_token')
        method = node_data.get('method')
        params = node_data.get('params', {})

        if not slack_token:
            logger.error("Missing Slack token")
            return {"status": "error", "message": "Missing Slack token"}

        if not method:
            logger.error("Missing method")
            return {"status": "error", "message": "Missing method"}

        try:
            self.client = WebClient(token=slack_token)
            
            # Resolve any placeholders in the params
            resolved_params = {k: self.resolve_path_placeholders(str(v), node_data) for k, v in params.items()}
            
            # Call the appropriate method
            method_to_call = getattr(self.client, method, None)
            if method_to_call:
                response = method_to_call(**resolved_params)
                result = self.serialize_slack_response(response)
            else:
                logger.error(f"Unknown method: {method}")
                return {"status": "error", "message": f"Unknown method: {method}"}

            return {
                "status": "success",
                "result": result
            }

        except SlackApiError as e:
            error_msg = f"Slack API error: {e.response['error']}"
            logger.error(error_msg)
            return {"status": "error", "message": error_msg}
        except Exception as e:
            error_msg = f"Unexpected error during execution: {str(e)}"
            logger.error(error_msg)
            return {"status": "error", "message": error_msg}

    def serialize_slack_response(self, response) -> Dict[str, Any]:
        """
        Serialize the SlackResponse object into a dictionary.
        """
        return {
            "ok": response.get("ok", False),
            "channel": response.get("channel"),
            "ts": response.get("ts"),
            "message": response.get("message", {})
        }
    
    @staticmethod
    def log_safe_node_data(node_data):
        if isinstance(node_data, dict):
            safe_data = {k: ('[REDACTED]' if k == 'slack_token' else v) for k, v in node_data.items()}
        else:
            safe_data = node_data
        return safe_data



    # Web API Methods
    def admin_analytics_getFile(self, **kwargs):
        return self.client.admin_analytics_getFile(**kwargs)

    def admin_apps_activities_list(self, **kwargs):
        return self.client.admin_apps_activities_list(**kwargs)

    def admin_apps_approve(self, **kwargs):
        return self.client.admin_apps_approve(**kwargs)

    def admin_apps_approved_list(self, **kwargs):
        return self.client.admin_apps_approved_list(**kwargs)

    def admin_apps_clearResolution(self, **kwargs):
        return self.client.admin_apps_clearResolution(**kwargs)

    def admin_apps_config_lookup(self, **kwargs):
        return self.client.admin_apps_config_lookup(**kwargs)

    def admin_apps_config_set(self, **kwargs):
        return self.client.admin_apps_config_set(**kwargs)

    def admin_apps_requests_list(self, **kwargs):
        return self.client.admin_apps_requests_list(**kwargs)

    def admin_apps_requests_cancel(self, **kwargs):
        return self.client.admin_apps_requests_cancel(**kwargs)

    def admin_apps_restrict(self, **kwargs):
        return self.client.admin_apps_restrict(**kwargs)

    def admin_apps_restricted_list(self, **kwargs):
        return self.client.admin_apps_restricted_list(**kwargs)

    def admin_apps_uninstall(self, **kwargs):
        return self.client.admin_apps_uninstall(**kwargs)

    def admin_audit_anomaly_allow_list(self, **kwargs):
        return self.client.admin_audit_anomaly_allow_list(**kwargs)

    def admin_auth_policy_assignEntities(self, **kwargs):
        return self.client.admin_auth_policy_assignEntities(**kwargs)

    def admin_auth_policy_getEntities(self, **kwargs):
        return self.client.admin_auth_policy_getEntities(**kwargs)

    def admin_auth_policy_removeEntities(self, **kwargs):
        return self.client.admin_auth_policy_removeEntities(**kwargs)

    def admin_barriers_create(self, **kwargs):
        return self.client.admin_barriers_create(**kwargs)

    def admin_barriers_delete(self, **kwargs):
        return self.client.admin_barriers_delete(**kwargs)

    def admin_barriers_list(self, **kwargs):
        return self.client.admin_barriers_list(**kwargs)

    def admin_barriers_update(self, **kwargs):
        return self.client.admin_barriers_update(**kwargs)

    def admin_conversations_archive(self, **kwargs):
        return self.client.admin_conversations_archive(**kwargs)

    def admin_conversations_convertToPrivate(self, **kwargs):
        return self.client.admin_conversations_convertToPrivate(**kwargs)

    def admin_conversations_create(self, **kwargs):
        return self.client.admin_conversations_create(**kwargs)

    def admin_conversations_delete(self, **kwargs):
        return self.client.admin_conversations_delete(**kwargs)

    def admin_conversations_disconnectShared(self, **kwargs):
        return self.client.admin_conversations_disconnectShared(**kwargs)

    def admin_conversations_ekm_listOriginalConnectedChannelInfo(self, **kwargs):
        return self.client.admin_conversations_ekm_listOriginalConnectedChannelInfo(**kwargs)

    def admin_conversations_getConversationPrefs(self, **kwargs):
        return self.client.admin_conversations_getConversationPrefs(**kwargs)

    def admin_conversations_getTeams(self, **kwargs):
        return self.client.admin_conversations_getTeams(**kwargs)

    def admin_conversations_invite(self, **kwargs):
        return self.client.admin_conversations_invite(**kwargs)

    def admin_conversations_rename(self, **kwargs):
        return self.client.admin_conversations_rename(**kwargs)

    def admin_conversations_restrictAccess_addGroup(self, **kwargs):
        return self.client.admin_conversations_restrictAccess_addGroup(**kwargs)

    def admin_conversations_restrictAccess_listGroups(self, **kwargs):
        return self.client.admin_conversations_restrictAccess_listGroups(**kwargs)

    def admin_conversations_restrictAccess_removeGroup(self, **kwargs):
        return self.client.admin_conversations_restrictAccess_removeGroup(**kwargs)

    def admin_conversations_search(self, **kwargs):
        return self.client.admin_conversations_search(**kwargs)

    def admin_conversations_setConversationPrefs(self, **kwargs):
        return self.client.admin_conversations_setConversationPrefs(**kwargs)

    def admin_conversations_setTeams(self, **kwargs):
        return self.client.admin_conversations_setTeams(**kwargs)

    def admin_conversations_unarchive(self, **kwargs):
        return self.client.admin_conversations_unarchive(**kwargs)

    def admin_emoji_add(self, **kwargs):
        return self.client.admin_emoji_add(**kwargs)

    def admin_emoji_addAlias(self, **kwargs):
        return self.client.admin_emoji_addAlias(**kwargs)

    def admin_emoji_list(self, **kwargs):
        return self.client.admin_emoji_list(**kwargs)

    def admin_emoji_remove(self, **kwargs):
        return self.client.admin_emoji_remove(**kwargs)

    def admin_emoji_rename(self, **kwargs):
        return self.client.admin_emoji_rename(**kwargs)

    def admin_functions_list(self, **kwargs):
        return self.client.admin_functions_list(**kwargs)

    def admin_functions_permissions_lookup(self, **kwargs):
        return self.client.admin_functions_permissions_lookup(**kwargs)

    def admin_functions_permissions_set(self, **kwargs):
        return self.client.admin_functions_permissions_set(**kwargs)

    def admin_inviteRequests_approve(self, **kwargs):
        return self.client.admin_inviteRequests_approve(**kwargs)

    def admin_inviteRequests_approved_list(self, **kwargs):
        return self.client.admin_inviteRequests_approved_list(**kwargs)

    def admin_inviteRequests_denied_list(self, **kwargs):
        return self.client.admin_inviteRequests_denied_list(**kwargs)

    def admin_inviteRequests_deny(self, **kwargs):
        return self.client.admin_inviteRequests_deny(**kwargs)

    def admin_inviteRequests_list(self, **kwargs):
        return self.client.admin_inviteRequests_list(**kwargs)

    def admin_roles_addAssignments(self, **kwargs):
        return self.client.admin_roles_addAssignments(**kwargs)

    def admin_roles_listAssignments(self, **kwargs):
        return self.client.admin_roles_listAssignments(**kwargs)

    def admin_roles_removeAssignments(self, **kwargs):
        return self.client.admin_roles_removeAssignments(**kwargs)

    def admin_teams_admins_list(self, **kwargs):
        return self.client.admin_teams_admins_list(**kwargs)

    def admin_teams_create(self, **kwargs):
        return self.client.admin_teams_create(**kwargs)

    def admin_teams_list(self, **kwargs):
        return self.client.admin_teams_list(**kwargs)

    def admin_teams_owners_list(self, **kwargs):
        return self.client.admin_teams_owners_list(**kwargs)

    def admin_teams_settings_info(self, **kwargs):
        return self.client.admin_teams_settings_info(**kwargs)

    def admin_teams_settings_setDefaultChannels(self, **kwargs):
        return self.client.admin_teams_settings_setDefaultChannels(**kwargs)

    def admin_teams_settings_setDescription(self, **kwargs):
        return self.client.admin_teams_settings_setDescription(**kwargs)

    def admin_teams_settings_setDiscoverability(self, **kwargs):
        return self.client.admin_teams_settings_setDiscoverability(**kwargs)

    def admin_teams_settings_setIcon(self, **kwargs):
        return self.client.admin_teams_settings_setIcon(**kwargs)

    def admin_teams_settings_setName(self, **kwargs):
        return self.client.admin_teams_settings_setName(**kwargs)

    def admin_usergroups_addChannels(self, **kwargs):
        return self.client.admin_usergroups_addChannels(**kwargs)

    def admin_usergroups_addTeams(self, **kwargs):
        return self.client.admin_usergroups_addTeams(**kwargs)

    def admin_usergroups_listChannels(self, **kwargs):
        return self.client.admin_usergroups_listChannels(**kwargs)

    def admin_usergroups_removeChannels(self, **kwargs):
        return self.client.admin_usergroups_removeChannels(**kwargs)

    def admin_users_assign(self, **kwargs):
        return self.client.admin_users_assign(**kwargs)

    def admin_users_invite(self, **kwargs):
        return self.client.admin_users_invite(**kwargs)

    def admin_users_list(self, **kwargs):
        return self.client.admin_users_list(**kwargs)

    def admin_users_remove(self, **kwargs):
        return self.client.admin_users_remove(**kwargs)

    def admin_users_setAdmin(self, **kwargs):
        return self.client.admin_users_setAdmin(**kwargs)

    def admin_users_setExpiration(self, **kwargs):
        return self.client.admin_users_setExpiration(**kwargs)

    def admin_users_setOwner(self, **kwargs):
        return self.client.admin_users_setOwner(**kwargs)

    def admin_users_setRegular(self, **kwargs):
        return self.client.admin_users_setRegular(**kwargs)

    def admin_users_session_invalidate(self, **kwargs):
        return self.client.admin_users_session_invalidate(**kwargs)

    def admin_users_session_list(self, **kwargs):
        return self.client.admin_users_session_list(**kwargs)

    def admin_users_session_reset(self, **kwargs):
        return self.client.admin_users_session_reset(**kwargs)

    def admin_users_session_resetBulk(self, **kwargs):
        return self.client.admin_users_session_resetBulk(**kwargs)

    def admin_users_unsupportedVersions_export(self, **kwargs):
        return self.client.admin_users_unsupportedVersions_export(**kwargs)

    def admin_workflows_collaborators_add(self, **kwargs):
        return self.client.admin_workflows_collaborators_add(**kwargs)

    def admin_workflows_collaborators_remove(self, **kwargs):
        return self.client.admin_workflows_collaborators_remove(**kwargs)

    def admin_workflows_permissions_lookup(self, **kwargs):
        return self.client.admin_workflows_permissions_lookup(**kwargs)

    def admin_workflows_search(self, **kwargs):
        return self.client.admin_workflows_search(**kwargs)

    def admin_workflows_triggers_types_permissions_list(self, **kwargs):
        return self.client.admin_workflows_triggers_types_permissions_list(**kwargs)

    def admin_workflows_unpublish(self, **kwargs):
        return self.client.admin_workflows_unpublish(**kwargs)

    def api_test(self, **kwargs):
        return self.client.api_test(**kwargs)

    def apps_activities_list(self, **kwargs):
        return self.client.apps_activities_list(**kwargs)

    def apps_auth_external_create(self, **kwargs):
        return self.client.apps_auth_external_create(**kwargs)

    def apps_auth_external_delete(self, **kwargs):
        return self.client.apps_auth_external_delete(**kwargs)

    def apps_connections_open(self, **kwargs):
        return self.client.apps_connections_open(**kwargs)

    def apps_datastore_delete(self, **kwargs):
        return self.client.apps_datastore_delete(**kwargs)

    def apps_datastore_get(self, **kwargs):
        return self.client.apps_datastore_get(**kwargs)

    def apps_datastore_put(self, **kwargs):
        return self.client.apps_datastore_put(**kwargs)

    def apps_datastore_query(self, **kwargs):
        return self.client.apps_datastore_query(**kwargs)

    def apps_datastore_update(self, **kwargs):
        return self.client.apps_datastore_update(**kwargs)

    def apps_event_authorizations_list(self, **kwargs):
        return self.client.apps_event_authorizations_list(**kwargs)

    def apps_manifest_create(self, **kwargs):
        return self.client.apps_manifest_create(**kwargs)

    def apps_manifest_delete(self, **kwargs):
        return self.client.apps_manifest_delete(**kwargs)

    def apps_manifest_export(self, **kwargs):
        return self.client.apps_manifest_export(**kwargs)

    def apps_manifest_update(self, **kwargs):
        return self.client.apps_manifest_update(**kwargs)

    def apps_manifest_validate(self, **kwargs):
        return self.client.apps_manifest_validate(**kwargs)

    def apps_uninstall(self, **kwargs):
        return self.client.apps_uninstall(**kwargs)

    def assistant_threads_ask(self, **kwargs):
        return self.client.assistant_threads_ask(**kwargs)

    def auth_revoke(self, **kwargs):
        return self.client.auth_revoke(**kwargs)

    def auth_test(self, **kwargs):
        return self.client.auth_test(**kwargs)

    def auth_teams_list(self, **kwargs):
        return self.client.auth_teams_list(**kwargs)

    def bookmarks_add(self, **kwargs):
        return self.client.bookmarks_add(**kwargs)

    def bookmarks_edit(self, **kwargs):
        return self.client.bookmarks_edit(**kwargs)

    def bookmarks_list(self, **kwargs):
        return self.client.bookmarks_list(**kwargs)

    def bookmarks_remove(self, **kwargs):
        return self.client.bookmarks_remove(**kwargs)

    def bots_info(self, **kwargs):
        return self.client.bots_info(**kwargs)

    def calls_add(self, **kwargs):
        return self.client.calls_add(**kwargs)

    def calls_end(self, **kwargs):
        return self.client.calls_end(**kwargs)

    def calls_info(self, **kwargs):
        return self.client.calls_info(**kwargs)

    def calls_participants_add(self, **kwargs):
        return self.client.calls_participants_add(**kwargs)

    def calls_participants_remove(self, **kwargs):
        return self.client.calls_participants_remove(**kwargs)

    def calls_update(self, **kwargs):
        return self.client.calls_update(**kwargs)

    def canvases_access_add(self, **kwargs):
        return self.client.canvases_access_add(**kwargs)

    def canvases_access_remove(self, **kwargs):
        return self.client.canvases_access_remove(**kwargs)

    def canvases_create(self, **kwargs):
        return self.client.canvases_create(**kwargs)

    def canvases_duplicate(self, **kwargs):
        return self.client.canvases_duplicate(**kwargs)

    def canvases_get(self, **kwargs):
        return self.client.canvases_get(**kwargs)

    def canvases_list(self, **kwargs):
        return self.client.canvases_list(**kwargs)

    def canvases_rename(self, **kwargs):
        return self.client.canvases_rename(**kwargs)

    def canvases_sections_add(self, **kwargs):
        return self.client.canvases_sections_add(**kwargs)

    def canvases_sections_get(self, **kwargs):
        return self.client.canvases_sections_get(**kwargs)

    def canvases_sections_list(self, **kwargs):
        return self.client.canvases_sections_list(**kwargs)

    def canvases_sections_remove(self, **kwargs):
        return self.client.canvases_sections_remove(**kwargs)

    def canvases_sections_rename(self, **kwargs):
        return self.client.canvases_sections_rename(**kwargs)

    def channels_archive(self, **kwargs):
        return self.client.channels_archive(**kwargs)

    def channels_create(self, **kwargs):
        return self.client.channels_create(**kwargs)

    def channels_history(self, **kwargs):
        return self.client.channels_history(**kwargs)

    def channels_info(self, **kwargs):
        return self.client.channels_info(**kwargs)

    def channels_invite(self, **kwargs):
        return self.client.channels_invite(**kwargs)

    def channels_join(self, **kwargs):
        return self.client.channels_join(**kwargs)

    def channels_kick(self, **kwargs):
        return self.client.channels_kick(**kwargs)

    def channels_leave(self, **kwargs):
        return self.client.channels_leave(**kwargs)

    def channels_list(self, **kwargs):
        return self.client.channels_list(**kwargs)

    def channels_mark(self, **kwargs):
        return self.client.channels_mark(**kwargs)

    def channels_rename(self, **kwargs):
        return self.client.channels_rename(**kwargs)

    def channels_replies(self, **kwargs):
        return self.client.channels_replies(**kwargs)

    def channels_setPurpose(self, **kwargs):
        return self.client.channels_setPurpose(**kwargs)

    def channels_setTopic(self, **kwargs):
        return self.client.channels_setTopic(**kwargs)

    def channels_unarchive(self, **kwargs):
        return self.client.channels_unarchive(**kwargs)

    def chat_delete(self, **kwargs):
        return self.client.chat_delete(**kwargs)

    def chat_deleteScheduledMessage(self, **kwargs):
        return self.client.chat_deleteScheduledMessage(**kwargs)

    def chat_getPermalink(self, **kwargs):
        return self.client.chat_getPermalink(**kwargs)

    def chat_meMessage(self, **kwargs):
        return self.client.chat_meMessage(**kwargs)

    def chat_postEphemeral(self, **kwargs):
        return self.client.chat_postEphemeral(**kwargs)

    def chat_postMessage(self, **kwargs):
        return self.client.chat_postMessage(**kwargs)

    def chat_scheduleMessage(self, **kwargs):
        return self.client.chat_scheduleMessage(**kwargs)

    def chat_scheduledMessages_list(self, **kwargs):
        return self.client.chat_scheduledMessages_list(**kwargs)

    def chat_unfurl(self, **kwargs):
        return self.client.chat_unfurl(**kwargs)

    def chat_update(self, **kwargs):
        return self.client.chat_update(**kwargs)

    def conversations_archive(self, **kwargs):
        return self.client.conversations_archive(**kwargs)

    def conversations_close(self, **kwargs):
        return self.client.conversations_close(**kwargs)

    def conversations_create(self, **kwargs):
        return self.client.conversations_create(**kwargs)

    def conversations_history(self, **kwargs):
        return self.client.conversations_history(**kwargs)

    def conversations_info(self, **kwargs):
        return self.client.conversations_info(**kwargs)

    def conversations_invite(self, **kwargs):
        return self.client.conversations_invite(**kwargs)

    def conversations_join(self, **kwargs):
        return self.client.conversations_join(**kwargs)

    def conversations_kick(self, **kwargs):
        return self.client.conversations_kick(**kwargs)

    def conversations_leave(self, **kwargs):
        return self.client.conversations_leave(**kwargs)

    def conversations_list(self, **kwargs):
        return self.client.conversations_list(**kwargs)

    def conversations_mark(self, **kwargs):
        return self.client.conversations_mark(**kwargs)

    def conversations_members(self, **kwargs):
        return self.client.conversations_members(**kwargs)

    def conversations_open(self, **kwargs):
        return self.client.conversations_open(**kwargs)

    def conversations_rename(self, **kwargs):
        return self.client.conversations_rename(**kwargs)

    def conversations_replies(self, **kwargs):
        return self.client.conversations_replies(**kwargs)

    def conversations_setPurpose(self, **kwargs):
        return self.client.conversations_setPurpose(**kwargs)

    def conversations_setTopic(self, **kwargs):
        return self.client.conversations_setTopic(**kwargs)

    def conversations_unarchive(self, **kwargs):
        return self.client.conversations_unarchive(**kwargs)

    def dialog_open(self, **kwargs):
        return self.client.dialog_open(**kwargs)

    def dnd_endDnd(self, **kwargs):
        return self.client.dnd_endDnd(**kwargs)

    def dnd_endSnooze(self, **kwargs):
        return self.client.dnd_endSnooze(**kwargs)

    def dnd_info(self, **kwargs):
        return self.client.dnd_info(**kwargs)

    def dnd_setSnooze(self, **kwargs):
        return self.client.dnd_setSnooze(**kwargs)

    def dnd_teamInfo(self, **kwargs):
        return self.client.dnd_teamInfo(**kwargs)

    def emoji_list(self, **kwargs):
        return self.client.emoji_list(**kwargs)

    def files_comments_delete(self, **kwargs):
        return self.client.files_comments_delete(**kwargs)

    def files_delete(self, **kwargs):
        return self.client.files_delete(**kwargs)

    def files_info(self, **kwargs):
        return self.client.files_info(**kwargs)

    def files_list(self, **kwargs):
        return self.client.files_list(**kwargs)

    def files_remote_add(self, **kwargs):
        return self.client.files_remote_add(**kwargs)

    def files_remote_info(self, **kwargs):
        return self.client.files_remote_info(**kwargs)

    def files_remote_list(self, **kwargs):
        return self.client.files_remote_list(**kwargs)

    def files_remote_remove(self, **kwargs):
        return self.client.files_remote_remove(**kwargs)

    def files_remote_share(self, **kwargs):
        return self.client.files_remote_share(**kwargs)

    def files_remote_update(self, **kwargs):
        return self.client.files_remote_update(**kwargs)

    def files_revokePublicURL(self, **kwargs):
        return self.client.files_revokePublicURL(**kwargs)

    def files_sharedPublicURL(self, **kwargs):
        return self.client.files_sharedPublicURL(**kwargs)

    def files_upload(self, **kwargs):
        return self.client.files_upload(**kwargs)

    def functions_workflows_steps_list(self, **kwargs):
        return self.client.functions_workflows_steps_list(**kwargs)

    def functions_workflows_steps_update(self, **kwargs):
        return self.client.functions_workflows_steps_update(**kwargs)

    def groups_archive(self, **kwargs):
        return self.client.groups_archive(**kwargs)

    def groups_create(self, **kwargs):
        return self.client.groups_create(**kwargs)

    def groups_createChild(self, **kwargs):
        return self.client.groups_createChild(**kwargs)

    def groups_history(self, **kwargs):
        return self.client.groups_history(**kwargs)

    def groups_info(self, **kwargs):
        return self.client.groups_info(**kwargs)

    def groups_invite(self, **kwargs):
        return self.client.groups_invite(**kwargs)

    def groups_kick(self, **kwargs):
        return self.client.groups_kick(**kwargs)

    def groups_leave(self, **kwargs):
        return self.client.groups_leave(**kwargs)

    def groups_list(self, **kwargs):
        return self.client.groups_list(**kwargs)

    def groups_mark(self, **kwargs):
        return self.client.groups_mark(**kwargs)

    def groups_open(self, **kwargs):
        return self.client.groups_open(**kwargs)

    def groups_rename(self, **kwargs):
        return self.client.groups_rename(**kwargs)

    def groups_replies(self, **kwargs):
        return self.client.groups_replies(**kwargs)

    def groups_setPurpose(self, **kwargs):
        return self.client.groups_setPurpose(**kwargs)

    def groups_setTopic(self, **kwargs):
        return self.client.groups_setTopic(**kwargs)

    def groups_unarchive(self, **kwargs):
        return self.client.groups_unarchive(**kwargs)

    def im_close(self, **kwargs):
        return self.client.im_close(**kwargs)

    def im_history(self, **kwargs):
        return self.client.im_history(**kwargs)

    def im_list(self, **kwargs):
        return self.client.im_list(**kwargs)

    def im_mark(self, **kwargs):
        return self.client.im_mark(**kwargs)

    def im_open(self, **kwargs):
        return self.client.im_open(**kwargs)

    def im_replies(self, **kwargs):
        return self.client.im_replies(**kwargs)

    def migration_exchange(self, **kwargs):
        return self.client.migration_exchange(**kwargs)

    def mpim_close(self, **kwargs):
        return self.client.mpim_close(**kwargs)

    def mpim_history(self, **kwargs):
        return self.client.mpim_history(**kwargs)

    def mpim_list(self, **kwargs):
        return self.client.mpim_list(**kwargs)

    def mpim_mark(self, **kwargs):
        return self.client.mpim_mark(**kwargs)

    def mpim_open(self, **kwargs):
        return self.client.mpim_open(**kwargs)

    def mpim_replies(self, **kwargs):
        return self.client.mpim_replies(**kwargs)

    def oauth_access(self, **kwargs):
        return self.client.oauth_access(**kwargs)

    def oauth_v2_access(self, **kwargs):
        return self.client.oauth_v2_access(**kwargs)

    def openid_connect_token(self, **kwargs):
        return self.client.openid_connect_token(**kwargs)

    def openid_connect_userInfo(self, **kwargs):
        return self.client.openid_connect_userInfo(**kwargs)

    def pins_add(self, **kwargs):
        return self.client.pins_add(**kwargs)

    def pins_list(self, **kwargs):
        return self.client.pins_list(**kwargs)

    def pins_remove(self, **kwargs):
        return self.client.pins_remove(**kwargs)

    def reactions_add(self, **kwargs):
        return self.client.reactions_add(**kwargs)

    def reactions_get(self, **kwargs):
        return self.client.reactions_get(**kwargs)

    def reactions_list(self, **kwargs):
        return self.client.reactions_list(**kwargs)

    def reactions_remove(self, **kwargs):
        return self.client.reactions_remove(**kwargs)

    def reminders_add(self, **kwargs):
        return self.client.reminders_add(**kwargs)

    def reminders_complete(self, **kwargs):
        return self.client.reminders_complete(**kwargs)

    def reminders_delete(self, **kwargs):
        return self.client.reminders_delete(**kwargs)

    def reminders_info(self, **kwargs):
        return self.client.reminders_info(**kwargs)

    def reminders_list(self, **kwargs):
        return self.client.reminders_list(**kwargs)

    def rtm_connect(self, **kwargs):
        return self.client.rtm_connect(**kwargs)

    def rtm_start(self, **kwargs):
        return self.client.rtm_start(**kwargs)

    def search_all(self, **kwargs):
        return self.client.search_all(**kwargs)

    def search_files(self, **kwargs):
        return self.client.search_files(**kwargs)

    def search_messages(self, **kwargs):
        return self.client.search_messages(**kwargs)

    def stars_add(self, **kwargs):
        return self.client.stars_add(**kwargs)

    def stars_list(self, **kwargs):
        return self.client.stars_list(**kwargs)

    def stars_remove(self, **kwargs):
        return self.client.stars_remove(**kwargs)

    def team_accessLogs(self, **kwargs):
        return self.client.team_accessLogs(**kwargs)

    def team_billableInfo(self, **kwargs):
        return self.client.team_billableInfo(**kwargs)

    def team_info(self, **kwargs):
        return self.client.team_info(**kwargs)

    def team_integrationLogs(self, **kwargs):
        return self.client.team_integrationLogs(**kwargs)

    def team_profile_get(self, **kwargs):
        return self.client.team_profile_get(**kwargs)

    def tooling_tokens_rotate(self, **kwargs):
        return self.client.tooling_tokens_rotate(**kwargs)

    def usergroups_create(self, **kwargs):
        return self.client.usergroups_create(**kwargs)

    def usergroups_disable(self, **kwargs):
        return self.client.usergroups_disable(**kwargs)

    def usergroups_enable(self, **kwargs):
        return self.client.usergroups_enable(**kwargs)

    def usergroups_list(self, **kwargs):
        return self.client.usergroups_list(**kwargs)

    def usergroups_update(self, **kwargs):
        return self.client.usergroups_update(**kwargs)

    def usergroups_users_list(self, **kwargs):
        return self.client.usergroups_users_list(**kwargs)

    def usergroups_users_update(self, **kwargs):
        return self.client.usergroups_users_update(**kwargs)

    def users_conversations(self, **kwargs):
        return self.client.users_conversations(**kwargs)

    def users_deletePhoto(self, **kwargs):
        return self.client.users_deletePhoto(**kwargs)

    def users_getPresence(self, **kwargs):
        return self.client.users_getPresence(**kwargs)

    def users_identity(self, **kwargs):
        return self.client.users_identity(**kwargs)

    def users_info(self, **kwargs):
        return self.client.users_info(**kwargs)

    def users_list(self, **kwargs):
        return self.client.users_list(**kwargs)

    def users_lookupByEmail(self, **kwargs):
        return self.client.users_lookupByEmail(**kwargs)

    def users_profile_get(self, **kwargs):
        return self.client.users_profile_get(**kwargs)

    def users_profile_set(self, **kwargs):
        return self.client.users_profile_set(**kwargs)

    def users_setActive(self, **kwargs):
        return self.client.users_setActive(**kwargs)

    def users_setPhoto(self, **kwargs):
        return self.client.users_setPhoto(**kwargs)

    def users_setPresence(self, **kwargs):
        return self.client.users_setPresence(**kwargs)

    def views_open(self, **kwargs):
        return self.client.views_open(**kwargs)

    def views_publish(self, **kwargs):
        return self.client.views_publish(**kwargs)

    def views_push(self, **kwargs):
        return self.client.views_push(**kwargs)

    def views_update(self, **kwargs):
        return self.client.views_update(**kwargs)

    def workflows_stepCompleted(self, **kwargs):
        return self.client.workflows_stepCompleted(**kwargs)

    def workflows_stepFailed(self, **kwargs):
        return self.client.workflows_stepFailed(**kwargs)

    def workflows_updateStep(self, **kwargs):
        return self.client.workflows_updateStep(**kwargs)


SlackNodeNode = SlackNode

if __name__ == "__main__":
    test_data = {
        "slack_token": os.environ.get("SLACK_TOKEN"),
        "method": "chat_postMessage",
        "params": {
            "channel": "#general",
            "text": "Hello from SlackNode!"
        }
    }

    node = SlackNode()
    result = node.execute(test_data)
    print(json.dumps(result, indent=2))