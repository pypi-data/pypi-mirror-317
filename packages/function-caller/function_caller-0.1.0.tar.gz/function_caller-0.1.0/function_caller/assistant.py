# function_caller/assistant.py

import logging
import json
from typing import Dict, Any, List, Optional
from .tools import ToolRegistry
from .model_interface import ModelInterface
from .prompts.default_prompt import DEFAULT_SYSTEM_PROMPT
from .utils.history_manager import HistoryManager
from .utils.logger import setup_logger
from .utils.message_formatter import parse_assistant_response

class Assistant:
    def __init__(
        self,
        model_interface: ModelInterface,
        tools: Dict[str, callable],
        use_native_function_calling: bool = False,
        system_prompt: Optional[str] = DEFAULT_SYSTEM_PROMPT,
        knowledge_cutoff: str = "September 2021",
        name: str = "AI Assistant",
        save_history: bool = True,
        history_dir: str = 'history',
        log_to_file: bool = False,
        log_to_console: bool = True
    ):
        self.model_interface = model_interface
        self.tool_registry = ToolRegistry(tools)
        self.use_native_function_calling = use_native_function_calling
        self.system_prompt = system_prompt
        self.knowledge_cutoff = knowledge_cutoff
        self.history_manager = HistoryManager(save_history=save_history, history_dir=history_dir)
        self.name = name
        self._initialize_history()
        self.logger = setup_logger(__name__, log_to_file=log_to_file, log_to_console=log_to_console)

    def _escape_braces(self, text: str) -> str:
        return text.replace('{', '{{').replace('}', '}}')

    def _initialize_history(self):
        if not self.history_manager.get_current_messages():
            escaped_tools_description = self._escape_braces(
                self.tool_registry.get_tools_description()
            )
            self.history_manager.add_message({
                "role": "system",
                "content": self.system_prompt.format(
                    tools_description=escaped_tools_description,
                    knowledge_cutoff=self.knowledge_cutoff,
                    name=self.name
                )
            })

    def handle_message(self, user_message: str) -> str:
        self.history_manager.add_message({
            "role": "user",
            "content": user_message
        })
        self.logger.info(f"User message: {user_message}")

        assistant_response = self.model_interface.generate(
            self.history_manager.get_current_messages()
        )
        self.logger.debug(f"Assistant raw response: {assistant_response}")

        parsed_response = parse_assistant_response(assistant_response)
        self.logger.info(f"Parsed response: {parsed_response}")

        if parsed_response.get("function_calls"):
            # Add the function call to the history before execution
            self.history_manager.add_message({
                "role": "assistant",
                "content": json.dumps(parsed_response["function_calls"]) # Add function calls in the correct format
            })

            function_results = self._execute_function_calls(parsed_response["function_calls"])
            self.logger.info(f"Function call results: {function_results}")

            for tool_name, result in function_results.items():
                self.history_manager.add_message({
                    "role": "user",
                    "content": f"The '{tool_name}' function was called with the provided input and returned the following result: {result}. Now, provide a natural language response based on this result."
                })

            # Generate final response using the entire conversation history
            final_response = self.model_interface.generate(
                self.history_manager.get_current_messages(),
                disable_function_calls=True  # Disable function calls for the final generation
            )

            # Add only the final response to history
            self.history_manager.add_message({
                "role": "assistant",
                "content": final_response.strip()
            })
            return final_response.strip()

        else:
            # Add only the parsed response to history
            self.history_manager.add_message({
                "role": "assistant",
                "content": parsed_response["message"].strip()
            })
            return parsed_response["message"].strip()

    def _execute_function_calls(self, function_calls: List[Dict[str, Any]]) -> Dict[str, str]:
        results = {}

        for call in function_calls:
            tool_name = call.get("tool_name")
            tool_input = call.get("tool_input")

            if tool_name not in self.tool_registry.tools:
                error_message = f"Error: Tool '{tool_name}' not found."
                self.logger.error(error_message)
                results[tool_name] = error_message
                continue

            try:
                self.logger.debug(f"Executing tool: {tool_name}")
                self.logger.debug(f"Tool input: {tool_input}")

                if isinstance(tool_input, dict):
                    result = self.tool_registry.tools[tool_name](**tool_input)
                elif isinstance(tool_input, str):
                    result = self.tool_registry.tools[tool_name](tool_input)
                else:
                    error_message = f"Error: Invalid input format for tool '{tool_name}'. Expected a dictionary or a string."
                    self.logger.error(error_message)
                    results[tool_name] = error_message
                    continue

                self.logger.debug(f"Tool execution result: {result}")
                results[tool_name] = result

            except Exception as e:
                error_message = f"Error: Tool '{tool_name}' execution failed: {str(e)}"
                self.logger.error(error_message, exc_info=True)
                results[tool_name] = error_message

        return results