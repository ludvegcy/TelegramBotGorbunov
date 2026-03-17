from aiogram import types
from aiogram.filters import CommandStart
from src.loader import dp
from src.keyboards import get_main_keyboard

@dp.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    keyboard = await get_main_keyboard(message.from_user.id)
    await message.answer(
        f"Привет, {message.from_user.full_name}! 👋\n"
        "Это **Фитнес-бот** — твой персональный гид в мире спорта и здоровья.\n\n"
        "🔥 Что ты узнаешь с нами:\n"
        "• Правильную технику упражнений (с фото!) 📸\n"
        "• Какие БАДы и для чего принимать 💊\n"
        "• Информацию по ААС и фармакологии 🧪\n"
        "• Как следить за анализами и вести дневник 📋\n"
        "• Персональные программы от наших тренеров 👨‍🏫\n\n"
        "👇 Выбери раздел в меню и начни свой путь к идеальному телу!\n\n"
        "⚠️ИЗ-ЗА БЛОКИРОВКИ ТЕЛЕГРАММ БОТ МОЖЕТ РАБОТАТЬ МЕДЛЕННО⚠️",
        parse_mode="Markdown",
        reply_markup=keyboard
    )