# function_caller/tools/__init__.py

from typing import Dict, Callable
import inspect

class ToolRegistry:
    def __init__(self, tools: Dict[str, Callable]):
        self.tools = {}
        for name, func in tools.items():
            self.register_tool(name, func)

    def register_tool(self, name: str, func: Callable):
        # Attempt to auto-detect description and parameters
        description = getattr(func, 'description', func.__doc__)
        if not description:
            raise ValueError(f"Function '{name}' does not have a description. Please provide one or add a docstring.")
        parameters = getattr(func, 'parameters', self._get_func_parameters(func))
        self.tools[name] = func
        func.description = description
        func.parameters = parameters

    def _get_func_parameters(self, func: Callable) -> Dict[str, Dict[str, str]]:
        sig = inspect.signature(func)
        parameters = {}
        for param_name, param in sig.parameters.items():
            if param.annotation != inspect.Parameter.empty:
                param_type = param.annotation.__name__
            else:
                param_type = 'str'
            parameters[param_name] = {
                'type': param_type,
                'description': ''
            }
        return parameters

    def register_tools(self, new_tools: Dict[str, Callable]):
        for name, func in new_tools.items():
            self.register_tool(name, func)

    def get_tools_description(self) -> str:
        descriptions = ""
        for tool_name, tool in self.tools.items():
            descriptions += f"### {tool_name}\n"
            descriptions += f"Description: {tool.description}\n"
            descriptions += "Parameters:\n"
            for param_name, param_info in tool.parameters.items():
                param_type = param_info.get('type', 'string')
                param_desc = param_info.get('description', '')
                # Escape braces in parameter descriptions
                param_desc = param_desc.replace('{', '{{').replace('}', '}}')
                descriptions += f"- {param_name} ({param_type}): {param_desc}\n"
            descriptions += "\n"
        return descriptions