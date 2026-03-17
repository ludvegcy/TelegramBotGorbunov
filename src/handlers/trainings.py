import asyncio
from aiogram.exceptions import TelegramBadRequest
from pathlib import Path
from aiogram import types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from src.loader import dp
from src.db import DatabaseManager
from src.exercises_db import EXERCISES, get_exercise
from src.keyboards import get_back_to_trainings_button
from src.utils import send_photo_with_cache, file_id_cache
from src.config import MEDIA_DIR

# Словарь с текстами программ
TRAININGS = {
    "train_chest_tri": {
        "title": "🏋️ ГРУДЬ И ТРИЦЕПС",
        "text": (
            "*Почему вместе:* При жимах грудь работает в начале движения, трицепс — в конце. Тренируя грудь первой, мы подготавливаем трицепс к добивке.\n\n"
            "*💪 ПРОГРАММА (ЗАЛ):*\n"
            "1️⃣ Жим штанги лежа — 4 подхода х 8-10 повторений\n"
            "2️⃣ Жим гантелей на наклонной скамье (30°) — 4х10-12\n"
            "3️⃣ Сведение рук в кроссовере — 3х15\n"
            "4️⃣ Французский жим со штангой — 4х12\n"
            "5️⃣ Разгибание рук в блоке — 3х15\n\n"
            "*🏠 ПРОГРАММА (ДОМА):*\n"
            "1️⃣ Отжимания от пола (широкие) — 4х max\n"
            "2️⃣ Отжимания с ногами на стуле — 4х12-15\n"
            "3️⃣ Пуловер с бутылкой/гантелью — 4х15\n"
            "4️⃣ Обратные отжимания от стула — 4х15\n"
            "5️⃣ Алмазные отжимания (узкие) — 3х12"
        )
    },
    "train_back_bi": {
        "title": "🔥 СПИНА И БИЦЕПС",
        "text": (
            "*Почему вместе:* Во всех тяговых движениях бицепс уже работает как помощник. Логично добить его в конце.\n\n"
            "*💪 ПРОГРАММА (ЗАЛ):*\n"
            "1️⃣ Подтягивания (или тяга верхнего блока) — 4х8-10\n"
            "2️⃣ Тяга штанги в наклоне — 4х10\n"
            "3️⃣ Горизонтальная тяга в блоке — 4х12\n"
            "4️⃣ Подъем штанги на бицепс — 4х10\n"
            "5️⃣ Молотки с гантелями — 4х12\n"
            "6️⃣ Гиперэкстензия — 3х15\n\n"
            "*🏠 ПРОГРАММА (ДОМА):*\n"
            "1️⃣ Подтягивания (если есть турник) — 4х max\n"
            "2️⃣ Тяга гантели/рюкзака в наклоне — 4х12\n"
            "3️⃣ Супермен (разгибатели спины) — 3х20\n"
            "4️⃣ Подъем гантелей/бутылок на бицепс — 4х12\n"
            "5️⃣ Становая тяга с гантелями — 4х12"
        )
    },
    "train_legs_shoulders": {
        "title": "🦵 НОГИ И ПЛЕЧИ",
        "text": (
            "*Почему вместе:* Классика трёхдневного сплита. Обе группы требуют много энергии.\n\n"
            "*💪 ПРОГРАММА (ЗАЛ):*\n"
            "1️⃣ Приседания со штангой — 4х8-10\n"
            "2️⃣ Жим ногами — 4х12\n"
            "3️⃣ Разгибание ног в тренажере — 3х15\n"
            "4️⃣ Армейский жим (стоя) — 4х10\n"
            "5️⃣ Махи гантелей в стороны — 3х15\n"
            "6️⃣ Подъем на носки — 4х20\n\n"
            "*🏠 ПРОГРАММА (ДОМА):*\n"
            "1️⃣ Приседания (можно с рюкзаком) — 4х20\n"
            "2️⃣ Выпады — 4х15 на ногу\n"
            "3️⃣ Ягодичный мостик — 4х20\n"
            "4️⃣ Жим гантелей сидя — 4х12\n"
            "5️⃣ Подъем на носки стоя — 4х30"
        )
    },
    "train_cardio": {
        "title": "❤️ КАРДИОТРЕНИРОВКИ",
        "text": (
            "Это аэробная нагрузка для укрепления сердца и сжигания жира.\n\n"
            "*📋 ПРАВИЛА:*\n"
            "• Начинай с разминки 5-10 минут\n"
            "• Пульс держи в зоне 60-85% от макс (220 - возраст)\n"
            "• Заканчивай заминкой и растяжкой\n"
            "• Частота: 3-5 раз в неделю\n\n"
            "*🏃 ВИДЫ КАРДИО:*\n"
            "• Бег (улица/дорожка)\n"
            "• Ходьба (в том числе интервальная)\n"
            "• Велосипед/велотренажёр\n"
            "• Плавание\n"
            "• Скакалка\n"
            "• Эллипс"
        )
    },
    "train_stretch": {
        "title": "🧘 РАСТЯЖКА",
        "text": (
            "Улучшает гибкость, ускоряет восстановление, снижает риск травм.\n\n"
            "*📋 ПРАВИЛА:*\n"
            "• Только на разогретые мышцы (после тренировки)\n"
            "• Не должно быть острой боли, только легкое натяжение\n"
            "• Задерживайся в позе на 20-30 секунд\n"
            "• Дыши ровно и глубоко\n\n"
            "*🤸 УПРАЖНЕНИЯ:*\n"
            "• *Выпады* — для сгибателей бедра\n"
            "• *Наклоны к ногам* — задняя поверхность бедра\n"
            "• *Замок за спиной* — плечи, грудь\n"
            "• *Скручивания* — спина\n"
            "• *Бабочка* — внутренняя поверхность бедра\n"
            "• *Кошка-корова* — позвоночник"
        )
    }
}

