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

@dp.message(F.text == "📝 Памятки")
async def notes_menu(message: types.Message):
    text = ("*📌 ОСНОВНЫЕ ПРИНЦИПЫ ФИТНЕСА*\n\n"
            "1️⃣ *Сплит-тренировки:* Разделяй группы мышц по дням.\n"
            "2️⃣ *Начинай с базы:* Сначала сложные упражнения (жимы, тяги), потом изолирующие.\n"
            "3️⃣ *Питание:* Дефицит калорий для похудения, профицит - для набора массы.\n"
            "4️⃣ *Вода:* Пей 30-40 мл на кг веса (2-3 литра в день).\n"
            "5️⃣ *Сон:* 7-8 часов - основа восстановления.\n"
            "6️⃣ *Прогрессия нагрузок:* Каждую тренировку старайся делать чуть больше.")
    await message.answer(text, parse_mode="Markdown", reply_markup=get_back_to_main_button())