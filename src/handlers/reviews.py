import re
import asyncio
from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from src.loader import dp
from src.reviews import ReviewManager
from src.constants import REVIEW_TYPES, REVIEW_PROMPTS, REVIEW_SUCCESS
from src.keyboards import get_back_to_main_button
from src.handlers.states import ReviewStates

async def show_reviews_menu(update: types.Message | types.CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👨‍🏫 О тренере", callback_data="review_trainer")],
        [InlineKeyboardButton(text="🤖 О боте", callback_data="review_bot")],
        [InlineKeyboardButton(text="💡 Пожелание", callback_data="review_wish")],
        [InlineKeyboardButton(text="📋 Мои отзывы", callback_data="my_reviews")],
        [InlineKeyboardButton(text="◀ Назад", callback_data="back_to_main")]
    ])
    text = "📝 *Оставьте отзыв или пожелание*"
    if isinstance(update, types.CallbackQuery):
        await update.message.edit_text(text, parse_mode="Markdown", reply_markup=kb)
        await update.answer()
    else:
        await update.answer(text, parse_mode="Markdown", reply_markup=kb)

@dp.message(F.text == "📝 Отзывы")
async def reviews_main_menu(message: types.Message):
    await show_reviews_menu(message)

@dp.callback_query(F.data.startswith("review_"))
async def review_choose_type(callback: types.CallbackQuery, state: FSMContext):
    review_type = callback.data.replace("review_", "")
    await state.update_data(review_type=review_type)

    if review_type == "trainer":
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="👨‍🏫 Валентин", callback_data="target_valentin")],
            [InlineKeyboardButton(text="⚡ Алексей Панков", callback_data="target_alexey")],
            [InlineKeyboardButton(text="◀ Назад", callback_data="back_to_reviews")]
        ])
        await callback.message.edit_text("Выберите тренера:", reply_markup=kb)
        await state.set_state(ReviewStates.waiting_for_target)
    else:
        await callback.message.edit_text(REVIEW_PROMPTS[review_type])
        await state.set_state(ReviewStates.waiting_for_text)
    await callback.answer()

@dp.callback_query(ReviewStates.waiting_for_target)
async def review_choose_target(callback: types.CallbackQuery, state: FSMContext):
    target = callback.data.replace("target_", "")
    target_id = 1 if target == "valentin" else 2
    await state.update_data(target_id=target_id, target_name=target)
    await callback.message.edit_text(REVIEW_PROMPTS['trainer'])
    await state.set_state(ReviewStates.waiting_for_text)
    await callback.answer()

@dp.message(ReviewStates.waiting_for_text)
async def review_get_text(message: types.Message, state: FSMContext):
    text = message.text.strip()
    if len(text) < 10:
        await message.answer("❌ Слишком короткий отзыв. Напишите хотя бы 10 символов.")
        return
    await state.update_data(text=text)

    data = await state.get_data()
    if data['review_type'] == 'trainer':
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⭐" * i, callback_data=f"rating_{i}") for i in range(1, 6)]
        ])
        await message.answer("Оцените тренера от 1 до 5:", reply_markup=kb)
        await state.set_state(ReviewStates.waiting_for_rating)
    else:
        await save_review(message, state, rating=None)

@dp.callback_query(ReviewStates.waiting_for_rating)
async def review_get_rating(callback: types.CallbackQuery, state: FSMContext):
    rating = int(callback.data.replace("rating_", ""))
    await callback.answer()
    await save_review(callback.message, state, rating)

@dp.message(ReviewStates.waiting_for_rating)
async def review_get_rating_text(message: types.Message, state: FSMContext):
    text = message.text.strip()
    numbers = re.findall(r'\d+', text)
    if numbers:
        rating = int(numbers[0])
        if 1 <= rating <= 5:
            await save_review(message, state, rating)
            return
    await message.answer("❌ Пожалуйста, укажите оценку от 1 до 5 цифрой или нажмите на кнопку.")

async def save_review(message_or_callback, state: FSMContext, rating=None):
    data = await state.get_data()
    review_type = data['review_type']
    target_id = data.get('target_id')
    text = data['text']

    user_id = message_or_callback.chat.id if hasattr(message_or_callback, 'chat') else message_or_callback.from_user.id

    review = await ReviewManager.create_review(
        telegram_id=user_id,
        review_type=review_type,
        text=text,
        target_id=target_id,
        rating=rating
    )
    if review:
        await message_or_callback.answer(REVIEW_SUCCESS)
    else:
        await message_or_callback.answer("❌ Ошибка при сохранении отзыва.")
    await state.clear()
    await show_reviews_menu(message_or_callback)

@dp.callback_query(F.data == "my_reviews")
async def my_reviews(callback: types.CallbackQuery):
    reviews = await ReviewManager.get_reviews_by_user(callback.from_user.id)
    if not reviews:
        await callback.message.edit_text("У вас пока нет отзывов.")
        await asyncio.sleep(2)
        await show_reviews_menu(callback)
        return

    text = "📋 *Ваши отзывы:*\n\n"
    for r in reviews:
        type_name = REVIEW_TYPES.get(r.review_type, r.review_type)
        target = f" (тренер {r.target_id})" if r.target_id else ""
        rating = f" Оценка: {r.rating}⭐" if r.rating else ""
        date = r.created_at.strftime("%d.%m.%Y")
        text += f"• {type_name}{target}{rating}\n   {r.text[:50]}...\n   {date}\n\n"
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀ Назад", callback_data="back_to_reviews")]
    ])
    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=kb)

@dp.callback_query(F.data == "back_to_reviews")
async def back_to_reviews(callback: types.CallbackQuery):
    await show_reviews_menu(callback)