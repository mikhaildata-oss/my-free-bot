import sys
from domain.ports import IAIProvider, IMessageRepository
from domain.entities import Message

class ProcessMessageUseCase:
    def __init__(self, ai: IAIProvider, repo: IMessageRepository):
        self.ai = ai
        self.repo = repo

    async def execute(self, message: Message) -> str:
        # 🔥 ЛОГ 4: ВХОД В ЮЗКЕЙС
        print(f"🚨 USE_CASE_EXECUTE: text='{message.text[:20]}...'", flush=True)
        
        # 🔥 ЛОГ 5: ПЕРЕД СОХРАНЕНИЕМ
        print(f"🚨 CALLING repo.save()...", flush=True)
        
        # Пробуем сохранить
        await self.repo.save(message)
        
        print(f"🚨 AFTER repo.save()", flush=True)
        
        return await self.ai.generate_response(message.text)