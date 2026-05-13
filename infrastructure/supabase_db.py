import os
import sys
from typing import Optional
from datetime import datetime, timezone
from supabase import create_client, Client
from domain.entities import Message
from domain.ports import IMessageRepository

class SupabaseMessageRepository(IMessageRepository):
    def __init__(self):
        self.client = None
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        self.table = os.getenv("SUPABASE_TABLE", "messages")
        
        if url and key:
            self.client = create_client(url, key)
            print("✅ Supabase client created", flush=True)

    async def save(self, message: Message) -> Optional[str]:
        print(f"💾 SAVE_START", flush=True)
        
        if not self.client: 
            print("❌ NO_CLIENT", flush=True)
            return None
        
        # 🔥 Безопасный timestamp
        ts = message.timestamp
        if ts is None:
            ts = datetime.now(timezone.utc)
        ts_str = ts.isoformat()
        
        data = {
            "user_id": message.user.id,
            "username": message.user.username or "unknown",
            "message_text": message.text,
            "created_at": ts_str
        }
        
        print(f"📦 INSERT_DATA: {data}", flush=True)
        
        # 🔥 ПРЯМАЯ ВСТАВКА БЕЗ try-except (чтобы видеть ошибку в логах Render)
        result = self.client.table(self.table).insert(data).execute()
        
        msg_id = result.data[0]['id']
        print(f"💚 SAVED_ID: {msg_id}", flush=True)
        return msg_id

    async def get_total_count(self) -> int: return 0
    async def get_user_message_count(self, user_id: int) -> int: return 0