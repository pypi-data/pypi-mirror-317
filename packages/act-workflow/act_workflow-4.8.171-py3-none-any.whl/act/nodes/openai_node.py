import logging
from typing import Dict, Any
import openai
import os

logger = logging.getLogger(__name__)

class OpenAINode:
    def __init__(self):
        logger.info("Initializing OpenAINode")
        openai_api_key = os.environ.get('OPENAI_API_KEY')
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        openai.api_key = openai_api_key

    def execute(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        operation = node_data.get('operation')
        if operation == 'parseBugReport':
            return self.parse_bug_report(node_data)
        elif operation == 'validateBugReport':
            return self.validate_bug_report(node_data)
        else:
            raise ValueError(f"Unsupported operation: {operation}")

    def parse_bug_report(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        model = node_data.get('model', 'gpt-3.5-turbo')
        prompt = node_data.get('prompt', 'Parse the following bug report:')
        bug_report = node_data.get('bug_report', '')
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": bug_report}
                ]
            )
            parsed = response.choices[0].message['content'].strip()
            return {"status": "success", "output": {"parsed_report": parsed}}
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return {"status": "error", "message": str(e), "output": None}

    def validate_bug_report(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        model = node_data.get('model', 'gpt-3.5-turbo')
        prompt = node_data.get('prompt', 'Validate the following bug report:')
        parsed_report = node_data.get('parsed_report', '')
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": parsed_report}
                ]
            )
            validation = response.choices[0].message['content'].strip()
            return {"status": "success", "output": {"is_complete": validation == "Complete"}}
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return {"status": "error", "message": str(e), "output": None}
