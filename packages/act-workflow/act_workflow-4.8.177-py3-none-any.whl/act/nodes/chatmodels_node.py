import os
import json
import logging
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ChatModelsNode:
    def __init__(self, sandbox_timeout=None):
        logger.info("Initializing ChatModelsNode")
        self.sandbox_timeout = sandbox_timeout

    def execute(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("Starting execution of ChatModelsNode")
        logger.info(f"Received node_data: {json.dumps(self.log_safe_node_data(node_data), indent=2)}")

    def extract_text(self, input_text: str) -> str:
        """
        Extract the actual text string from various possible input formats.
        """
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
        """
        Resolve any path placeholders in the input text before processing.
        """
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
        """
        Fetch the value from the node_data based on the node_id and path.
        """
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
        logger.info("Starting execution of ChatModelsNode")
        logger.info(f"Received node_data: {json.dumps(self.log_safe_node_data(node_data), indent=2)}")
        
        api_key = node_data.get('api_key')
        model_name = node_data.get('model', 'gpt-3.5-turbo')
        input_text = node_data.get('input_text')

        if not api_key:
            logger.error("Missing API key")
            return {"status": "error", "message": "Missing API key"}

        if not input_text:
            logger.error("Missing input text")
            return {"status": "error", "message": "Missing input text"}

        try:
            # Resolve any placeholders in the input text before processing
            resolved_input_text = self.resolve_path_placeholders(input_text, node_data)
            logger.info(f"Resolved input text: {resolved_input_text}")

            # Extract the actual text string
            actual_text = self.extract_text(resolved_input_text)
            logger.info(f"Extracted text: {actual_text}")

            self.model = ChatOpenAI(api_key=api_key, model_name=model_name)
            message = HumanMessage(content=actual_text)
            response = self.model.invoke([message])
            response_text = response.content
            logger.info(f"Model response: {response_text}")

            result = {
                "status": "success",
                "result": {
                    "response": response_text
                }
            }
            logger.info(f"Execution completed successfully. Result: {json.dumps(self.log_safe_node_data(result), indent=2)}")
            return result

        except Exception as e:
            error_msg = f"Unexpected error during execution: {str(e)}"
            logger.error(error_msg)
            return {"status": "error", "message": error_msg}

    @staticmethod
    def log_safe_node_data(node_data):
        if isinstance(node_data, dict):
            safe_data = {k: ('[REDACTED]' if k == 'api_key' else v) for k, v in node_data.items()}
        else:
            safe_data = node_data
        return safe_data

ChatModelsNode = ChatModelsNode


if __name__ == "__main__":
    test_data = {
        "api_key": os.environ.get("OPENAI_API_KEY"),
        "input_text": "Explain the concept of quantum entanglement in simple terms.",
        "model": "gpt-4"
    }

    node = ChatModelsNode()
    result = node.execute(test_data)
    print(json.dumps(result, indent=2))