# function_caller/model_interface.py

from abc import ABC, abstractmethod
from typing import List, Dict

class ModelInterface(ABC):
    @abstractmethod
    def generate(self, messages: List[Dict[str, str]]) -> str:
        pass