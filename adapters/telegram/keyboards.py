from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_help_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для /help"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="📖 Как использовать", callback_data="help_usage"),
        InlineKeyboardButton(text="🤖 О боте", callback_data="help_about")
    )
    builder.row(
        InlineKeyboardButton(text="📊 Статистика", callback_data="stats")
    )
    return builder.as_markup()

def get_ai_mode_keyboard() -> InlineKeyboardMarkup:
    """Кнопки переключения режимов AI"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🧠 Творческий режим", callback_data="mode_creative"),
        InlineKeyboardButton(text="🎯 Точный режим", callback_data="mode_precise")
    )
    return builder.as_markup()