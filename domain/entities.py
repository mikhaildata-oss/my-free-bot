from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

@dataclass
class User:
    id: int
    username: str | None
    first_name: str

@dataclass
class Message:
    id: str = str(uuid4())
    user: User
    text: str
    timestamp: datetime = datetime.utcnow()