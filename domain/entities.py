# domain/entities.py
from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

@dataclass
class User:
    id: int
    username: str | None
    first_name: str

@dataclass
class Message:
    # Сначала поля БЕЗ default (обязательные)
    user: User
    text: str
    
    # Потом поля С default (опциональные)
    id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = field(default_factory=datetime.utcnow)