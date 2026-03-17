from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from src.db import DatabaseManager

async def get_main_keyboard(telegram_id: int) -> ReplyKeyboardMarkup:
    is_premium = await DatabaseManager.is_premium_user(telegram_id)
    buttons = [
        [KeyboardButton(text="💪 Тренировки")],
        [KeyboardButton(text="🍎 Питание"), KeyboardButton(text="📊 Прогресс")],
        [KeyboardButton(text="📝 Памятки")],
    ]
    if is_premium:
        buttons.append([KeyboardButton(text="💊 БАДы и Спортпит")])
        buttons.append([KeyboardButton(text="🧪 ААС и фармакология"), KeyboardButton(text="🩸 Анализы")])
        buttons.append([KeyboardButton(text="👨‍🏫 Тренеры"), KeyboardButton(text="📋 Составление питания")])
        buttons.append([KeyboardButton(text="🎵 Треки")])
    else:
        buttons.append([KeyboardButton(text="💊 БАДы (Premium) 🔒")])
        buttons.append([KeyboardButton(text="🧪 ААС (Premium) 🔒"), KeyboardButton(text="🩸 Анализы (Premium) 🔒")])
        buttons.append([KeyboardButton(text="👨‍🏫 Тренеры"), KeyboardButton(text="📋 Питание (Premium) 🔒")])
    buttons.append([KeyboardButton(text="📝 Отзывы")])
    buttons.append([KeyboardButton(text="💰 Услуги")])
    buttons.append([KeyboardButton(text="🛒 Наш бренд")])
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def get_back_to_main_button() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀ Назад в главное меню", callback_data="back_to_main")]
    ])

def get_back_to_trainings_button() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀ Назад к тренировкам", callback_data="back_to_trainings")]
    ])

def get_back_to_nutrition_button() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀ Назад к питанию", callback_data="back_to_nutrition")]
    ])

def gender_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👨 Мужской", callback_data="gender_male")],
        [InlineKeyboardButton(text="👩 Женский", callback_data="gender_female")],
        [InlineKeyboardButton(text="◀ Назад", callback_data="back_to_main")]
    ])

def activity_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🪑 Минимальная (сидячая работа)", callback_data="activity_minimal")],
        [InlineKeyboardButton(text="🚶 Легкая (1-3 тренировки)", callback_data="activity_light")],
        [InlineKeyboardButton(text="🏃 Средняя (3-5 тренировок)", callback_data="activity_moderate")],
        [InlineKeyboardButton(text="🏋️ Высокая (6-7 тренировок)", callback_data="activity_high")],
        [InlineKeyboardButton(text="⚡ Экстремальная (спортсмены)", callback_data="activity_extreme")],
    ])

def goal_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⚖️ Похудение", callback_data="goal_loss")],
        [InlineKeyboardButton(text="💪 Поддержание", callback_data="goal_maintenance")],
        [InlineKeyboardButton(text="🏋️ Набор массы", callback_data="goal_gain")],
    ])