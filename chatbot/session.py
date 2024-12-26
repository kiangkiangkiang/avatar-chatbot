from typing import Dict


class UserData:
    def __init__(self):
        self.chat_memory = []
        self.max_memory = 10

    def append_memory(self, role: str, content: str):
        if len(self.chat_memory) > 10:
            self.chat_memory.pop(1)

        self.chat_memory.append({"role": role, "content": content})


sessions: Dict[str, UserData] = {}  # User ID: User Data
