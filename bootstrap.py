import os
from core.config import settings, AIProvider
from infrastructure.ai.groq_adapter import GroqAdapter
from infrastructure.ai.ollama_adapter import OllamaAdapter
from infrastructure.db.supabase_repo import SupabaseMessageRepository
from domain.ports import IAIAdapter, IMessageRepository

def init_ai_adapter() -> IAIAdapter:
    match settings.ai_provider:
        case AIProvider.OLLAMA:
            print("🔧 AI Provider: Ollama (Local)")
            return OllamaAdapter()
        case _:
            print("🚀 AI Provider: Groq (Production)")
            return GroqAdapter()

def init_message_repo() -> IMessageRepository:
    print("🗄️ Message Repository: Supabase")
    return SupabaseMessageRepository()
