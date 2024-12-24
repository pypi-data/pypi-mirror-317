import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class GenericNode:
    def execute(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("Executing GenericNode for operation")
        operation = node_data.get('operation', '').lower()
        input_data = node_data.get('input', {})

        if operation == 'get':
            return self.handle_get(input_data)
        elif operation == 'post':
            return self.handle_post(input_data)
        elif operation == 'put':
            return self.handle_put(input_data)
        elif operation == 'delete':
            return self.handle_delete(input_data)
        else:
            return {"status": "error", "message": f"Unsupported operation: {operation}", "output": None}

    def handle_get(self, input_data):
        return {"status": "success", "message": "GET operation handled", "output": input_data}

    def handle_post(self, input_data):
        return {"status": "success", "message": "POST operation handled", "output": input_data}

    def handle_put(self, input_data):
        return {"status": "success", "message": "PUT operation handled", "output": input_data}

    def handle_delete(self, input_data):
        return {"status": "success", "message": "DELETE operation handled", "output": input_data}
