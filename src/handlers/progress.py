from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from src.loader import dp
from src.db import DatabaseManager
from src.keyboards import get_back_to_main_button, get_main_keyboard
from src.handlers.states import WeightState

@dp.message(F.text == "📊 Прогресс")
async def progress_tracking(message: types.Message):
    user = await DatabaseManager.get_user(message.from_user.id)
    if not user:
        await message.answer("📊 *Прогресс*\n\nСначала заполни профиль в разделе Питание!",
                             parse_mode="Markdown", reply_markup=get_back_to_main_button())
        return
    weight_history = await DatabaseManager.get_weight_history(message.from_user.id, days=30)
    if weight_history:
        weights = [entry.weight for entry in weight_history[-7:]]
        dates = [entry.date.strftime("%d.%m") for entry in weight_history[-7:]]
        progress_text = "*📊 ТВОЙ ПРОГРЕСС*\n\n"
        progress_text += f"*Текущий вес:* {user.weight} кг\n"
        progress_text += f"*Цель:* {user.goal}\n"
        progress_text += f"*Дневная норма:* {user.daily_calories} ккал\n\n"
        progress_text += "*Последние измерения:*\n"
        for date, weight in zip(dates, weights):
            progress_text += f"• {date}: {weight} кг\n"
        if len(weights) >= 2:
            change = weights[-1] - weights[0]
            if change < 0:
                progress_text += f"\n✅ Потеряно: {abs(change):.1f} кг"
            elif change > 0:
                progress_text += f"\n⚠️ Набрано: {change:.1f} кг"
            else:
                progress_text += f"\n➡️ Вес стабилен"
    else:
        progress_text = "*📊 ТВОЙ ПРОГРЕСС*\n\n"
        progress_text += f"*Текущий вес:* {user.weight} кг\n"
        progress_text += f"*Цель:* {user.goal}\n"
        progress_text += f"*Дневная норма:* {user.daily_calories} ккал\n\n"
        progress_text += "Пока нет истории измерений. Добавь вес в разделе Питание!"
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Добавить вес", callback_data="add_weight")],
        [InlineKeyboardButton(text="◀ Назад", callback_data="back_to_main")]
    ])
    await message.answer(progress_text, parse_mode=None, reply_markup=kb)

@dp.callback_query(F.data == "add_weight")
async def add_weight_start(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("📊 Введи текущий вес (в кг):\n\nНапример: 75.5")
    await state.set_state(WeightState.waiting_for_weight)

@dp.message(WeightState.waiting_for_weight)
async def process_add_weight(message: types.Message, state: FSMContext):
    try:
        weight = float(message.text.replace(',', '.'))
        if weight < 30 or weight > 250:
            await message.answer("⚠️ Вес должен быть от 30 до 250 кг. Попробуй еще раз:")
            return
        await DatabaseManager.add_weight_entry(message.from_user.id, weight)
        keyboard = await get_main_keyboard(message.from_user.id)
        await message.answer(f"✅ Вес {weight} кг сохранен!", reply_markup=keyboard)
        await state.clear()
    except ValueError:
        await message.answer("⚠️ Пожалуйста, введи число (например: 75.5)")