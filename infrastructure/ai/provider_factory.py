import os
from infrastructure.ai.groq_adapter import GroqAdapter
from infrastructure.ai.ollama_adapter import OllamaAdapter

def get_ai_provider():
    provider = os.getenv("AI_PROVIDER", "prod").lower()
    if provider == "local":
        print("🔧 AI Provider: Ollama (Local)")
        return OllamaAdapter()
    print("🚀 AI Provider: Groq (Production)")
    return GroqAdapter()
