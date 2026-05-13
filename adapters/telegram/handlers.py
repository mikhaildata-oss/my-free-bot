# coding: utf-8
from datetime import datetime, timezone
import os
from aiogram import Router, F
from aiogram.types import Message as TgMessage, CallbackQuery
from aiogram.filters import Command
from supabase import create_client
from . import keyboards
from application.services import ApplicationServices
from domain.entities import User as DomainUser, Message as DomainMessage

router = Router()

def register_handlers(dp: Router, services: ApplicationServices):
    
    @dp.message(Command("start"))
    async def cmd_start(msg: TgMessage):
        await msg.answer("🤖 <b>AI-бот запущен!</b>\nНапиши что угодно...", parse_mode="HTML")

    @dp.message(Command("help"))
    async def cmd_help(msg: TgMessage):
        await msg.answer("📖 <b>Справка:</b>\n/start — Рестарт\n/stats — Статистика", reply_markup=keyboards.get_help_keyboard(), parse_mode="HTML")

    @dp.message(Command("stats"))
    async def cmd_stats(msg: TgMessage):
        stats = await services.get_stats.execute(msg.from_user.id)
        await msg.answer(f"📊 <b>Статистика:</b>\nВсего: {stats['total_messages']}\nВаши: {stats['user_messages']}", parse_mode="HTML")

    @dp.message(F.text)
    async def handle_ai(msg: TgMessage):
        # 🔥 ШАГ 1: ГАРАНТИРОВАННАЯ ВСТАВКА (ПРЯМОЙ ЗАПРОС В БД)
        try:
            client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
            data = {
                "user_id": msg.from_user.id,
                "username": msg.from_user.username or "unknown",
                "message_text": msg.text,
                "created_at": datetime.now(timezone.utc).isoformat()
            }
            result = client.table("messages").insert(data).execute()
            print(f"💚 HARD_SAVE_OK: ID={result.data[0]['id']}", flush=True)
        except Exception as e:  # ← двоеточие обязательно!
            print(f"❌ HARD_SAVE_FAIL: {e}", flush=True)

        # 🔥 ШАГ 2: AI ОТВЕТ (через Clean Architecture)
        user = DomainUser(
            id=msg.from_user.id,
            username=msg.from_user.username,
            first_name=msg.from_user.first_name
        )
        domain_msg = DomainMessage(
            user=user,
            text=msg.text,
            timestamp=datetime.now(timezone.utc)
        )
        
        response = await services.process_message.execute(domain_msg)
        await msg.answer(response)