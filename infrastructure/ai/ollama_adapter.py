import os
import httpx
from domain.ports import IAIAdapter
from domain.entities import Message

class OllamaAdapter(IAIAdapter):
    def __init__(self):
        self.host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.model = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
        print(f"✅ OllamaAdapter initialized (model: {self.model})")

    async def generate_response(self, user_message: Message, history: list) -> str:
        messages = [{"role": "system", "content": "Ты полезный ассистент. Отвечай кратко и по делу."}]
        
        # Берём последние 5 сообщений из истории для контекста
        for msg in history[-5:]:
            messages.append({"role": msg.get("role", "user"), "content": msg.get("content", "")})
            
        messages.append({"role": "user", "content": user_message.text})

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {"temperature": 0.7}
        }

        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(f"{self.host}/api/chat", json=payload)
            resp.raise_for_status()
            return resp.json()["message"]["content"].strip()

    def get_model_name(self) -> str:
        return self.model