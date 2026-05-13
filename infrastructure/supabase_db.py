import os
import traceback
from typing import Optional
from pathlib import Path
from supabase import create_client, Client
from domain.entities import Message
from domain.ports import IMessageRepository

# 🔥 Лог-файл для ВСЕХ ошибок
ERROR_LOG = Path(__file__).parent.parent.parent / "save_errors.log"

class SupabaseMessageRepository(IMessageRepository):
    def __init__(self):
        self.client = None
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        self.table = os.getenv("SUPABASE_TABLE", "messages")
        if url and key:
            try:
                self.client = create_client(url, key)
                with open(ERROR_LOG, "a", encoding="utf-8") as f:
                    f.write("✅ Supabase client created\n")
            except Exception as e:
                with open(ERROR_LOG, "a", encoding="utf-8") as f:
                    f.write(f"❌ Client init failed: {e}\n{traceback.format_exc()}\n")

    async def save(self, message: Message) -> Optional[str]:
        with open(ERROR_LOG, "a", encoding="utf-8") as f:
            f.write(f"\n🔥 save() called: user={message.user.id}, text='{message.text[:30]}'\n")
        
        if not self.client:
            with open(ERROR_LOG, "a", encoding="utf-8") as f:
                f.write("⚠️ No client\n")
            return None
        
        try:
            data = {
                "user_id": message.user.id,
                "username": message.user.username or "unknown",
                "message_text": message.text,
                "created_at": message.timestamp.isoformat()
            }
            with open(ERROR_LOG, "a", encoding="utf-8") as f:
                f.write(f"🔄 Inserting: {data}\n")
            
            result = self.client.table(self.table).insert(data).execute()
            msg_id = result.data[0]['id']
            
            with open(ERROR_LOG, "a", encoding="utf-8") as f:
                f.write(f"💚 SAVED: {msg_id}\n")
            return msg_id
            
        except Exception as e:
            with open(ERROR_LOG, "a", encoding="utf-8") as f:
                f.write(f"❌ SAVE FAILED: {type(e).__name__}: {e}\n")
                f.write(f"📋 TRACEBACK:\n{traceback.format_exc()}\n")
                if hasattr(e, 'response') and e.response:
                    f.write(f"🌐 Response: {e.response.text}\n")
            return None

    async def get_total_count(self) -> int: return 0
    async def get_user_message_count(self, user_id: int) -> int: return 0