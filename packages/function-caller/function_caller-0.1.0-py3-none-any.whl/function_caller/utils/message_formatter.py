# function_caller/utils/message_formatter.py

import json

def parse_assistant_response(response: str) -> dict:
    """Parses the assistant's response to extract function calls or direct messages."""
    try:
        # Attempt to parse response as JSON
        parsed_response = json.loads(response)

        # Check if it's a list of dictionaries (function calls)
        if isinstance(parsed_response, list) and all(isinstance(item, dict) for item in parsed_response):
            return {"function_calls": parsed_response}
        # If not, treat as a direct message
        else:
            return {"message": response}
    except json.JSONDecodeError:
        # If JSON parsing fails, treat as a direct message
        return {"message": response}