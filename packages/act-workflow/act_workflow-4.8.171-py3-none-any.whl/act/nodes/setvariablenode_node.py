import os
import json
import logging
from typing import Dict, Any, List, Union
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NodeOperationError(Exception):
    pass

class SetVariableNode:
    def __init__(self, sandbox_timeout=None):
        logger.info("Initializing SetVariableNode")
        self.sandbox_timeout = sandbox_timeout

    def execute(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("Starting execution of SetVariableNode")
        logger.debug(f"Received node_data: {json.dumps(node_data, indent=2)}")

        form_data = node_data.get('formData', {})
        if isinstance(form_data, str):
            try:
                form_data = json.loads(form_data)
            except json.JSONDecodeError:
                return {"status": "error", "message": "Invalid formData format"}

        try:
            variables = form_data.get('variables', [])
            if not variables:
                raise NodeOperationError("No variables specified for setting.")

            result = self.set_variables(variables, node_data)
            logger.info("Variables set successfully")
            return {"status": "success", "result": result}
        except NodeOperationError as e:
            logger.error(f"Error in executing operation: {str(e)}")
            return {"status": "error", "message": str(e)}

    def set_variables(self, variables: List[Dict[str, Any]], node_data: Dict[str, Any]) -> Dict[str, Any]:
        result = {}
        
        for variable in variables:
            variable_name = variable.get('name')
            variable_type = variable.get('type', 'string')
            variable_value = variable.get('value')
            
            if not variable_name:
                raise NodeOperationError("Variable name is required")

            # Resolve any placeholders in the value
            resolved_value = self.resolve_path_placeholders(variable_value, node_data)
            
            # Convert the value based on the specified type
            try:
                typed_value = self.convert_value_type(resolved_value, variable_type)
            except ValueError as e:
                raise NodeOperationError(f"Error converting value for variable {variable_name}: {str(e)}")

            result[variable_name] = typed_value

        return result

    def convert_value_type(self, value: Any, type_name: str) -> Any:
        if value is None:
            return None

        try:
            if type_name == 'string':
                return str(value)
            elif type_name == 'number':
                if isinstance(value, str):
                    # Handle both integer and float cases
                    return float(value) if '.' in value else int(value)
                return value
            elif type_name == 'boolean':
                if isinstance(value, str):
                    return value.lower() == 'true'
                return bool(value)
            elif type_name == 'array':
                if isinstance(value, str):
                    return json.loads(value)
                elif isinstance(value, (list, tuple)):
                    return list(value)
                raise ValueError(f"Cannot convert {type(value)} to array")
            elif type_name == 'object':
                if isinstance(value, str):
                    return json.loads(value)
                elif isinstance(value, dict):
                    return value
                raise ValueError(f"Cannot convert {type(value)} to object")
            else:
                raise NodeOperationError(f"Unsupported variable type: {type_name}")
        except Exception as e:
            raise ValueError(f"Error converting to {type_name}: {str(e)}")

    def resolve_path_placeholders(self, data: Any, node_data: Dict[str, Any]) -> Any:
        if isinstance(data, str):
            pattern = re.compile(r"\{\{(.*?)\}\}")
            matches = pattern.findall(data)

            for match in matches:
                parts = match.split('.')
                node_id = parts[0]
                path = '.'.join(parts[1:])
                value = self.fetch_value(node_id, path, node_data)
                if value is not None:
                    data = data.replace(f"{{{{{match}}}}}", str(value))

            return data
        elif isinstance(data, dict):
            return {k: self.resolve_path_placeholders(v, node_data) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.resolve_path_placeholders(item, node_data) for item in data]
        else:
            return data

    def fetch_value(self, node_id: str, path: str, node_data: Dict[str, Any]) -> Any:
        try:
            node_result = node_data.get('results', {}).get(node_id, {})
            for part in path.split('.'):
                node_result = node_result.get(part, None)
                if node_result is None:
                    break
            return node_result
        except Exception as e:
            logger.error(f"Failed to fetch value for {node_id}.{path}: {str(e)}")
            return None

# Alias the class name for compatibility
SetVariableNode = SetVariableNode

if __name__ == "__main__":
    # Test data for setting variables
    test_data = {
        "formData": {
            "variables": [
                {
                    "name": "user_name",
                    "type": "string",
                    "value": "John Doe"
                },
                {
                    "name": "age",
                    "type": "number",
                    "value": "30"
                },
                {
                    "name": "is_active",
                    "type": "boolean",
                    "value": "true"
                },
                {
                    "name": "tags",
                    "type": "array",
                    "value": '["tag1", "tag2"]'
                },
                {
                    "name": "metadata",
                    "type": "object",
                    "value": '{"key": "value"}'
                }
            ]
        },
        "results": {}
    }

    # Create and execute the node
    node = SetVariableNode()
    result = node.execute(test_data)
    print(json.dumps(result, indent=2))