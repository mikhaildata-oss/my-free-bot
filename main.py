# coding: utf-8
import os
import sys
import logging
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

# 🔥 Загружаем .env ВСЕГДА, с явным путём
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)
logging.info(f"✅ .env loaded from: {env_path.resolve()}")

# Проверяем токен сразу
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    logging.error("❌ BOT_TOKEN not found! Check .env file")
    sys.exit(1)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", stream=sys.stdout)

# Infrastructure
from infrastructure.groq_ai import GroqAIAdapter
from infrastructure.supabase_db import SupabaseMessageRepository
from infrastructure.error_handler import ErrorHandlingMiddleware
from application.services import ApplicationServices
from adapters.telegram.handlers import register_handlers

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info(" Bootstrapping bot with Clean Architecture...")
    yield
    await bot.session.close()
    logging.info("🛑 Bot stopped")

app = FastAPI(lifespan=lifespan)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# === Dependency Injection ===
ai_adapter = GroqAIAdapter()
db_repository = SupabaseMessageRepository()
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
@app.head("/health")  # ← ЯВНЫЙ HEAD для UptimeRobot
async def health():
    return JSONResponse({"status": "ok", "architecture": "Clean/Hexagonal"})

@app.get("/")
async def root():
    return {"message": "Bot is running"}

@app.on_event("startup")
async def setup():
    webhook_url = os.getenv("WEBHOOK_URL")
    if webhook_url:
        await bot.set_webhook(webhook_url)
    logging.info("✅ Webhook configured")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)