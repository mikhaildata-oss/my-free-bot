from ...domain.ports import IMessageRepository
from typing import Dict

class GetStatsUseCase:
    def __init__(self, repo: IMessageRepository):
        self.repo = repo

    async def execute(self, user_id: int) -> Dict[str, int]:
        # Пока заглушка — в следующем шаге подключим Supabase
        return {
            "total_messages": 0,
            "user_messages": 0,
            "status": "Bot is running"
        }