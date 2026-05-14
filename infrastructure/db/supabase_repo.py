from domain.ports import IMessageRepository
from core.config import settings
from supabase import create_client, Client
from datetime import datetime, timezone

class SupabaseMessageRepository(IMessageRepository):
    def __init__(self):
        self.client: Client = create_client(settings.supabase_url, settings.supabase_key)
        self.bot_id = -1
        print(f"✅ SupabaseMessageRepository initialized (bot_id: {self.bot_id})")

    async def save(self, user_id: int, username: str, message_text: str, ai_response: str = None, ai_generated_at: datetime = None) -> int:
        now = datetime.now(timezone.utc)
        
        # 1. Upsert пользователя
        self.client.table("users").upsert({
            "user_id": user_id,
            "username": username,
            "created_at": now.isoformat()
        }, on_conflict="user_id").execute()

        # 2. Вставка сообщения (явно передаём created_at, чтобы обойти NOT NULL)
        data = {
            "sender_id": user_id,
            "receiver_id": self.bot_id,
            "text": message_text,
            "ai_response": ai_response,
            "created_at": now.isoformat(),
            "ai_generated_at": ai_generated_at.isoformat() if ai_generated_at else now.isoformat()
        }
        result = self.client.table("messages").insert(data).execute()
        msg_id = result.data[0]["id"] if result.data else None
        print(f"💾 SAVED: msg_id={msg_id} | from={user_id} | created_at={now.isoformat()}")
        return msg_id
