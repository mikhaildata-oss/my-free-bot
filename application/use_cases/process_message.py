from domain.ports import IAIProvider, IMessageRepository
from domain.entities import Message
class ProcessMessageUseCase:
    def __init__(self, ai: IAIProvider, repo: IMessageRepository):
        self.ai = ai
        self.repo = repo

    async def execute(self, message: Message) -> str:
        # 1. Сохраняем входящее (в следующем шаге подключим Supabase)
        await self.repo.save(message)
        
        # 2. Генерируем AI-ответ
        response = await self.ai.generate_response(message.text)
        return response