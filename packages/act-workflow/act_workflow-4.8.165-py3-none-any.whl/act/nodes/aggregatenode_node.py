import os
import json
import logging
from typing import Dict, Any, List, Union
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NodeOperationError(Exception):
    pass

class AggregateNode:
    def __init__(self, sandbox_timeout=None):
        logger.info("Initializing AggregateNode")
        self.sandbox_timeout = sandbox_timeout


    def execute(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("Starting execution of AggregateNode")
        logger.debug(f"Received node_data: {json.dumps(node_data, indent=2)}")

        form_data = node_data.get('formData', {})
        if isinstance(form_data, str):
            try:
                form_data = json.loads(form_data)
            except json.JSONDecodeError:
                return {"status": "error", "message": "Invalid formData format"}

        aggregate_method = form_data.get('aggregate', '')

        try:
            items = node_data.get('items', [])
            if isinstance(items, str):
                try:
                    items = json.loads(items)
                except json.JSONDecodeError:
                    items = [{"content": items}]

            if aggregate_method == 'Individual Fields':
                result = self.aggregate_individual_fields(form_data, {"items": items})
            elif aggregate_method == 'All Item Data (Into a Single List)':
                result = self.aggregate_all_item_data(form_data, {"items": items})
            else:
                raise NodeOperationError(f"Invalid aggregation method: {aggregate_method}")

            logger.info("Aggregation completed successfully")
            return {"status": "success", "result": result}
        except NodeOperationError as e:
            logger.error(f"Error in executing operation: {str(e)}")
            return {"status": "error", "message": str(e)}

    def aggregate_individual_fields(self, form_data: Dict[str, Any], node_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        fields_to_aggregate = form_data.get('fieldsToAggregate', [])
        if not fields_to_aggregate:
            raise NodeOperationError("No fields specified for aggregation.")

        aggregated_data = {}
        for field in fields_to_aggregate:
            input_field_name = field.get('inputFieldName')
            rename_field = field.get('renameField', False)
            output_field_name = field.get('outputFieldName') if rename_field else input_field_name

            field_values = []
            for item in node_data.get('items', []):
                value = self.fetch_value_from_item(item, input_field_name)
                if value is not None:
                    field_values.append(value)

            if output_field_name in aggregated_data:
                raise NodeOperationError(f"Duplicate output field name: {output_field_name}")

            aggregated_data[output_field_name] = field_values

        return [aggregated_data]

    def aggregate_all_item_data(self, form_data: Dict[str, Any], node_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        put_output_in_field = form_data.get('putOutputInField', 'aggregatedData')
        include_option = form_data.get('include', 'All Fields')
        fields_to_include_or_exclude = form_data.get('fieldsToIncludeOrExclude', '').split(',')

        aggregated_data = []
        for item in node_data.get('items', []):
            if include_option == 'All Fields':
                aggregated_data.append(item)
            elif include_option == 'Specified Fields':
                filtered_item = {k: v for k, v in item.items() if k in fields_to_include_or_exclude}
                aggregated_data.append(filtered_item)
            elif include_option == 'All Fields Except':
                filtered_item = {k: v for k, v in item.items() if k not in fields_to_include_or_exclude}
                aggregated_data.append(filtered_item)

        return [{put_output_in_field: aggregated_data}]

    def fetch_value_from_item(self, item: Dict[str, Any], field_name: str) -> Any:
        try:
            return item.get(field_name)
        except KeyError:
            logger.warning(f"Field {field_name} not found in item.")
            return None

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
AggregateNode = AggregateNode

if __name__ == "__main__":
    test_data = {
        "formData": {
            "accessToken": "your_access_token",
            "aggregate": "Individual Fields",
            "fieldsToAggregate": [
                {"inputFieldName": "name", "renameField": True, "outputFieldName": "aggregatedName"},
                {"inputFieldName": "age", "renameField": False}
            ]
        },
        "items": [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25}
        ],
        "results": {}
    }

    node = AggregateNode()
    result = node.execute(test_data)
    print(json.dumps(result, indent=2))