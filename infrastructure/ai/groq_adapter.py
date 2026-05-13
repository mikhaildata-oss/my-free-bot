from domain.ports import IAIAdapter
from domain.entities import Message

class GroqAdapter(IAIAdapter):
    """
    Stub GroqAdapter для локальной разработки.
    В продакшене здесь будет реальный вызов Groq API.
    """
    def __init__(self, api_key: str = ""):
        self.api_key = api_key
        self.model = "llama-3.1-8b-instant"
        print(f"✅ GroqAdapter initialized (model: {self.model})")

    async def generate_response(self, user_message: Message, history: list) -> str:
        # Заглушка: возвращает эхо-ответ
        return f"[Groq stub] Вы написали: {user_message.text}"

    def get_model_name(self) -> str:
        return self.model
