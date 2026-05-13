import os
import logging
from groq import AsyncGroq
from domain.ports import IAIProvider

logger = logging.getLogger(__name__)

class GroqAIAdapter(IAIProvider):
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            logger.error("❌ GROQ_API_KEY not found in environment!")
        self.client = AsyncGroq(api_key=api_key)
        self.model = "llama-3.1-8b-instant"  # ← ПРАВИЛЬНАЯ МОДЕЛЬ
        logger.info(f"✅ GroqAIAdapter initialized (model: {self.model})")

    async def generate_response(self, prompt: str) -> str:
        try:
            logger.info(f"🤖 Sending to Groq: {prompt[:50]}...")
            chat = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=512
            )
            response = chat.choices[0].message.content
            logger.info(f"✅ Groq response received: {response[:50]}...")
            return response or "❌ Пустой ответ от AI"
            
        except Exception as e:
            logger.error(f"💥 Groq API ERROR: {type(e).__name__}: {str(e)}")
            return "⚠️ Сейчас я не могу ответить. Попробуй через минуту."   