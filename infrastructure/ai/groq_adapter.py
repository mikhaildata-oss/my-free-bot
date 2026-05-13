import os
from groq import Groq
from domain.ports import IAIAdapter
from domain.entities import Message

class GroqAdapter(IAIAdapter):
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY", "")
        if not api_key:
            raise ValueError("GROQ_API_KEY not set")
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.1-8b-instant"
        print(f"✅ GroqAdapter initialized (model: {self.model})")

    def get_model_name(self) -> str:
        return self.model

    async def generate_response(self, message: Message, history: list = None) -> str:
        messages = [{"role": "user", "content": message.text}]
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
