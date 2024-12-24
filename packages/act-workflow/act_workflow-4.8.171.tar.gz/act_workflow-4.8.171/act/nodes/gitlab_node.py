import logging
from typing import Dict, Any
import gitlab
import os

logger = logging.getLogger(__name__)

class GitLabNode:
    def __init__(self):
        logger.info("Initializing GitLabNode")
        gitlab_token = os.environ.get('GITLAB_API_TOKEN')
        gitlab_project_id = os.environ.get('GITLAB_PROJECT_ID')
        if not gitlab_token:
            raise ValueError("GITLAB_API_TOKEN environment variable not set")
        if not gitlab_project_id:
            raise ValueError("GITLAB_PROJECT_ID environment variable not set")
        self.gl = gitlab.Gitlab('https://gitlab.com', private_token=gitlab_token)
        self.project = self.gl.projects.get(gitlab_project_id)

    def execute(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        operation = node_data.get('operation')
        if operation == 'createIssue':
            return self.create_issue(node_data)
        elif operation == 'assignIssue':
            return self.assign_issue(node_data)
        elif operation == 'addLabel':
            return self.add_label(node_data)
        elif operation == 'monitorIssue':
            return self.monitor_issue(node_data)
        elif operation == 'closeIssue':
            return self.close_issue(node_data)
        elif operation == 'reopenIssue':
            return self.reopen_issue(node_data)
        else:
            raise ValueError(f"Unsupported operation: {operation}")

    def create_issue(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        title = node_data.get('title', 'New Issue')
        description = node_data.get('description', '')
        try:
            issue = self.project.issues.create({'title': title, 'description': description})
            return {"status": "success", "output": {"issue_id": issue.id}}
        except Exception as e:
            logger.error(f"GitLab API error: {e}")
            return {"status": "error", "message": str(e), "output": None}

    def assign_issue(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        issue_id = node_data.get('issue_id')
        assignee_id = node_data.get('assignee_id')
        if not issue_id or not assignee_id:
            return {"status": "error", "message": "issue_id and assignee_id are required", "output": None}
        try:
            issue = self.project.issues.get(issue_id)
            issue.assignee_ids = [assignee_id]
            issue.save()
            return {"status": "success", "message": f"Issue {issue_id} assigned to user {assignee_id}"}
        except Exception as e:
            logger.error(f"GitLab API error: {e}")
            return {"status": "error", "message": str(e), "output": None}

    def add_label(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        issue_id = node_data.get('issue_id')
        labels = node_data.get('labels', [])
        if not issue_id:
            return {"status": "error", "message": "issue_id is required", "output": None}
        try:
            issue = self.project.issues.get(issue_id)
            issue.labels = labels
            issue.save()
            return {"status": "success", "message": f"Labels {labels} added to issue {issue_id}"}
        except Exception as e:
            logger.error(f"GitLab API error: {e}")
            return {"status": "error", "message": str(e), "output": None}

    def monitor_issue(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        issue_id = node_data.get('issue_id')
        if not issue_id:
            return {"status": "error", "message": "issue_id is required", "output": None}
        try:
            issue = self.project.issues.get(issue_id)
            status = issue.state
            return {"status": "success", "output": {"status": status}}
        except Exception as e:
            logger.error(f"GitLab API error: {e}")
            return {"status": "error", "message": str(e), "output": None}

    def close_issue(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        issue_id = node_data.get('issue_id')
        if not issue_id:
            return {"status": "error", "message": "issue_id is required", "output": None}
        try:
            issue = self.project.issues.get(issue_id)
            issue.state_event = 'close'
            issue.save()
            return {"status": "success", "message": f"Issue {issue_id} closed"}
        except Exception as e:
            logger.error(f"GitLab API error: {e}")
            return {"status": "error", "message": str(e), "output": None}

    def reopen_issue(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        issue_id = node_data.get('issue_id')
        if not issue_id:
            return {"status": "error", "message": "issue_id is required", "output": None}
        try:
            issue = self.project.issues.get(issue_id)
            issue.state_event = 'reopen'
            issue.save()
            return {"status": "success", "message": f"Issue {issue_id} reopened"}
        except Exception as e:
            logger.error(f"GitLab API error: {e}")
            return {"status": "error", "message": str(e), "output": None}
