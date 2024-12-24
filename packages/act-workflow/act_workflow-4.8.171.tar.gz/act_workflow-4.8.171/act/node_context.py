from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class NodeContext:
    input_data: Dict[str, Any]
    output_data: Dict[str, Any]
    node_type: str
    node_name: str
