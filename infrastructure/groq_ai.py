import os
from groq import AsyncGroq
from ..domain.ports import IAIProvider

class GroqAIAdapter(IAIProvider):
    def __init__(self):
        self.client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = os.getenv("AI_MODEL", "llama-3.1-8b-instant")

    async def generate_response(self, prompt: str) -> str:
        try:
            chat = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=512
            )
            return chat.choices[0].message.content or "❌ Пустой ответ от AI"
        except Exception as e:
            # Логируем, но не ломаем поток
            print(f" AI Error: {e}")
            return "⚠️ Сейчас я не могу ответить. Попробуй через минуту."