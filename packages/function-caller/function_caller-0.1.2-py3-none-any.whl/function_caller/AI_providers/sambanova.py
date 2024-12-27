# models/sambanova.py

import requests
from typing import List, Dict, Union
import os
from dotenv import load_dotenv
load_dotenv()

class SambanovaAPI:
    API_URL = "https://api.sambanova.ai/v1/chat/completions"
    HEADERS = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('SAMBANOVA_API_KEY')}"
    }

    def generate(
        self,
        messages: List[Dict[str, str]],
        model: str = "Meta-Llama-3.1-70B-Instruct",
        temperature: float = 0.7,
        max_tokens: int = 2000,
        disable_function_calls: bool = False
    ) -> str:
        
        payload = {
            "messages": messages,
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "functions": [] if disable_function_calls else None
        }

        response = requests.post(
            self.API_URL,
            headers=self.HEADERS,
            json=payload
        )

        json_response = response.json()
        return json_response['choices'][0]['message']['content']