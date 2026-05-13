from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from . import keyboards
from application.services import ApplicationServices
from domain.entities import User, Message

router = Router()

def register_handlers(dp: Router, services: ApplicationServices):
    
    @dp.message(Command("start"))
    async def cmd_start(msg: Message):
        await msg.answer(
            "🤖 <b>AI-бот запущен!</b>\n"
            "Напиши что угодно — отвечу через Llama 3.1.\n"
            "Используй /help для меню",
            parse_mode="HTML"
        )

    @dp.message(Command("help"))
    async def cmd_help(msg: Message):
        await msg.answer(
            "📖 <b>Справка:</b>\n"
            "/start — Рестарт\n"
            "/stats — Статистика\n"
            "Просто напиши сообщение для AI",
            reply_markup=keyboards.get_help_keyboard(),
            parse_mode="HTML"
        )

    @dp.message(Command("stats"))
    async def cmd_stats(msg: Message):
        stats = await services.get_stats.execute(msg.from_user.id)
        await msg.answer(
            f"📊 <b>Статистика:</b>\n"
            f"Всего сообщений: {stats['total_messages']}\n"
            f"Ваши сообщения: {stats['user_messages']}\n"
            f"Статус: {stats['status']}",
            parse_mode="HTML"
        )

    @dp.callback_query(F.data == "help_usage")
    async def help_usage(callback: CallbackQuery):
        await callback.answer("Просто напиши сообщение — я отвечу через AI!", show_alert=True)

    @dp.callback_query(F.data == "help_about")
    async def help_about(callback: CallbackQuery):
        await callback.answer("Бот на Llama 3.1 (Groq). Бесплатно и быстро!", show_alert=True)

    @dp.callback_query(F.data == "stats")
    async def inline_stats(callback: CallbackQuery):
        stats = await services.get_stats.execute(callback.from_user.id)
        await callback.message.answer(
            f"📊 Сообщений: {stats['total_messages']}"
        )
        await callback.answer()

    @dp.message(F.text)
    async def handle_ai(msg: Message):
        user = User(
            id=msg.from_user.id,
            username=msg.from_user.username,
            first_name=msg.from_user.first_name
        )
        domain_msg = Message(user=user, text=msg.text)
        
        response = await services.process_message.execute(domain_msg)
        await msg.answer(response)