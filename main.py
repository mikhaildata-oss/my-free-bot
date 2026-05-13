import os, logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types  # ← убедись, что types здесь есть
from aiogram.fsm.storage.memory import MemoryStorage

# Infrastructure
from infrastructure.groq_ai import GroqAIAdapter
from infrastructure.supabase_db import SupabaseMessageRepository
from infrastructure.error_handler import ErrorHandlingMiddleware
from application.services import ApplicationServices
from adapters.telegram.handlers import register_handlers

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("🚀 Bootstrapping bot with Clean Architecture...")
    yield
    await bot.session.close()
    logging.info("🛑 Bot stopped")

app = FastAPI(lifespan=lifespan)
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(storage=MemoryStorage())

# === Dependency Injection ===
ai_adapter = GroqAIAdapter()
db_repository = SupabaseMessageRepository()  # пока заглушка
services = ApplicationServices(ai=ai_adapter, repo=db_repository)

# === Middleware ===
dp.update.middleware(ErrorHandlingMiddleware())

# === Handlers ===
register_handlers(dp, services)

# === Webhook ===
@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    update = types.Update.model_validate(data, context={"bot": bot})
    await dp.feed_webhook_update(bot, update)
    return {"ok": True}

@app.get("/health")
async def health():
    return {"status": "ok", "architecture": "Clean/Hexagonal"}

@app.on_event("startup")
async def setup():
    if os.getenv("WEBHOOK_URL"):
        await bot.set_webhook(os.getenv("WEBHOOK_URL"))
    logging.info("✅ Webhook configured")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))