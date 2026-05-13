from abc import ABC, abstractmethod
from .entities import Message

class IAIProvider(ABC):
    @abstractmethod
    async def generate_response(self, prompt: str) -> str: ...

class IMessageRepository(ABC):
    @abstractmethod
    async def save(self, message: Message) -> None: ...