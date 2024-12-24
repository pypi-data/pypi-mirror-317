import os
import json
import logging
from typing import Dict, Any
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ConditionNode:
    def __init__(self):
        logger.info("Initializing ConditionNode")

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
        logger.info("Starting execution of ConditionNode")
        logger.info(f"Received node_data: {json.dumps(self.log_safe_node_data(node_data), indent=2)}")
        
        condition = node_data.get('condition')
        true_branch = node_data.get('true_branch')
        false_branch = node_data.get('false_branch')

        if not condition:
            logger.error("Missing condition")
            return {"status": "error", "message": "Missing condition"}

        if not true_branch or not false_branch:
            logger.error("Missing true_branch or false_branch")
            return {"status": "error", "message": "Missing true_branch or false_branch"}

        try:
            # Resolve any placeholders in the condition
            resolved_condition = self.resolve_path_placeholders(condition, node_data)
            
            # Evaluate the condition
            condition_result = eval(resolved_condition)

            result = {
                "status": "success",
                "result": {
                    "condition_met": condition_result,
                    "next_node": true_branch if condition_result else false_branch
                }
            }
            
            logger.info(f"Condition evaluation result: {condition_result}")
            logger.info(f"Next node: {result['result']['next_node']}")
            
            return result

        except Exception as e:
            error_msg = f"Unexpected error during condition evaluation: {str(e)}"
            logger.error(error_msg)
            return {"status": "error", "message": error_msg}

    @staticmethod
    def log_safe_node_data(node_data):
        if isinstance(node_data, dict):
            return {k: v for k, v in node_data.items() if k not in ['condition', 'true_branch', 'false_branch']}
        return node_data

ConditionNodeNode = ConditionNode

if __name__ == "__main__":
    test_data = {
        "condition": "{{api_request.output.body.length}} > 0",
        "true_branch": "summarize",
        "false_branch": "error_notification",
        "input": {
            "api_request": {
                "output": {
                    "body": [{"some": "data"}]
                }
            }
        }
    }

    node = ConditionNode()
    result = node.execute(test_data)
    print(json.dumps(result, indent=2))