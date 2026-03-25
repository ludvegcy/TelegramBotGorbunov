from datetime import datetime, timedelta
from aiogram import types, F
from aiogram.filters import Command
from src.loader import dp
from src.db import DatabaseManager
from src.config import ADMINS

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
            await message.answer(f"✅ Премиум активирован для user_id {user_id} на {days} дней")
        else:
            await DatabaseManager.create_user(
                telegram_id=user_id,
                is_premium=True,
                premium_until=datetime.now() + timedelta(days=days)
            )
            await message.answer(f"✅ Создан новый пользователь {user_id} с премиум на {days} дней")
    except ValueError:
        await message.answer("❌ Неверный формат. Используйте: /premium 123456789 30")