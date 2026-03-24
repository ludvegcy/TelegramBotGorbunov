from aiogram import types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from src.loader import dp
from src.db import DatabaseManager
from src.keyboards import get_back_to_main_button
from src.supps_database import SUPPS

@dp.message(F.text.contains("БАДы"))
async def supps_menu(message: types.Message, **kwargs):
    if not await DatabaseManager.is_premium_user(message.from_user.id):
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💎 Купить полную версию", callback_data="tariff_full_month")]
        ])
        await message.answer(
            "🔒 *Это премиум-функция*\n\n"
            "Оформи подписку за 299₽ в разделе 💰 Услуги и получи доступ ко всем возможностям бота:\n"
            "• Все БАДы и их описание\n"
            "• Информацию по ААС и фармакологии\n"
            "• Слежение за анализами крови\n"
            "• Персональные консультации тренеров\n"
            "• Детальные программы упражнений с фото и техникой",
            parse_mode="Markdown",
            reply_markup=kb
        )
        return

    buttons = []
    for supp_name in SUPPS.keys():
        buttons.append([InlineKeyboardButton(text=f"💊 {supp_name.capitalize()}", callback_data=f"supp_{supp_name}")])
    buttons.append([InlineKeyboardButton(text="◀ Назад", callback_data="back_to_main")])
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer("💊 *Спортивные добавки*\n\nВыбери добавку для подробной информации:",
                         parse_mode="Markdown", reply_markup=kb)

@dp.callback_query(F.data.startswith("supp_"))
async def process_supp(callback: types.CallbackQuery):
    supp_name = callback.data.replace("supp_", "")
    supp = SUPPS.get(supp_name)
    if supp:
        text = (f"*💊 {supp_name.upper()}*\n\n"
                f"*Описание:* {supp['description']}\n"
                f"*Дозировка:* {supp['dosage']}\n"
                f"*Время приема:* {supp['timing']}\n"
                f"*Польза:* {supp['benefits']}")
    else:
        text = "Информация не найдена"
    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=get_back_to_main_button())

@dp.message(F.text.contains("ААС"))
async def aas_info(message: types.Message, **kwargs):
    if not await DatabaseManager.is_premium_user(message.from_user.id):
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💎 Купить полную версию", callback_data="tariff_full_month")]
        ])
        await message.answer("🔒 Премиум...", reply_markup=kb)
        return
    text = (
        "*🧪 Информация по ААС*\n\n"
        "Здесь будет подробная информация о стероидах, ПКТ, анализах...\n\n"
        "• Основные стероиды\n"
        "• Курсы для начинающих\n"
        "• Посткурсовая терапия\n"
        "• Контроль анализов"
    )
    await message.answer(text, parse_mode="Markdown")

@dp.message(F.text.contains("Анализы"))
async def blood_tests_info(message: types.Message, **kwargs):
    if not await DatabaseManager.is_premium_user(message.from_user.id):
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💎 Купить полную версию", callback_data="tariff_full_month")]
        ])
        await message.answer("🔒 Премиум...", reply_markup=kb)
        return
    text = (
        "*🩸 Контроль анализов*\n\n"
        "Здесь будет информация о том, какие анализы сдавать и как их интерпретировать...\n\n"
        "• Базовые анализы\n"
        "• Гормональный профиль\n"
        "• Печёночные пробы\n"
        "• Почечные показатели"
    )
    await message.answer(text, parse_mode="Markdown")

@dp.message(F.text.contains("Питание") & F.text.contains("Premium"))
async def diet_plan(message: types.Message, **kwargs):
    if not await DatabaseManager.is_premium_user(message.from_user.id):
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💎 Купить полную версию", callback_data="tariff_full_month")]
        ])
        await message.answer("🔒 Премиум...", reply_markup=kb)
        return
    text = (
        "*📋 Составление индивидуального питания*\n\n"
        "Здесь будет информация о том, как составить план питания под ваши цели.\n\n"
        "• Расчёт калорий и БЖУ\n"
        "• Подбор продуктов\n"
        "• Примеры рационов\n"
        "• Советы по режиму"
    )
    await message.answer(text, parse_mode="Markdown")

@dp.message(F.text == "📋 Составление питания")
async def diet_plan_choice(message: types.Message):
    if not await DatabaseManager.is_premium_user(message.from_user.id):
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💎 Купить полную версию", callback_data="tariff_full_month")]
        ])
        await message.answer(
            "🔒 Эта функция доступна только в полной версии.\n\n"
            "Оформи подписку в разделе 💰 Услуги.",
            parse_mode="Markdown",
            reply_markup=kb
        )
        return

    # Клавиатура выбора тренера
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👨‍🏫 Валентин", callback_data="diet_plan_valentin")],
        [InlineKeyboardButton(text="⚡ Алексей Панков", callback_data="diet_plan_alexey")],
        [InlineKeyboardButton(text="◀ Назад", callback_data="back_to_main")]
    ])
    await message.answer(
        "📋 Выберите тренера, который составит для вас индивидуальный план питания:",
        reply_markup=kb
    )

@dp.callback_query(F.data.startswith("diet_plan_"))
async def diet_plan_choose_trainer(callback: types.CallbackQuery):
    trainer_key = callback.data.replace("diet_plan_", "")
    if trainer_key == "valentin":
        contact = "@krivha9"
        name = "Валентин"
    elif trainer_key == "alexey":
        contact = "@irulebreaker"
        name = "Алексей Панков"
    else:
        await callback.answer("Неизвестный тренер")
        return

    text = (
        f"👨‍🏫 *{name}* поможет составить индивидуальный план питания.\n\n"
        f"Напишите ему: {contact}\n\n"
        f"Не забудьте упомянуть, что вы от бота Gorbunov Fitness!"
    )
    await callback.message.edit_text(text, parse_mode="Markdown")
    await callback.answer()