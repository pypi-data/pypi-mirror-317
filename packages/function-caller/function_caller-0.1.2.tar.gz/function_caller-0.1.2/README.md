# Function Caller: Unleash the Power of Function Calling in Any AI Model

<!-- [![PyPI version](https://badge.fury.io/py/function-caller.svg)](https://badge.fury.io/py/function-caller)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/yourusername/function-caller/workflows/Tests/badge.svg)](https://github.com/yourusername/function-caller/actions?query=workflow%3ATests)
[![codecov](https://codecov.io/gh/yourusername/function-caller/branch/main/graph/badge.svg?token=YOUR_CODECOV_TOKEN)](https://codecov.io/gh/yourusername/function-caller)
[![Downloads](https://static.pepy.tech/badge/function-caller)](https://pepy.tech/project/function-caller) -->

## 🌟 Overview

**Function Caller** is a powerful and flexible Python package that brings function calling capabilities to *any* AI language model, even those without native support. This package empowers developers to seamlessly integrate external tools and APIs into their AI workflows, enhancing the capabilities and real-world applicability of their models.

## ✨ Key Features

*   **Universal Function Calling:** Extend any AI model with function calling, regardless of its inherent capabilities.
*   **Easy Integration:** Simple and intuitive API for defining and registering custom tools.
*   **Flexible Tool Definition:** Supports automatic description and parameter detection for Python functions.
*   **Robust Error Handling:** Gracefully handles tool execution failures and provides informative error messages.
*   **Conversation History Management:** Built-in history tracking for multi-turn interactions.
*   **Customizable Logging:** Configure logging to console and/or file with different levels of detail.
*   **Support for Multiple AI Providers:** Currently supports DeepInfra, and Sambanova, with more to come.
*   **Non-Native Function Calling Support:** Seamlessly implements function calling using a JSON-based approach for models that don't natively support it.
*   **Streamlined Assistant Setup:** Easily configure and initialize an AI assistant with custom tools, system prompts, and behavior.
*   **Modular Design:** Well-structured codebase for easy maintenance and extension.

## 🚀 Installation

Install Function Caller directly from PyPI:

```bash
pip install -U function-caller
```

## 🛠️ Usage Guide

### 1. Define Your Tools

Create Python functions that represent the actions your AI can perform. Add metadata using docstrings or directly as attributes:

```python
# example_tools.py
import json
import requests

def get_weather(city: str) -> str:
    """
    Get current weather information for a city.

    Args:
        city (str): The name of the city.

    Returns:
        str: A JSON string containing weather information.
    """
    try:
        # ... (Implementation to fetch weather data) ...
        return json.dumps({"weather": "sunny and warm"})
    except Exception as e:
        return json.dumps({"error": str(e)})

# Automatic metadata detection from docstrings is supported.
# You can also add metadata directly:
get_weather.description = "Get current weather information for a city."  # Optional if docstring is present
get_weather.parameters = {
    "city": {"type": "string", "description": "Name of the city"}
}

# Example of another tool:
def file_operations(operation: str, filename: str = "", content: str = "") -> str:
    """
    Perform file operations like read, write, list, and delete.

    Args:
        operation (str): The operation to perform (list, read, write, delete).
        filename (str, optional): Name of the file.
        content (str, optional): Content to write.

    Returns:
        str: A JSON string with the operation result or an error message.
    """
    # ... (Implementation for file operations) ...
```

### 2. Set Up Your AI Provider and Model Interface

Configure the connection to your chosen AI provider (currently DeepInfra and Sambanova are supported):

```python
# example_usage.py

from function_caller.AI_providers.deepinfra import DeepInfraAPI
# from function_caller.AI_providers.sambanova import SambanovaAPI  # Uncomment to use Sambanova

# DeepInfra (replace with your preferred provider)
model_interface = DeepInfraAPI() 

# Sambanova (ensure you have set the SAMBANOVA_API_KEY in your environment)
# model_interface = SambanovaAPI()
```
**Note:** For Sambanova, you will need to set your API key in an `.env` file like this:

```
SAMBANOVA_API_KEY=your_sambanova_api_key_here
```

### 3. Create and Configure Your Assistant

Instantiate the `Assistant` with your tools, model interface, and other settings:

```python
from function_caller.assistant import Assistant
from example_tools import get_weather, file_operations

tools = {
    "get_weather": get_weather,
    "file_operations": file_operations,
}

assistant = Assistant(
    model_interface=model_interface,
    tools=tools,
    use_native_function_calling=False, # Set to True if your model has native support
    name="MyAssistant",
    system_prompt="You are a helpful AI assistant...",  # Customize as needed
    save_history=True,
    history_dir='history',
    log_to_file=True,
    log_to_console=True
)
```

### 4. Interact with Your Assistant

Start a conversation and let your assistant handle user messages:

```python
if __name__ == "__main__":
    while True:
        user_message = input("You: ")
        response = assistant.handle_message(user_message)
        print(f"Assistant: {response}")
```

### 5. Example Interaction
```
You: What's the weather in London?
Assistant: [{"tool_name": "get_weather", "tool_input": {"city": "London"}}] 
You: The 'get_weather' function was called with the provided input and returned the following result: {"status": "success", "location": "London", "country": "United Kingdom", "temperature": "12°C", "humidity": "80%", "wind_speed": "15 km/h", "message": "Current weather in London, United Kingdom"}. Now, provide a natural language response based on this result.
Assistant: The current weather in London, United Kingdom is 12°C with 80% humidity and a wind speed of 15 km/h.
```

## ⚙️ Advanced Configuration

### Customizing the System Prompt

You can tailor the assistant's behavior and personality by modifying the `system_prompt`:

```python
DEFAULT_SYSTEM_PROMPT = """
## Core Instructions for {name} AI System

**Primary Directive:** You are {name}, an AI assistant focused on function calling and direct responses.

# ... (rest of the prompt) ...
"""

assistant = Assistant(
    # ... other settings ...
    system_prompt=DEFAULT_SYSTEM_PROMPT
)
```
There are other prompts available in `function_caller/prompts/default_prompt.py` file which you can use.

### Managing Conversation History

The `HistoryManager` automatically saves conversations to a JSON file. You can customize this:

```python
assistant = Assistant(
    # ... other settings ...
    save_history=False,  # Disable history saving
    history_dir='my_history_folder'  # Change the directory
)
```

### Logging

Control logging verbosity and output:

```python
assistant = Assistant(
    # ... other settings ...
    log_to_file=False,  # Disable file logging
    log_to_console=False  # Disable console logging
)
```

## 🤝 Contributing

Contributions are welcome! Please read our [CONTRIBUTING.md](CONTRIBUTING.md) (you'll need to create this file) for guidelines on how to contribute.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

*   Thanks to the developers of the AI models that inspire and power this project.
*   Special thanks to all contributors who help improve Function Caller.

## 📞 Contact

For questions, issues, or suggestions, please open an issue on the [GitHub repository](https://github.com/SreejanPersonal/function_caller).

---

**Let Function Caller empower your AI models to interact with the world like never before!** 🚀