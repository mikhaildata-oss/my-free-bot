from abc import ABC, abstractmethod
from typing import List, Dict
from domain.entities import Message

class IAIAdapter(ABC):
    """
    Порт для AI-провайдера (порты и адаптеры / Hexagonal Architecture).
    Конкретные реализации: GroqAdapter, OllamaAdapter, etc.
    """
    @abstractmethod
    async def generate_response(self, user_message: Message, history: List[Dict]) -> str:
        """Генерирует ответ на сообщение пользователя с учётом истории."""
        pass

    @abstractmethod
    def get_model_name(self) -> str:
        """Возвращает название модели для логов/мониторинга."""
        pass


class IMessageRepository(ABC):
    """Порт для репозитория сообщений (работа с БД)."""
    @abstractmethod
    async def save(self, user_id: int, username: str, message_text: str) -> int:
        """Сохраняет сообщение и возвращает его ID."""
        pass
