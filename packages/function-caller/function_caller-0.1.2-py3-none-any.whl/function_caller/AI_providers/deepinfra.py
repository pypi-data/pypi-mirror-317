# models/deepinfra.py

import json
import requests
from typing import Union, List, Dict

class DeepInfraAPI:
    API_URL = "https://api.deepinfra.com/v1/openai/chat/completions"
    HEADERS = {
        "Accept": "text/event-stream",
        "Accept-Encoding": "gzip, deflate, br, zstd", 
        "Accept-Language": "en-US,en;q=0.9,hi;q=0.8",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Dnt": "1",
        "Host": "api.deepinfra.com",
        "Origin": "https://deepinfra.com",
        "Referer": "https://deepinfra.com/",
        "Sec-Ch-Ua": "\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty", 
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "X-Deepinfra-Source": "web-page",
    }

    def generate(
        self,
        conversation: Union[str, List[Dict[str, str]]],
        model: str = 'mistralai/Mixtral-8x22B-Instruct-v0.1',
        max_tokens: int = 512,
        temperature: float = 0.7,
        stream: bool = False,
        disable_function_calls: bool = False
        
    ) -> str:
        if isinstance(conversation, str):
            conversation = [{"role": "user", "content": conversation}]
        elif not isinstance(conversation, list):
            raise ValueError("Conversation must be either a string or a list of dictionaries")

        payload = {
            "model": model,
            "messages": conversation,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream
        }

        response = requests.post(
            self.API_URL,
            headers=self.HEADERS,
            json=payload
        )

        json_response = response.json()
        return json_response['choices'][0]['message']['content']
    

if __name__ == "__main__":
    api = DeepInfraAPI()
    response = api.generate("Hello, how are you?")
    print(response)