import os
import asyncio
from groq import AsyncGroq
from dotenv import load_dotenv

load_dotenv()

async def main():
    api_key = os.getenv("GROQ_API_KEY")
    print(f"🔑 Ключ: {api_key[:10]}..." if api_key else "❌ Нет ключа")
    
    if not api_key:
        return
    
    client = AsyncGroq(api_key=api_key)
    try:
        print("🔄 Отправляю запрос к Llama 3.1...")
        response = await client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": "Скажи 'Работает'"}],
            max_tokens=20
        )
        print(f"✅ Ответ: {response.choices[0].message.content}")
    except Exception as e:
        print(f"❌ Ошибка: {type(e).__name__}: {e}")

if __name__ == "__main__":
    asyncio.run(main())