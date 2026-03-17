import logging
from pathlib import Path
from aiogram import types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.exceptions import TelegramBadRequest
from src.loader import dp
from src.utils import send_photo_with_cache
from src.config import MEDIA_DIR

logger = logging.getLogger(__name__)

TRAINERS = {
    "valentin": {
        "name": "Валентин",
        "photo": "trainers/Gorbunov.jpg",
        "description": (
            "👨‍🏫 *Валентин — твой персональный тренер*\n\n"
            "🔥 *Опыт и Достижения:*\n"
            "Более 15 лет успешной карьеры в мире спорта: каратэ, бокс, MMA, тяжёлая атлетика. "
            "Уникальный подход к тренировкам, закалённый годами практики.\n\n"
            "💥 *Многостороннее Мастерство:*\n"
            "Глубокое понимание организма и разнообразие методик — от простых кардио до продвинутых комплексов. "
            "Программа под любой уровень подготовки!\n\n"
            "✅ *Результат гарантирован*\n\n"
            "😊 *Поддержка и Инспирация:*\n"
            "Валентин не просто тренер, а друг и мотиватор. Атмосфера поддержки и взаимовыручки поможет тебе прогрессировать с удовольствием.\n\n"
            "Начни своё путешествие к идеальной форме вместе с Валентином прямо сейчас! 💪"
        )
    },
    "alexey": {
        "name": "Алексей Панков",
        "photo": "trainers/Pankov.jpg",
        "description": (
            "⚡️ *Персональный тренер тренажёрного зала — Панков Алексей* ⚡️\n\n"
            "Опыт в фитнесе: более 5 лет\n\n"
            "*Специализация:*\n"
            "• Составление персонализированных планов занятий с учётом физических особенностей, возраста, состояния здоровья и желаемого результата каждого клиента;\n\n"
            "• Составление плана питания под конкретные цели: набор мышечной массы, снижение веса или поддержание оптимальной физической формы;\n\n"
            "• Распределение тренировочной нагрузки, исходя из текущего физического состояния, что обеспечивает безопасность и максимальную эффективность занятий;\n\n"
            "• Коррекция техники выполнения упражнений для предотвращения перегрузок и получения максимального результата от каждой тренировки;\n\n"
            "• Сопровождение и поддержка мотивации: помощь в постановке реальных целей, отслеживание прогресса, своевременная корректировка программ и поддержка на каждом этапе.\n\n"
            "🎁 *Хочешь записаться на БЕСПЛАТНУЮ пробную тренировку?*\n"
            "Или на *ОНЛАЙН тренировки*!\n\n"
            "Жду тебя на связи! 😉"
        )
    }
}

@dp.message(F.text == "👨‍🏫 Тренеры")
async def trainers_menu(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👨‍🏫 Валентин", callback_data="trainer_valentin")],
        [InlineKeyboardButton(text="⚡ Алексей Панков", callback_data="trainer_alexey")],
        [InlineKeyboardButton(text="◀ Назад", callback_data="back_to_main")]
    ])
    await message.answer(
        "Выбери тренера, чтобы узнать подробности:",
        reply_markup=kb
    )

@dp.callback_query(F.data.startswith("trainer_"))
async def show_trainer_info(callback: types.CallbackQuery):
    await callback.answer()
    trainer_key = callback.data.replace("trainer_", "")
    trainer = TRAINERS.get(trainer_key)
    if not trainer:
        await callback.message.answer("❌ Тренер не найден")
        return

    photo_path = MEDIA_DIR / trainer["photo"]
    logger.info(f"🖼️ Попытка отправить фото тренера {trainer_key}: {photo_path}")
    logger.info(f"📁 Файл существует: {photo_path.exists()}")

    if trainer_key == "alexey":
        short_desc = (
            "⚡️ *Алексей Панков — персональный тренер* ⚡️\n\n"
            f"Опыт: более 5 лет\n\n"
            "👇 *Подробности в следующем сообщении*"
        )
        details = (
            "*Специализация:*\n\n"
            "• Составление персонализированных планов занятий с учётом физических особенностей, возраста, состояния здоровья и желаемого результата каждого клиента;\n\n"
            "• Составление плана питания под конкретные цели: набор мышечной массы, снижение веса или поддержание оптимальной физической формы;\n\n"
            "• Распределение тренировочной нагрузки, исходя из текущего физического состояния, что обеспечивает безопасность и максимальную эффективность занятий;\n\n"
            "• Коррекция техники выполнения упражнений для предотвращения перегрузок и получения максимального результата от каждой тренировки;\n\n"
            "• Сопровождение и поддержка мотивации: помощь в постановке реальных целей, отслеживание прогресса, своевременная корректировка программ и поддержка на каждом этапе.\n\n"
            "🎁 *Хочешь записаться на БЕСПЛАТНУЮ пробную тренировку?*\n"
            "Или на *ОНЛАЙН тренировки*!\n\n"
            "Жду тебя на связи! 😉"
        )
        await send_photo_with_cache(callback.message.chat.id, photo_path, short_desc, "Markdown")
        await callback.message.answer(details, parse_mode="Markdown")
    else:
        text = trainer["description"]
        await send_photo_with_cache(callback.message.chat.id, photo_path, text, "Markdown")

    # Пытаемся удалить исходное сообщение, игнорируем ошибку, если оно уже удалено
    try:
        await callback.message.delete()
    except TelegramBadRequest as e:
        if "message to delete not found" in str(e):
            logger.warning("Сообщение уже удалено")
        else:
            raise