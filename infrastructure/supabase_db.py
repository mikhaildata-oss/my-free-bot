import os
import logging
from typing import Optional
from supabase import create_client, Client
from domain.entities import Message, User
from domain.ports import IMessageRepository

logger = logging.getLogger(__name__)

class SupabaseMessageRepository(IMessageRepository):
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        self.table = os.getenv("SUPABASE_TABLE", "messages")
        
        if not self.url or not self.key:
            logger.warning("⚠️ Supabase credentials not found, using mock repository")
            self.client = None
        else:
            try:
                self.client: Client = create_client(self.url, self.key)
                logger.info(f"✅ Supabase connected (table: {self.table})")
            except Exception as e:
                logger.error(f"❌ Supabase connection failed: {e}")
                self.client = None

    async def save_message(self, message: Message) -> Optional[str]:
        if not self.client:
            logger.warning("⚠️ Supabase not connected, message not saved")
            return None
        
        try:
            data = {
                "user_id": message.user.id,
                "username": message.user.username or "unknown",
                "message_text": message.text,
                "created_at": message.timestamp.isoformat()
            }
            result = self.client.table(self.table).insert(data).execute()
            logger.info(f"💾 Message saved: {result.data[0]['id']}")
            return result.data[0]['id']
        except Exception as e:
            logger.error(f"❌ Failed to save message: {e}")
            return None

    async def get_total_count(self) -> int:
        if not self.client:
            return 0
        try:
            result = self.client.table(self.table).select("*", count="exact").execute()
            return result.count
        except Exception as e:
            logger.error(f"❌ Failed to get count: {e}")
            return 0

    async def get_user_message_count(self, user_id: int) -> int:
        if not self.client:
            return 0
        try:
            result = self.client.table(self.table).select("*", count="exact").eq("user_id", user_id).execute()
            return result.count
        except Exception as e:
            logger.error(f"❌ Failed to get user count: {e}")
            return 0