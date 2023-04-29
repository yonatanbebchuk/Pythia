from abc import ABC, abstractmethod
from dataclasses import field, dataclass
from typing import Dict, List


@dataclass
class ChatRecord:
    messages: List[Dict[str, str]] = field(default_factory=list)

    def extend(self, record: "ChatRecord"):
        self.messages.extend(record.messages)

    def __str__(self):
        chat_record = str()
        for message in self.messages:
            chat_record += f"[{message['role']}]: {message['content']}\n"
        return chat_record


class IChat(ABC):

    @abstractmethod
    def query(self, prompt: str) -> ChatRecord:
        raise NotImplementedError()
