
# coding: utf-8
import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

if not BOT_TOKEN:
    raise ValueError("❌ Укажи BOT_TOKEN в переменных окружения Render")

storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=storage)

# === Обработчики ===
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("✅ <b>Бот работает на хостинге!</b>\nНапиши что-нибудь — я повторю.", parse_mode="HTML")

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer("📖 <b>Справка</b>:\n/start — перезапуск", parse_mode="HTML")

@dp.message()
async def echo(message: types.Message):
    if message.text and not message.from_user.is_bot:
        await message.answer(f"💬 <i>Эхо:</i> <code>{message.text}</code>", parse_mode="HTML")

# === Lifespan (вместо устаревшего on_event) ===
@asynccontextmanager
async def lifespan(app: FastAPI):
    if WEBHOOK_URL:
        await bot.set_webhook(WEBHOOK_URL)
        logging.info(f"✅ Webhook: {WEBHOOK_URL}")
    yield
    await bot.session.close()
    if WEBHOOK_URL:
        await bot.delete_webhook()

app = FastAPI(lifespan=lifespan)

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    update = types.Update.model_validate(data, context={"bot": bot})
    await dp.feed_webhook_update(bot, update)
    return {"ok": True}

@app.get("/health")
async def health():
    return {"status": "ok"}