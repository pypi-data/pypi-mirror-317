# function_caller/tools/sample_tools.py

import json
import requests

def get_weather(city: str) -> str:
    """Get current weather information for a city."""
    # Mock JSON response
    return json.dumps({"weather": "sunny and warm"})

# Add metadata for tool description and parameters
get_weather.description = "Get current weather information for a city."
get_weather.parameters = {
    "city": {"type": "string", "description": "Name of the city"}
}

def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """Convert amount from one currency to another."""
    # Mock JSON response
    converted_amount = amount * 2  # Mock conversion rate
    return json.dumps({
        "amount": amount,
        "from_currency": from_currency,
        "to_currency": to_currency,
        "converted_amount": converted_amount
    })

# Add metadata
convert_currency.description = "Convert amount from one currency to another."
convert_currency.parameters = {
    "amount": {"type": "number", "description": "Amount to convert"},
    "from_currency": {"type": "string", "description": "Source currency code (e.g., USD)"},
    "to_currency": {"type": "string", "description": "Target currency code (e.g., EUR)"}
}