import importlib
import traceback
import logging
import json
from typing import Dict, Any, List
import asyncio
from datetime import datetime, timedelta
import re
import os
from .actfile_parser import ActfileParser, ActfileParserError
from pathlib import Path
from .workflow_engine import WorkflowEngine
from .node_context import NodeContext

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ExecutionManager:
    def __init__(self, actfile_path: str = 'Actfile', sandbox_timeout: int = 600):
        logger.info(f"Initializing ExecutionManager")
        self.actfile_path = actfile_path
        self.node_results = {}
        self.execution_queue = asyncio.Queue()
        self.sandbox_timeout = sandbox_timeout
        self.sandbox_start_time = None
        self.load_workflow()
        self.actfile_path = Path(actfile_path)
        self.workflow_engine = WorkflowEngine()


    def load_workflow(self):
        logger.info("Loading workflow data")
        try:
            parser = ActfileParser(self.actfile_path)
            self.workflow_data = parser.parse()
            self.actfile_parser = parser
        except ActfileParserError as e:
            logger.error(f"Error parsing Actfile: {e}")
            raise

        self.load_node_executors()

    def load_node_executors(self):
        logger.info("Loading node executors")
        node_types = set(node['type'] for node in self.workflow_data['nodes'].values())
        self.node_executors = {}
        for node_type in node_types:
            try:
                logger.info(f"Attempting to load node type: {node_type}")
                if node_type == 'DataTransformation':
                    # Specific handling for DataTransformation
                    from act.nodes.data_transformation_node import DataTransformationNode
                    self.node_executors[node_type] = DataTransformationNode(sandbox_timeout=self.sandbox_timeout)
                    logger.info(f"DataTransformationNode loaded successfully")
                else:
                    module_name = f"act.nodes.{node_type.lower()}_node"
                    module = importlib.import_module(module_name)
                    logger.info(f"Module loaded: {module}")

                    class_names = [
                        f"{node_type}Node",
                        f"{node_type.capitalize()}Node",
                        f"{node_type}NodeNode",
                        node_type
                    ]

                    for class_name in class_names:
                        logger.info(f"Looking for class: {class_name}")
                        if hasattr(module, class_name):
                            node_class = getattr(module, class_name)
                            logger.info(f"Class found: {node_class}")
                            if 'sandbox_timeout' in node_class.__init__.__code__.co_varnames:
                                node_instance = node_class(sandbox_timeout=self.sandbox_timeout)
                            else:
                                node_instance = node_class()
                            if hasattr(node_instance, 'set_execution_manager'):
                                node_instance.set_execution_manager(self)
                            self.node_executors[node_type] = node_instance
                            logger.info(f"Executor created for {node_type}")
                            break
                    else:
                        logger.warning(f"No suitable class found for {node_type}")
                        raise AttributeError(f"No suitable class found for {node_type}")

            except Exception as e:
                logger.error(f"Error loading node type '{node_type}': {str(e)}")
                logger.error(traceback.format_exc())
                from act.nodes.generic_node import GenericNode
                self.node_executors[node_type] = GenericNode()
                logger.info(f"Fallback to GenericNode for {node_type}")

    def execute_workflow(self) -> Dict[str, Any]:
        logger.info(f"Starting execution of workflow")
        self.node_results = {}
        execution_queue = []
        self.sandbox_start_time = datetime.now()

        try:
            start_node_name = self.actfile_parser.get_start_node()
            if not start_node_name:
                logger.error("No start node specified in Actfile.")
                return {"status": "error", "message": "No start node specified in Actfile.", "results": {}}

            execution_queue.append((start_node_name, None))

            while execution_queue:
                if self.is_sandbox_expired():
                    logger.warning("Sandbox has expired. Stopping execution.")
                    return {
                        "status": "warning",
                        "message": "Workflow execution stopped due to sandbox expiration",
                        "results": self.node_results
                    }

                node_name, input_data = execution_queue.pop(0)
                node_result = self.execute_node(node_name, input_data)
                self.node_results[node_name] = node_result

                if node_result.get('status') == 'error':
                    logger.error(f"Node {node_name} execution failed. Stopping workflow.")
                    return {
                        "status": "error",
                        "message": f"Workflow execution failed at node {node_name}",
                        "results": self.node_results
                    }

                successors = self.actfile_parser.get_node_successors(node_name)
                for successor in successors:
                    logger.debug(f"Queueing next node: {successor}")
                    execution_queue.append((successor, node_result))

            logger.info("Workflow execution completed")
            return {
                "status": "success",
                "message": "Workflow executed successfully",
                "results": self.node_results
            }

        except Exception as e:
            logger.error(f"Error during workflow execution: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "message": f"Workflow execution failed: {str(e)}",
                "results": self.node_results
            }

    def execute_node(self, node_name: str, input_data: Dict[str, Any] = None) -> Dict[str, Any]:
        logger.info(f"Executing node: {node_name}")
        try:
            if self.is_sandbox_expired():
                return {"status": "error", "message": "Sandbox expired"}

            node = self.workflow_data['nodes'][node_name]
            node_type = node.get('type')
            node_data = node.copy()

            if input_data:
                node_data['input'] = input_data

            resolved_node_data = self.resolve_placeholders_for_execution(node_data)

            logger.info(f"Node type: {node_type}")
            logger.info(f"Node data after resolving placeholders: {self.log_safe_node_data(resolved_node_data)}")

            executor = self.node_executors.get(node_type)
            if executor:
                logger.info(f"Executor found for node type: {node_type}")

                result = executor.execute(resolved_node_data)
                logger.info(f"Node {node_name} execution result: {self.log_safe_node_data(result)}")

                return result
            else:
                logger.error(f"No executor found for node type: {node_type}")
                return {"status": "error", "message": f"No executor found for node type: {node_type}"}

        except Exception as e:
            logger.error(f"Error executing node {node_name}: {str(e)}")
            logger.error(traceback.format_exc())
            return {"status": "error", "message": str(e)}

    def is_sandbox_expired(self) -> bool:
        if self.sandbox_start_time is None:
            return False
        elapsed_time = datetime.now() - self.sandbox_start_time
        return elapsed_time.total_seconds() >= (self.sandbox_timeout - 30)  # Give 30 seconds buffer

    def resolve_placeholders_for_execution(self, data: Any) -> Any:
        if isinstance(data, dict):
            return {k: self.resolve_placeholders_for_execution(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.resolve_placeholders_for_execution(item) for item in data]
        elif isinstance(data, str):
            return self.resolve_placeholder_string(data)
        return data

    def resolve_placeholder_string(self, text: str) -> str:
        # Handle environment variables
        if text.startswith('${') and text.endswith('}'):
            env_var = text[2:-1]
            return os.environ.get(env_var, text)
        
        pattern = re.compile(r'\{\{(.*?)\}\}')
        matches = pattern.findall(text)
        
        for match in matches:
            parts = match.split('.')
            node_id = parts[0]
            path = '.'.join(parts[1:])
            value = self.fetch_value(node_id, path)
            if value is not None:
                text = text.replace(f"{{{{{match}}}}}", str(value))
        
        return text

    def fetch_value(self, node_id: str, path: str) -> Any:
        logger.info(f"Fetching value for node_id: {node_id}, path: {path}")
        if node_id in self.node_results:
            result = self.node_results[node_id]
            for part in path.split('.'):
                if isinstance(result, dict) and part in result:
                    result = result[part]
                else:
                    return None
            return result
        return None

    @staticmethod
    def log_safe_node_data(node_data):
        if isinstance(node_data, dict):
            safe_data = {k: ('[REDACTED]' if k == 'api_key' else v) for k, v in node_data.items()}
        else:
            safe_data = node_data
        return json.dumps(safe_data, indent=2)

    @classmethod
    def register_node_type(cls, node_type: str, node_class: Any):
        logger.info(f"Registering custom node type: {node_type}")
        if not hasattr(cls, 'custom_node_types'):
            cls.custom_node_types = {}
        cls.custom_node_types[node_type] = node_class

    def get_node_executor(self, node_type: str) -> Any:
        if hasattr(self, 'custom_node_types') and node_type in self.custom_node_types:
            return self.custom_node_types[node_type]()
        return self.node_executors.get(node_type)

if __name__ == "__main__":
    # This block is for testing the ExecutionManager class independently
    execution_manager = ExecutionManager(actfile_path='path/to/your/Actfile', sandbox_timeout=600)
    result = execution_manager.execute_workflow()
    print(json.dumps(result, indent=2))