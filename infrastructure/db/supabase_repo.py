from domain.ports import IMessageRepository
from core.config import settings
from supabase import create_client, Client

class SupabaseMessageRepository(IMessageRepository):
    def __init__(self):
        self.supabase_url = settings.supabase_url
        self.supabase_key = settings.supabase_key
        self.table = settings.supabase_table
        self.client: Client = create_client(self.supabase_url, self.supabase_key)
        print(f"✅ SupabaseMessageRepository initialized (table: {self.table})")

    async def save(self, user_id: int, username: str, message_text: str, ai_response: str = None) -> int:
        data = {
            "user_id": user_id,
            "username": username,
            "message_text": message_text,
            "ai_response": ai_response,
            "created_at": None
        }
        result = self.client.table(self.table).insert(data).execute()
        msg_id = result.data[0]["id"] if result.data else None
        print(f"💾 SAVED to Supabase: ID={msg_id}")
        return msg_id
