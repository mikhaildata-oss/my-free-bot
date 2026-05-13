# coding: utf-8
import sys
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from . import keyboards
from application.services import ApplicationServices
from domain.entities import User as DomainUser, Message as DomainMessage

router = Router()

def register_handlers(dp: Router, services: ApplicationServices):
    
    @dp.message(Command("start"))
    async def cmd_start(msg: Message):
        await msg.answer("🤖 <b>AI-бот запущен!</b>\nНапиши что угодно...", parse_mode="HTML")

    @dp.message(Command("help"))
    async def cmd_help(msg: Message):
        await msg.answer("📖 <b>Справка:</b>\n/start — Рестарт\n/stats — Статистика", reply_markup=keyboards.get_help_keyboard(), parse_mode="HTML")

    @dp.message(Command("stats"))
    async def cmd_stats(msg: Message):
        stats = await services.get_stats.execute(msg.from_user.id)
        await msg.answer(f"📊 <b>Статистика:</b>\nВсего: {stats['total_messages']}\nВаши: {stats['user_messages']}", parse_mode="HTML")

    @dp.message(F.text)
    async def handle_ai(msg: Message):
        print(f"🚨 HANDLER: text='{msg.text[:20]}'", flush=True)
        
        user = DomainUser(
            id=msg.from_user.id,
            username=msg.from_user.username,
            first_name=msg.from_user.first_name
        )
        domain_msg = DomainMessage(
            user=user,
            text=msg.text
        )
        
        print(f"🚨 CALLING execute...", flush=True)
        response = await services.process_message.execute(domain_msg)
        print(f"🚨 GOT RESPONSE", flush=True)
        await msg.answer(response)