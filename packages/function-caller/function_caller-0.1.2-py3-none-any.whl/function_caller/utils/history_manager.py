# function_caller/utils/history_manager.py

import json
from pathlib import Path

class HistoryManager:
    def __init__(self, save_history: bool = True, history_dir: str = 'history'):
        self.save_history = save_history
        self.history_file = None

        self.current_conversation = {"messages": []}

        if self.save_history:
            # Ensure the history directory exists
            history_path = Path(history_dir)
            history_path.mkdir(parents=True, exist_ok=True)
            self.history_file = history_path / 'conversation_history.json'

            if self.history_file.exists():
                # Check if the file is empty before loading
                if self.history_file.stat().st_size == 0:
                    self.current_conversation = {"messages": []}
                else:
                    with open(self.history_file, 'r') as f:
                        self.current_conversation = json.load(f)
            else:
                self.current_conversation = {"messages": []}

    def add_message(self, message):
        self.current_conversation["messages"].append(message)
        if self.save_history and self.history_file:
            with open(self.history_file, 'w') as f:
                json.dump(self.current_conversation, f, indent=4)

    def get_current_messages(self):
        return self.current_conversation["messages"]

    def clear_current_conversation(self):
        self.current_conversation = {"messages": []}
        if self.save_history and self.history_file:
            with open(self.history_file, 'w') as f:
                json.dump(self.current_conversation, f, indent=4)