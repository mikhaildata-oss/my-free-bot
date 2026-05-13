from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Message:
    """
    Entity: Сообщение пользователя (чистая архитектура — ядро домена).
    """
    user_id: int
    text: str
    username: str = "unknown"
    message_id: int | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)
