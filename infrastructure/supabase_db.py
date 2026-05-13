import os
from ..domain.ports import IMessageRepository
from ..domain.entities import Message

class SupabaseMessageRepository(IMessageRepository):
    """
    Заглушка до подключения Supabase.
    В следующем шаге добавим:
    - from supabase import create_client
    - Реальное сохранение в БД
    """
    
    def __init__(self):
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
        # TODO: Инициализация клиента Supabase
        
    async def save(self, message: Message) -> None:
        # TODO: Реальное сохранение
        print(f"💾 Saving message {message.id} (placeholder)")
        pass