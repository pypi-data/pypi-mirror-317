import os
import json
import logging
import re
from typing import Dict, Any, List
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# WARNING: This is only for development purposes. Remove in production.
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GoogleDocsNode:
    def __init__(self, sandbox_timeout=None):
        logger.info("Initializing GoogleDocsNode")
        self.sandbox_timeout = sandbox_timeout
        self.docs_service = None
        self.drive_service = None
        self.execution_manager = None

    def set_execution_manager(self, execution_manager):
        self.execution_manager = execution_manager

    def execute(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("Starting execution of GoogleDocsNode")
        logger.info(f"Received node_data: {json.dumps(self.log_safe_node_data(node_data), indent=2)}")

        client_config = node_data.get('client_config')
        token = node_data.get('token')
        operation = node_data.get('operation')
        params = node_data.get('params', {})

        if not client_config:
            logger.error("Missing client configuration")
            return {"status": "error", "message": "Missing client configuration"}

        if not operation:
            logger.error("Missing operation")
            return {"status": "error", "message": "Missing operation"}

        try:
            # Initialize or refresh the credentials
            creds = self._get_credentials(client_config, token)
            
            # Initialize the Google Docs and Drive API services
            self.docs_service = build('docs', 'v1', credentials=creds)
            self.drive_service = build('drive', 'v3', credentials=creds)

            # Resolve any placeholders in the params
            resolved_params = self.resolve_placeholders(params, node_data)

            # Call the appropriate method
            method_name = f"_{operation}"
            method_to_call = getattr(self, method_name, None)
            if method_to_call:
                result = method_to_call(**resolved_params)
            else:
                logger.error(f"Unknown operation: {operation}")
                return {"status": "error", "message": f"Unknown operation: {operation}"}

            return {
                "status": "success",
                "result": result,
                "token": self._credentials_to_dict(creds)  # Return the updated token
            }

        except HttpError as e:
            error_msg = f"Google API error: {str(e)}"
            logger.error(error_msg)
            return {"status": "error", "message": error_msg}
        except Exception as e:
            error_msg = f"Unexpected error during execution: {str(e)}"
            logger.error(error_msg)
            return {"status": "error", "message": error_msg}

    def _get_credentials(self, client_config: Dict[str, Any], token: Dict[str, Any]) -> Credentials:
        creds = None
        if token:
            creds = Credentials.from_authorized_user_info(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = Flow.from_client_config(
                    client_config,
                    scopes=['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']
                )
                flow.redirect_uri = 'http://localhost:8080/'
                
                auth_url, _ = flow.authorization_url(prompt='consent')
                print(f'Please go to this URL to authorize the application: {auth_url}')
                
                authorization_response = input('Enter the full callback URL: ')
                
                flow.fetch_token(authorization_response=authorization_response)
                
                creds = flow.credentials

        return creds

    def _credentials_to_dict(self, credentials: Credentials) -> Dict[str, Any]:
        return {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }

    @staticmethod
    def log_safe_node_data(node_data):
        if isinstance(node_data, dict):
            safe_data = {k: ('[REDACTED]' if k in ['client_config', 'token'] else v) for k, v in node_data.items()}
        else:
            safe_data = node_data
        return safe_data

    def resolve_placeholders(self, params: Dict[str, Any], node_data: Dict[str, Any]) -> Dict[str, Any]:
        resolved_params = {}
        for key, value in params.items():
            if isinstance(value, str):
                resolved_params[key] = self.resolve_path_placeholders(value, node_data)
            else:
                resolved_params[key] = value
        return resolved_params

    def resolve_path_placeholders(self, text: str, node_data: Dict[str, Any]) -> str:
        # Handle environment variables
        env_var_pattern = re.compile(r'\$\{(.*?)\}')
        env_var_matches = env_var_pattern.findall(text)
        for match in env_var_matches:
            env_value = os.environ.get(match, '')
            text = text.replace(f"${{{match}}}", env_value)

        # Handle parameters
        param_pattern = re.compile(r'\{\{\.Parameter\.(.*?)\}\}')
        param_matches = param_pattern.findall(text)
        for match in param_matches:
            param_value = self.execution_manager.workflow_data['parameters'].get(match, '')
            text = text.replace(f"{{{{.Parameter.{match}}}}}", str(param_value))

        # Handle node results
        node_pattern = re.compile(r'\{\{(.*?)\}\}')
        node_matches = node_pattern.findall(text)
        for match in node_matches:
            parts = match.split('.')
            node_id = parts[0]
            path = '.'.join(parts[1:])
            value = self.fetch_value(node_id, path, node_data)
            if value is not None:
                text = text.replace(f"{{{{{match}}}}}", str(value))

        return text

    def fetch_value(self, node_id: str, path: str, node_data: Dict[str, Any]) -> Any:
        try:
            if self.execution_manager and node_id in self.execution_manager.node_results:
                node_result = self.execution_manager.node_results[node_id]
            else:
                node_result = node_data.get('input', {}).get('result', {})

            for part in path.split('.'):
                node_result = node_result.get(part, None)
                if node_result is None:
                    break
            return node_result
        except Exception as e:
            logger.error(f"Failed to fetch value for {node_id}.{path}: {str(e)}")
            return None

    def _create_document(self, title: str, content: str = '') -> Dict[str, Any]:
        document = self.docs_service.documents().create(body={'title': title}).execute()
        document_id = document['documentId']
        if content:
            requests = [
                {
                    'insertText': {
                        'location': {'index': 1},
                        'text': content
                    }
                }
            ]
            self.docs_service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()
        return document

    def _get_document(self, document_id: str) -> Dict[str, Any]:
        return self.docs_service.documents().get(documentId=document_id).execute()

    def _update_document(self, document_id: str, requests: List[Dict[str, Any]]) -> Dict[str, Any]:
        return self.docs_service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()

    def _delete_document(self, document_id: str) -> Dict[str, Any]:
        return self.drive_service.files().delete(fileId=document_id).execute()

    def _list_documents(self, page_size: int = 10, page_token: str = None) -> Dict[str, Any]:
        return self.drive_service.files().list(
            q="mimeType='application/vnd.google-apps.document'",
            pageSize=page_size,
            fields="nextPageToken, files(id, name)",
            pageToken=page_token
        ).execute()

    def _search_documents(self, query: str, page_size: int = 10, page_token: str = None) -> Dict[str, Any]:
        return self.drive_service.files().list(
            q=f"mimeType='application/vnd.google-apps.document' and fullText contains '{query}'",
            pageSize=page_size,
            fields="nextPageToken, files(id, name)",
            pageToken=page_token
        ).execute()

    def _get_document_content(self, document_id: str) -> str:
        document = self.docs_service.documents().get(documentId=document_id).execute()
        content = ""
        for elem in document.get('body', {}).get('content', []):
            if 'paragraph' in elem:
                for parElem in elem['paragraph'].get('elements', []):
                    if 'textRun' in parElem:
                        content += parElem['textRun'].get('content', '')
        return content

    def _insert_text(self, document_id: str, text: str, index: int) -> Dict[str, Any]:
        requests = [
            {
                'insertText': {
                    'location': {'index': index},
                    'text': text
                }
            }
        ]
        return self.docs_service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()

    def _delete_content(self, document_id: str, start_index: int, end_index: int) -> Dict[str, Any]:
        requests = [
            {
                'deleteContentRange': {
                    'range': {
                        'startIndex': start_index,
                        'endIndex': end_index
                    }
                }
            }
        ]
        return self.docs_service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()

    def _format_text(self, document_id: str, start_index: int, end_index: int, format_options: Dict[str, Any]) -> Dict[str, Any]:
        requests = [
            {
                'updateTextStyle': {
                    'range': {
                        'startIndex': start_index,
                        'endIndex': end_index
                    },
                    'textStyle': format_options,
                    'fields': ','.join(format_options.keys())
                }
            }
        ]
        return self.docs_service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()

    def _insert_image(self, document_id: str, image_url: str, index: int) -> Dict[str, Any]:
        requests = [
            {
                'insertInlineImage': {
                    'location': {'index': index},
                    'uri': image_url,
                    'objectSize': {
                        'height': {'magnitude': 100, 'unit': 'PT'},
                        'width': {'magnitude': 100, 'unit': 'PT'}
                    }
                }
            }
        ]
        return self.docs_service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()

    def _create_table(self, document_id: str, index: int, rows: int, columns: int) -> Dict[str, Any]:
        requests = [
            {
                'insertTable': {
                    'location': {'index': index},
                    'rows': rows,
                    'columns': columns
                }
            }
        ]
        return self.docs_service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()

GoogleDocsNodeNode = GoogleDocsNode

def main():
    print("IMPORTANT: Make sure you have enabled both the Google Docs API and Google Drive API for your project.")
    print("Visit https://console.developers.google.com/apis/library and enable both APIs.")
    print("Wait a few minutes for the changes to propagate before running this script.")
    input("Press Enter to continue...")

    # Load client configuration from a JSON file
    client_config_path = '/Users/taj/Desktop/ll/mvp2/lib/python3.10/site-packages/act/nodes/client_secret_239221702034-v5tec3pmo2uhpdjbtlpvsqm3p166o7m7.apps.googleusercontent.com.json'
    if not os.path.exists(client_config_path):
        print(f"Error: Client configuration file not found at {client_config_path}")
        return

    with open(client_config_path, 'r') as f:
        client_config = json.load(f)

    # Check if we have a stored token
    token_path = '/Users/taj/Desktop/ll/mvp2/lib/python3.10/site-packages/act/nodes/token.json'
    token = None
    if os.path.exists(token_path):
        with open(token_path, 'r') as f:
            token = json.load(f)

    # Example operations
    operations = [
        {
            "operation": "create_document",
            "params": {
                "title": "Test Document",
                "content": "This is a test document created by GoogleDocsNode."
            }
        },
        {
            "operation": "list_documents",
            "params": {
                "page_size": 5
            }
        },
        {
            "operation": "search_documents",
            "params": {
                "query": "test",
                "page_size": 5
            }
        }
    ]

    node = GoogleDocsNode()

    for op in operations:
        test_data = {
            "client_config": client_config,
            "token": token,
            "operation": op["operation"],
            "params": op["params"]
        }

        print(f"\nExecuting operation: {op['operation']}")
        result = node.execute(test_data)

        if result['status'] == 'success':
            print("Operation completed successfully!")
            print(json.dumps(result['result'], indent=2))
            
            # Update the token after each successful operation
            token = result['token']
            with open(token_path, 'w') as f:
                json.dump(token, f)
        else:
            print("Error occurred:")
            print(result['message'])

if __name__ == "__main__":
    main()
