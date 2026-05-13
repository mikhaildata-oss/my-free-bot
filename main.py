# coding: utf-8
import os
import sys
import logging
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    logging.error("❌ BOT_TOKEN not found!")
    sys.exit(1)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", stream=sys.stdout)

from infrastructure.groq_ai import GroqAIAdapter
from infrastructure.supabase_db import SupabaseMessageRepository
from application.services import ApplicationServices
from adapters.telegram.handlers import register_handlers

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("🚀 Bootstrapping bot...")
    yield
    await bot.session.close()

app = FastAPI(lifespan=lifespan)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

ai_adapter = GroqAIAdapter()
db_repository = SupabaseMessageRepository()
services = ApplicationServices(ai=ai_adapter, repo=db_repository)

register_handlers(dp, services)

@app.post("/webhook")
async def webhook(request: Request):
    print("🔥🔥🔥 WEBHOOK_HIT 🔥🔥🔥", flush=True)  # ← САМЫЙ ВЕРХ
    try:
        data = await request.json()
        print(f"📦 Webhook data keys: {list(data.keys())}", flush=True)
        if "message" in data:
            print(f"💬 Message text: {data['message'].get('text')}", flush=True)
        update = types.Update.model_validate(data, context={"bot": bot})
        await dp.feed_webhook_update(bot, update)
        print("✅ feed_webhook_update done", flush=True)
    except Exception as e:
        print(f"❌ Webhook error: {e}", flush=True)
    return {"ok": True}

@app.get("/health")
@app.head("/health")
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