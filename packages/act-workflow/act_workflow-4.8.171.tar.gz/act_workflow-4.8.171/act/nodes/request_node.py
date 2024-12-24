import os
import json
import logging
from typing import Dict, Any, Union
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RequestNode:
    def __init__(self):
        logger.info("Initializing RequestNode")
        self.session = requests.Session()
        retry = Retry(total=3, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
        self.session.mount('http://', HTTPAdapter(max_retries=retry))
        self.session.mount('https://', HTTPAdapter(max_retries=retry))

    def execute(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("Starting execution of RequestNode")
        logger.debug(f"Received node_data: {json.dumps(self.log_safe_node_data(node_data), indent=2)}")

        url = node_data.get('url', '').strip()
        method = node_data.get('method', 'GET').upper()
        headers = {'Content-Type': 'application/json'}
        auth_type = node_data.get('auth_type', 'none')
        auth_value = node_data.get('auth_value', '')
        parameters = node_data.get('parameters', {})
        body = node_data.get('body', {})
        timeout = node_data.get('timeout', 30)
        verify_ssl = node_data.get('verify_ssl', True)
        max_response_size = node_data.get('max_response_size', 10 * 1024 * 1024)  # 10 MB default

        if not url:
            logger.error("URL not provided in node data")
            return {"status": "error", "message": "URL not provided", "output": None}

        try:
            # Parse body if it's a string
            if isinstance(body, str):
                try:
                    body = json.loads(body)
                except json.JSONDecodeError:
                    logger.error("Failed to parse body as JSON")
                    return {"status": "error", "message": "Invalid JSON in body", "output": None}

            # Set authentication header
            if auth_type == 'api_key':
                headers['Authorization'] = auth_value

            # Make the request
            result = self.make_request(url, method, headers, parameters, body, timeout, verify_ssl, max_response_size)
            logger.info("Request completed successfully")
            return {
                "status": "success",
                "output": result
            }
        except Exception as e:
            logger.error(f"Error in making request: {str(e)}")
            return {"status": "error", "message": str(e), "output": None}

    def make_request(self, url: str, method: str, headers: Dict[str, str], 
                     parameters: Dict[str, Any], body: Dict[str, Any], 
                     timeout: int, verify_ssl: bool, max_response_size: int) -> Dict[str, Any]:
        logger.info(f"Making {method} request to {url}")
        
        try:
            # Prepare the request
            request_kwargs = {
                "method": method,
                "url": url,
                "headers": headers,
                "params": parameters,
                "timeout": timeout,
                "verify": verify_ssl
            }

            # Add body for POST, PUT, PATCH
            if method in ['POST', 'PUT', 'PATCH']:
                request_kwargs["json"] = body

            # Make the request
            with self.session.request(**request_kwargs) as response:
                response.raise_for_status()

                # Check response size
                if int(response.headers.get('Content-Length', 0)) > max_response_size:
                    raise ValueError(f"Response size exceeds maximum allowed size of {max_response_size} bytes")

                try:
                    result = response.json()
                except json.JSONDecodeError:
                    result = response.text

                return {
                    "status_code": response.status_code,
                    "headers": dict(response.headers),
                    "body": result,
                    "url": response.url
                }

        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            raise

    @staticmethod
    def log_safe_node_data(node_data):
        if isinstance(node_data, dict):
            safe_data = {k: ('[REDACTED]' if k in ['auth_value', 'api_key'] else v) for k, v in node_data.items()}
        else:
            safe_data = node_data
        return safe_data

# This part is for testing the RequestNode independently
if __name__ == "__main__":
    # Make the specific API request
    node_data = {
        "url": "https://dobee-dev.ew.r.appspot.com/objectives/mi331cCJ0abn19PD1HkX/keyResults",
        "method": "GET",
        "auth_type": "api_key",
        "auth_value": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjcxOGY0ZGY5MmFkMTc1ZjZhMDMwN2FiNjVkOGY2N2YwNTRmYTFlNWYiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZG9iZWUtZGV2IiwiYXVkIjoiZG9iZWUtZGV2IiwiYXV0aF90aW1lIjoxNzI4NTg5MjczLCJ1c2VyX2lkIjoiblFzWTNTQUhVbFhsOTcwSFk1amh2eER4Rk10MiIsInN1YiI6Im5Rc1kzU0FIVWxYbDk3MEhZNWpodnhEeEZNdDIiLCJpYXQiOjE3MjkxOTI0NzYsImV4cCI6MTcyOTE5NjA3NiwiZW1haWwiOiJhZG1pbkBleGFtcGxlLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJlbWFpbCI6WyJhZG1pbkBleGFtcGxlLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6InBhc3N3b3JkIn19.sS0PWtI4q2eAogmI3Uqw3Vmh9i9VCPIHNa1x3eDcs8hQuICM4CSj9sUvQLdVdHhx6gLTXB6XzU8u58CfCGjz7SD7QAnqmVyle4eaHu7MuPnY__4ieAwmCnFutpaxuFXWhbeq84nUEXuvgZGJIr4g_nCDPqWWDfXg1dYn0n5KIlvgCWe3eGd0nuHUnoWWF6dFSgf8eYmoEdyJ3VvOP4975imL0XKBdtJjbEgo7N8sUA3r_wWxV9U-hL7a-i50vhMCZ49vT7ncPnRNUuZAhq_PL0T_N2qu5MAPbWXtHiPWsI6CM2UDikpSqZIvGIWNyjim5GhWOTQy1vuNfpa99L6oaw"
    }
    
    request_node = RequestNode()
    result = request_node.execute(node_data)
    print("API Request Result:", json.dumps(RequestNode.log_safe_node_data(result), indent=2))