from datetime import datetime, timedelta
from aiogram import types, F
from aiogram.filters import Command
from src.constants import REVIEW_TYPES
from src.loader import dp
from src.db import DatabaseManager
from src.config import ADMINS
from src.reviews import ReviewManager

def is_admin(user_id: int) -> bool:
    return user_id in ADMINS

@dp.message(Command("stats"))
async def admin_stats(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ У вас нет прав администратора")
        return

    total_users = await DatabaseManager.get_all_users_count()
    premium_users = await DatabaseManager.get_premium_users_count()

    stats_text = (
        f"📊 *Статистика бота*\n\n"
        f"👥 Всего пользователей: {total_users}\n"
        f"💎 Премиум: {premium_users}\n"
        f"📝 Обычных: {total_users - premium_users}"
    )
    await message.answer(stats_text, parse_mode="Markdown")

@dp.message(Command("premium"))
async def admin_set_premium(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ У вас нет прав администратора")
        return

    args = message.text.split()
    if len(args) != 3:
        await message.answer("Использование: /premium [user_id] [days]")
        return

    try:
        user_id = int(args[1])
        days = int(args[2])

        user = await DatabaseManager.get_user(user_id)
        if user:
            await DatabaseManager.update_user(
                user_id,
                is_premium=True,
                premium_until=datetime.now() + timedelta(days=days)
            )
            await message.answer(f"✅ Премиум активирован для user_id {user_id} на {days} дней", parse_mode=None)
        else:
            await DatabaseManager.create_user(
                telegram_id=user_id,
                is_premium=True,
                premium_until=datetime.now() + timedelta(days=days)
            )
            await message.answer(f"✅ Создан новый пользователь {user_id} с премиум на {days} дней", parse_mode=None)
    except ValueError:
        await message.answer("❌ Неверный формат. Используйте: /premium 123456789 30", parse_mode=None)

@dp.message(Command("reviews"))
async def admin_reviews(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ У вас нет прав администратора")
        return

    reviews = await ReviewManager.get_all_reviews(limit=20)

    if not reviews:
        await message.answer("📭 Отзывов пока нет.")
        return

    text = "📋 *Последние отзывы:*\n\n"
    for rev in reviews:
        user = await DatabaseManager.get_user_by_id(rev.user_id)
        user_name = user.first_name if user.first_name else str(user.telegram_id)

        type_name = REVIEW_TYPES.get(rev.review_type, rev.review_type)
        if rev.review_type == 'trainer':
            target = "Валентин" if rev.target_id == 1 else "Алексей"
            type_name = f"👨‍🏫 Отзыв о тренере {target}"

        rating = f"⭐️ {rev.rating}" if rev.rating else ""
        date = rev.created_at.strftime("%d.%m.%Y %H:%M")

        text += f"*{type_name}* {rating}\n"
        text += f"📝 {rev.text[:200]}\n"
        text += f"👤 {user_name} | {date}\n\n"

    await message.answer(text, parse_mode=None)