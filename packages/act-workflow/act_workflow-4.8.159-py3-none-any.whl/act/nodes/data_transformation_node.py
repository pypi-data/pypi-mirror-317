import json
import logging
from typing import Dict, Any, List, Union
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataTransformationNode:
    def __init__(self):
        logger.info("Initializing DataTransformationNode")

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
        logger.info("Starting execution of DataTransformationNode")
        logger.info(f"Received node_data: {json.dumps(self.log_safe_node_data(node_data), indent=2)}")
        
        input_data = node_data.get('input_data')
        operations = node_data.get('operations', [])

        if not input_data:
            logger.error("Missing input data")
            return {"status": "error", "message": "Missing input data"}

        if not operations:
            logger.error("No operations specified")
            return {"status": "error", "message": "No operations specified"}

        try:
            # Resolve any placeholders in the input data before processing
            resolved_input_data = self.resolve_path_placeholders(json.dumps(input_data), node_data)
            input_data = json.loads(resolved_input_data)
            logger.info(f"Resolved input data: {input_data}")

            result = self.apply_operations(input_data, operations)
            logger.info(f"Transformation result: {result}")

            return {
                "status": "success",
                "result": result
            }

        except Exception as e:
            error_msg = f"Unexpected error during execution: {str(e)}"
            logger.error(error_msg)
            return {"status": "error", "message": error_msg}

    def apply_operations(self, data: Any, operations: List[Dict[str, Any]]) -> Any:
        """
        Apply a series of operations to the input data.
        """
        for operation in operations:
            op_type = operation.get('type')
            if op_type == 'filter':
                data = self.filter_operation(data, operation.get('condition'))
            elif op_type == 'map':
                data = self.map_operation(data, operation.get('transformation'))
            elif op_type == 'reduce':
                data = self.reduce_operation(data, operation.get('function'))
            elif op_type == 'sort':
                data = self.sort_operation(data, operation.get('key'), operation.get('reverse', False))
            elif op_type == 'add':
                data = self.add_operation(data, operation.get('item'), operation.get('position'))
            else:
                logger.warning(f"Unknown operation type: {op_type}")
        return data

    def filter_operation(self, data: List[Dict[str, Any]], condition: str) -> List[Dict[str, Any]]:
        return list(filter(lambda item: eval(condition, {'item': item}), data))

    def map_operation(self, data: List[Dict[str, Any]], transformation: str) -> List[Any]:
        return [eval(transformation, {'item': item}) for item in data]

    def reduce_operation(self, data: List[Any], function: str) -> Any:
        from functools import reduce
        return reduce(eval(f"lambda x, y: {function}"), data)

    def sort_operation(self, data: List[Dict[str, Any]], key: str, reverse: bool) -> List[Dict[str, Any]]:
        return sorted(data, key=lambda x: x[key], reverse=reverse)

    def add_operation(self, data: List[Dict[str, Any]], item: Dict[str, Any], position: Union[int, str] = 'end') -> List[Dict[str, Any]]:
        """
        Add a new item to the data list at the specified position.
        If position is 'start', add to the beginning. If 'end' or not specified, add to the end.
        If position is an integer, add at that index.
        """
        if position == 'start':
            return [item] + data
        elif position == 'end' or position is None:
            return data + [item]
        elif isinstance(position, int):
            return data[:position] + [item] + data[position:]
        else:
            logger.warning(f"Invalid position '{position}' for add operation. Adding to the end.")
            return data + [item]

    @staticmethod
    def log_safe_node_data(node_data):
        if isinstance(node_data, dict):
            safe_data = {k: ('[REDACTED]' if k in ['auth_value', 'api_key'] else v) for k, v in node_data.items()}
        else:
            safe_data = node_data
        return safe_data

DataTransformationNodeNode = DataTransformationNode

if __name__ == "__main__":
    test_data = {
        "input_data": [
            {"name": "Alice", "age": 30, "score": 85},
            {"name": "Bob", "age": 25, "score": 92},
            {"name": "Charlie", "age": 35, "score": 78},
        ],
        "operations": [
            {"type": "filter", "condition": "item['age'] > 25"},
            {"type": "map", "transformation": "{'name': item['name'], 'score': item['score']}"},
            {"type": "sort", "key": "score", "reverse": True},
            {"type": "add", "item": {"name": "David", "score": 88}, "position": "start"}
        ]
    }

    node = DataTransformationNode()
    result = node.execute(test_data)
    print(json.dumps(result, indent=2))