from aiogram import types, F
from src.loader import dp
from src.keyboards import get_back_to_main_button

@dp.message(F.text == "🛒 Наш бренд")
async def brand_info(message: types.Message):
    text = ("*👕 НАШ БРЕНД ОДЕЖДЫ*\n\n"
            "🚀 Скоро мы представим линейку спортивной одежды и аксессуаров.\n"
            "🔥 Следите за обновлениями!\n\n"
            "А пока - тренируйся в том, что есть! 💪")
    await message.answer(text, parse_mode="Markdown", reply_markup=get_back_to_main_button())