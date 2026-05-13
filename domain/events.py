from dataclasses import dataclass
from .entities import Message

@dataclass
class UserMessageReceived:
    message: Message

@dataclass
class AIResponseGenerated:
    message_id: str
    response_text: str