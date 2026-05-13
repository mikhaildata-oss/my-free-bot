from core.config import settings
print(f"AI Provider: {settings.ai_provider}")
print(f"Supabase URL: '{settings.supabase_url}'")
print(f"Supabase Key: '{settings.supabase_key[:15] if settings.supabase_key else 'EMPTY'}...'")
