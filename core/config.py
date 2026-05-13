import os
from enum import Enum
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class AIProvider(str, Enum):
    GROQ = "groq"
    OLLAMA = "ollama"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).parent.parent / ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )
    
    # AI
    ai_provider: AIProvider = AIProvider.GROQ
    groq_api_key: str = ""
    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "llama3.1:8b"
    
    # Supabase
    supabase_url: str = ""
    supabase_key: str = ""
    supabase_table: str = "messages"

settings = Settings()

# Для отладки: раскомментируй, чтобы видеть, что загрузилось
# print(f"🔍 DEBUG: supabase_url={settings.supabase_url[:20] if settings.supabase_url else 'EMPTY'}...")