@dp.message(F.text == "💪 Тренировки")
async def trainings_menu(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏋️ Грудь + Трицепс", callback_data="train_chest_tri")],
        [InlineKeyboardButton(text="🔥 Спина + Бицепс", callback_data="train_back_bi")],
        [InlineKeyboardButton(text="🦵 Ноги + Плечи", callback_data="train_legs_shoulders")],
        [InlineKeyboardButton(text="❤️ Кардио", callback_data="train_cardio")],
        [InlineKeyboardButton(text="🧘 Растяжка", callback_data="train_stretch")],
        [InlineKeyboardButton(text="◀ Назад в главное меню", callback_data="back_to_main")]
    ])
    await message.answer("🏋️ *Выбери группу мышц для тренировки:*", parse_mode="Markdown", reply_markup=kb)

@dp.callback_query(F.data.in_(list(TRAININGS.keys())))
async def process_trainings(callback: types.CallbackQuery):
    data = callback.data

    # Если пользователь премиум, показать детальные упражнения
    if await DatabaseManager.is_premium_user(callback.from_user.id) and data in ["train_chest_tri", "train_back_bi", "train_legs_shoulders"]:
        if data == "train_chest_tri":
            await show_premium_chest_tri(callback)
        elif data == "train_back_bi":
            await show_premium_back_bi(callback)
        elif data == "train_legs_shoulders":
            await show_premium_legs_shoulders(callback)
        return

    train = TRAININGS.get(data)
    if train:
        text = f"*{train['title']}*\n\n{train['text']}"
        try:
            await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=get_back_to_trainings_button())
        except TelegramBadRequest as e:
            if "message is not modified" in str(e):
                await callback.answer()
            else:
                raise
    else:
        await callback.answer("Неизвестная тренировка")

async def show_premium_chest_tri(callback: types.CallbackQuery):
    exercises = [
        ("Жим штанги лежа", "bench_press"),
        ("Жим гантелей на наклонной скамье", "incline_dumbbell_press"),
        ("Брусья", "dips"),
        ("Французский жим", "french_press"),
        ("Разгибание с канатиком", "triceps_cable_extension"),
        ("Пек-дек (бабочка)", "butterfly2"),
    ]
    await show_premium_exercise_list(callback, exercises)

async def show_premium_back_bi(callback: types.CallbackQuery):
    exercises = [
        ("Подтягивания", "pullups"),
        ("Тяга штанги в наклоне", "bent_over_row"),
        ("Горизонтальная тяга сидя", "seated_cable_row"),
        ("Тяга гантели одной рукой", "one_arm_dumbbell_row"),
        ("Тяга вертикального блока", "lat_pulldown"),
        ("Подъем EZ-грифа", "ez_bar_curl"),
        ("Подъем гантелей с супинацией", "dumbbell_curl_supination")
    ]
    await show_premium_exercise_list(callback, exercises)

async def show_premium_legs_shoulders(callback: types.CallbackQuery):
    exercises = [
        ("Присед со штангой", "squat"),
        ("Жим ногами", "leg_press"),
        ("Румынская тяга", "romanian_deadlift"),
        ("Армейский жим гантелей", "overhead_press"),
        ("Баттерфляй", "butterfly"),
        ("Обратный пэк-дэк", "reverse_pec_deck"),
        ("Махи гантелей в стороны", "lateral_raises")
    ]
    await show_premium_exercise_list(callback, exercises)

async def show_premium_exercise_list(callback: types.CallbackQuery, exercises):
    kb_buttons = []
    for name, key in exercises:
        if key in EXERCISES:
            kb_buttons.append([InlineKeyboardButton(text=f"🏋️ {name}", callback_data=f"ex_{key}")])
    kb_buttons.append([InlineKeyboardButton(text="◀ Назад к тренировкам", callback_data="back_to_trainings")])
    kb = InlineKeyboardMarkup(inline_keyboard=kb_buttons)
    try:
        await callback.message.edit_text(
            "👇 *Выбери упражнение для просмотра техники и фото:*",
            parse_mode="Markdown", reply_markup=kb
        )
    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            await callback.answer()
        else:
            raise

@dp.callback_query(F.data.startswith("ex_"))
async def show_exercise_detail(callback: types.CallbackQuery):
    if not await DatabaseManager.is_premium_user(callback.from_user.id):
        await callback.answer("❌ Эта функция доступна только в полной версии", show_alert=True)
        return

    ex_key = callback.data.replace("ex_", "")
    exercise = get_exercise(ex_key)
    if not exercise:
        await callback.answer("Упражнение не найдено")
        return

    photo_path = MEDIA_DIR / exercise["photo"]
    name = exercise['name']
    technique = exercise['technique']

    # Отправляем фото (если есть)
    if photo_path.exists():
        await send_photo_with_cache(callback.message.chat.id, photo_path, f"*{name}*", "Markdown")
    else:
        # Если фото нет, отправляем название и технику вместе
        full_text = f"*{name}*\n\n{technique}"
        await callback.message.answer(full_text, parse_mode="Markdown")
        await callback.answer()
        return

    # Отправляем технику отдельно (с разбивкой)
    if len(technique) > 4096:
        parts = [technique[i:i+4096] for i in range(0, len(technique), 4096)]
        for part in parts:
            await callback.message.answer(part, parse_mode="Markdown")
    else:
        await callback.message.answer(technique, parse_mode="Markdown")

    await callback.answer()