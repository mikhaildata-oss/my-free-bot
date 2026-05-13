# coding: utf-8
import os
import sys
from dotenv import load_dotenv
from supabase import create_client

# Загружаем .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
table = os.getenv("SUPABASE_TABLE", "messages")

print(f"🔑 URL: {url}")
print(f"🔑 Key starts with: {key[:10] if key else 'None'}...")
print(f"📦 Table: {table}")

if not url or not key:
    print("❌ Нет ключей в .env")
    sys.exit(1)

try:
    client = create_client(url, key)
    print("✅ Клиент создан")
    
    # Пробуем вставить тестовую запись
    test_data = {
        "user_id": 999999,
        "username": "debug_test",
        "message_text": "Прямой тест вставки",
        "created_at": "2026-05-14T00:00:00Z"
    }
    print(f"🔄 Вставляю: {test_data}")
    
    result = client.table(table).insert(test_data).execute()
    print(f"💚 УСПЕХ! Запись создана: {result.data}")
    
except Exception as e:
    print(f"❌ ОШИБКА: {type(e).__name__}")
    print(f"   Сообщение: {e}")
    if hasattr(e, 'response') and e.response:
        print(f"   Response: {e.response.text}")