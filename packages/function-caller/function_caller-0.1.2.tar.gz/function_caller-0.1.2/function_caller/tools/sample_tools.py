# function_caller/tools/sample_tools.py

import json
import os
import requests
import psutil
import json

def get_weather(city: str) -> str:
    try:
        geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        geo_response = requests.get(geocoding_url)
        geo_data = geo_response.json()
        
        if not geo_data.get('results'):
            return json.dumps({
                "status": "error",
                "message": f"City '{city}' not found"
            })
            
        location = geo_data['results'][0]
        lat, lon = location['latitude'], location['longitude']
        
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m"
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()
        
        current = weather_data['current']
        
        return json.dumps({
            "status": "success",
            "location": location['name'],
            "country": location['country'],
            "temperature": f"{current['temperature_2m']}°C",
            "humidity": f"{current['relative_humidity_2m']}%",
            "wind_speed": f"{current['wind_speed_10m']} km/h",
            "message": f"Current weather in {location['name']}, {location['country']}"
        })
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": str(e)
        })
    
# Manual way to add metadata for tool description and parameters
get_weather.description = "Get current weather information for any city."
get_weather.parameters = {
    "city": {"type": "str", "description": "The city name, e.g. 'London'."}
}

def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    try:
        url = f"https://api.frankfurter.app/latest?from={from_currency.upper()}&to={to_currency.upper()}&amount={amount}"
        response = requests.get(url)
        data = response.json()
        converted = data['rates']
        return json.dumps({
            "status": "success",
            "converted_amount": converted,
            "message": f"Converted {amount} {from_currency} to {converted} {to_currency}"
        })
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": str(e)
        })

# Add metadata
convert_currency.description = "Convert amount from one currency to another."
convert_currency.parameters = {
    "amount": {"type": "number", "description": "Amount to convert"},
    "from_currency": {"type": "string", "description": "Source currency code (e.g., USD)"},
    "to_currency": {"type": "string", "description": "Target currency code (e.g., EUR)"}
}

def file_operations(operation: str, filename: str = "", content: str = "") -> str:
    """
    Perform file operations like read, write, list, and delete

    Args:
        operation (str): The operation to perform. Supported operations are:
            - list: List all files in the current directory.
            - read: Read the contents of a file.
            - write: Write content to a file.
            - delete: Delete a file.
        filename (str, optional): Name of the file to operate on.
        content (str, optional): Content to write (for write operation).

    Returns:
        A JSON string containing the result of the operation or an error message.
    """
    try:
        if operation == "list":
            files = os.listdir('.')
            return json.dumps({
                "status": "success",
                "files": files,
                "message": f"Found {len(files)} files in current directory"
            })
        elif operation == "read":
            with open(filename, 'r') as f:
                return json.dumps({
                    "status": "success",
                    "content": f.read(),
                    "message": f"File {filename} read successfully"
                })
        elif operation == "write":
            with open(filename, 'w') as f:
                f.write(content)
            return json.dumps({
                "status": "success",
                "message": f"Content written to {filename} successfully"
            })
        elif operation == "delete":
            os.remove(filename)
            return json.dumps({
                "status": "success",
                "message": f"File {filename} deleted successfully"
            })
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": str(e)
        })


def system_info(info_type: str) -> str:
    try:
        if info_type == "os":
            info = {
                "system": psutil.os.name,
                "platform": psutil.sys.platform,
                "processor": psutil.os.processor()
            }
        elif info_type == "memory":
            memory = psutil.virtual_memory()
            info = {
                "total": f"{memory.total / (1024**3):.2f} GB",
                "available": f"{memory.available / (1024**3):.2f} GB",
                "percent_used": f"{memory.percent}%"
            }
        elif info_type == "disk":
            disk = psutil.disk_usage('/')
            info = {
                "total": f"{disk.total / (1024**3):.2f} GB",
                "free": f"{disk.free / (1024**3):.2f} GB",
                "percent_used": f"{disk.percent}%"
            }
        return json.dumps({
            "status": "success",
            "info": info,
            "message": f"Retrieved {info_type} information successfully"
        })
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": str(e)
        })

def process_manager(action: str, process_name: str = None) -> str:
    try:
        if action == "list":
            processes = [p.name() for p in psutil.process_iter()]
            return json.dumps({
                "status": "success",
                "processes": processes[:10],
                "message": f"Listed top 10 of {len(processes)} running processes"
            })
        elif action == "find" and process_name:
            found = [p.info for p in psutil.process_iter(['name', 'pid']) 
                    if process_name.lower() in p.info['name'].lower()]
            return json.dumps({
                "status": "success",
                "found": found,
                "message": f"Found {len(found)} matching processes"
            })
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": str(e)
        })
    
process_manager.description = "Manage and monitor system processes"
process_manager.parameters = {
     "action": {"type": "string", "enum": ["list", "find"]},
     "process_name": {"type": "string", "description": "Name of process to find (for find action)"}
}