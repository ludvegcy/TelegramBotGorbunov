from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from src.loader import dp
from src.db import DatabaseManager
from src.food_database import FOODS, search_food
from src.nutrition_calculator import NutritionCalculator
from src.keyboards import (
    get_back_to_nutrition_button,
    get_main_keyboard,
    gender_keyboard,
    activity_keyboard,
    goal_keyboard,
    get_back_to_main_button
)
from src.handlers.states import ProfileStates, FoodTrackingStates

@dp.message(F.text == "🍎 Питание")
async def nutrition_menu(message: types.Message):
    user = await DatabaseManager.get_user(message.from_user.id)
    if user and user.daily_calories:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📊 Пересчитать норму", callback_data="calc_norm")],
            [InlineKeyboardButton(text="🍗 Добавить продукт", callback_data="add_food")],
            [InlineKeyboardButton(text="📋 Сегодняшний рацион", callback_data="today_food")],
            [InlineKeyboardButton(text="🥑 Советы по питанию", callback_data="food_tips")],
            [InlineKeyboardButton(text="◀ Назад", callback_data="back_to_main")]
        ])
        totals = await DatabaseManager.get_today_totals(message.from_user.id)
        remaining = user.daily_calories - totals['calories']
        await message.answer(
            f"🍎 *Раздел Питания*\n\n"
            f"*Твоя норма:* {user.daily_calories} ккал\n"
            f"*Сегодня:* {totals['calories']} ккал\n"
            f"*Осталось:* {remaining} ккал\n"
            f"*Б/Ж/У:* {totals['protein']:.1f} / {totals['fat']:.1f} / {totals['carbs']:.1f} г\n\n"
            f"Выбери действие:",
            parse_mode="Markdown", reply_markup=kb
        )
    else:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📊 Рассчитать норму калорий", callback_data="calc_norm")],
            [InlineKeyboardButton(text="🍗 База продуктов (КБЖУ)", callback_data="food_base")],
            [InlineKeyboardButton(text="🥑 Советы по питанию", callback_data="food_tips")],
            [InlineKeyboardButton(text="◀ Назад", callback_data="back_to_main")]
        ])
        await message.answer("🍎 *Раздел Питания*\n\nСначала рассчитай свою норму калорий:",
                             parse_mode="Markdown", reply_markup=kb)

@dp.callback_query(F.data == "calc_norm")
async def start_calc(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "📊 *РАСЧЕТ НОРМЫ КАЛОРИЙ*\n\n"
        "Давай рассчитаем твою индивидуальную норму!\n\n"
        "Сначала выбери пол:",
        parse_mode="Markdown", reply_markup=gender_keyboard()
    )
    await state.set_state(ProfileStates.gender)

@dp.callback_query(ProfileStates.gender)
async def process_gender(callback: types.CallbackQuery, state: FSMContext):
    gender = "male" if callback.data == "gender_male" else "female"
    await state.update_data(gender=gender)
    await callback.message.edit_text("📊 Введи свой вес (в кг):\n\nНапример: 75.5")
    await state.set_state(ProfileStates.weight)

@dp.message(ProfileStates.weight)
async def process_weight(message: types.Message, state: FSMContext):
    try:
        weight = float(message.text.replace(',', '.'))
        if weight < 30 or weight > 250:
            await message.answer("⚠️ Вес должен быть от 30 до 250 кг. Попробуй еще раз:")
            return
        await state.update_data(weight=weight)
        await message.answer("📊 Теперь введи свой рост (в см):\n\nНапример: 175")
        await state.set_state(ProfileStates.height)
    except ValueError:
        await message.answer("⚠️ Пожалуйста, введи число (например: 75.5)")

@dp.message(ProfileStates.height)
async def process_height(message: types.Message, state: FSMContext):
    try:
        height = float(message.text)
        if height < 100 or height > 250:
            await message.answer("⚠️ Рост должен быть от 100 до 250 см. Попробуй еще раз:")
            return
        await state.update_data(height=height)
        await message.answer("📊 Теперь введи свой возраст:")
        await state.set_state(ProfileStates.age)
    except ValueError:
        await message.answer("⚠️ Пожалуйста, введи число (например: 25)")

@dp.message(ProfileStates.age)
async def process_age(message: types.Message, state: FSMContext):
    try:
        age = int(message.text)
        if age < 10 or age > 100:
            await message.answer("⚠️ Возраст должен быть от 10 до 100 лет. Попробуй еще раз:")
            return
        await state.update_data(age=age)
        await message.answer("📊 Выбери уровень активности:", reply_markup=activity_keyboard())
        await state.set_state(ProfileStates.activity)
    except ValueError:
        await message.answer("⚠️ Пожалуйста, введи целое число")

@dp.callback_query(ProfileStates.activity)
async def process_activity(callback: types.CallbackQuery, state: FSMContext):
    activity_map = {
        "activity_minimal": "minimal",
        "activity_light": "light",
        "activity_moderate": "moderate",
        "activity_high": "high",
        "activity_extreme": "extreme"
    }
    activity = activity_map.get(callback.data, "moderate")
    await state.update_data(activity=activity)
    await callback.message.edit_text("📊 Выбери свою цель:", reply_markup=goal_keyboard())
    await state.set_state(ProfileStates.goal)

@dp.callback_query(ProfileStates.goal)
async def process_goal(callback: types.CallbackQuery, state: FSMContext):
    goal_map = {
        "goal_loss": "weight_loss",
        "goal_maintenance": "maintenance",
        "goal_gain": "weight_gain"
    }
    goal = goal_map.get(callback.data, "maintenance")
    data = await state.get_data()
    data['goal'] = goal

    bmr = NutritionCalculator.calculate_bmr(
        data['weight'], data['height'], data['age'], data['gender']
    )
    maintenance = NutritionCalculator.calculate_maintenance(bmr, data['activity'])
    daily_calories = NutritionCalculator.get_goal_calories(maintenance, goal)

    user = await DatabaseManager.get_user(callback.from_user.id)
    if user:
        await DatabaseManager.update_user(
            callback.from_user.id,
            weight=data['weight'],
            height=data['height'],
            age=data['age'],
            gender=data['gender'],
            activity=data['activity'],
            goal=goal,
            daily_calories=int(daily_calories)
        )
    else:
        await DatabaseManager.create_user(
            telegram_id=callback.from_user.id,
            weight=data['weight'],
            height=data['height'],
            age=data['age'],
            gender=data['gender'],
            activity=data['activity'],
            goal=goal,
            daily_calories=int(daily_calories)
        )

    result_text = (
        "✅ *ГОТОВО!*\n\n"
        f"*Твой базовый обмен:* {int(bmr)} ккал\n"
        f"*Поддержание веса:* {int(maintenance)} ккал\n"
        f"*Твоя цель:* {int(daily_calories)} ккал/день\n\n"
    )
    if goal == "weight_loss":
        result_text += "🎯 *Режим: Похудение*\nРекомендуемый дефицит: 15%"
    elif goal == "weight_gain":
        result_text += "🎯 *Режим: Набор массы*\nРекомендуемый профицит: 15%"
    else:
        result_text += "🎯 *Режим: Поддержание веса*"
    result_text += "\n\nТеперь ты можешь добавлять продукты в разделе Питание!"

    await callback.message.edit_text(
        result_text, parse_mode="Markdown", reply_markup=get_back_to_main_button()
    )
    await state.clear()

@dp.callback_query(F.data == "add_food")
async def add_food_start(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("🍗 Введи название продукта:\n\nНапример: курица, яйцо, гречка")
    await state.set_state(FoodTrackingStates.waiting_for_food_name)

@dp.message(FoodTrackingStates.waiting_for_food_name)
async def process_food_name(message: types.Message, state: FSMContext):
    food_name = message.text.lower().strip()
    results = search_food(food_name)
    if not results:
        await message.answer(f"❌ Продукт '{food_name}' не найден.\n\nПопробуй другое название или посмотри базу продуктов.")
        return
    if len(results) == 1:
        name, data = results[0]
        await state.update_data(selected_food=name, food_data=data)
        await message.answer(
            f"Найден продукт: *{name.capitalize()}*\n"
            f"КБЖУ на 100г: {data['kcal']} ккал, Б:{data['protein']}г, Ж:{data['fat']}г, У:{data['carbs']}г\n\n"
            f"Сколько грамм ты съел(а)?",
            parse_mode="Markdown"
        )
        await state.set_state(FoodTrackingStates.waiting_for_food_weight)
    else:
        kb_buttons = []
        for name, data in results[:5]:
            kb_buttons.append([InlineKeyboardButton(
                text=f"{name.capitalize()} ({data['kcal']} ккал)",
                callback_data=f"food_{name}"
            )])
        kb = InlineKeyboardMarkup(inline_keyboard=kb_buttons)
        await state.update_data(search_results=results)
        await message.answer("Найдено несколько продуктов. Выбери нужный:", reply_markup=kb)

@dp.callback_query(FoodTrackingStates.waiting_for_food_name)
async def select_food_from_list(callback: types.CallbackQuery, state: FSMContext):
    food_name = callback.data.replace("food_", "")
    data = await state.get_data()
    results = data.get('search_results', [])
    for name, food_data in results:
        if name == food_name:
            await state.update_data(selected_food=name, food_data=food_data)
            await callback.message.edit_text(
                f"Выбран продукт: *{name.capitalize()}*\n"
                f"КБЖУ на 100г: {food_data['kcal']} ккал, "
                f"Б:{food_data['protein']}г, Ж:{food_data['fat']}г, У:{food_data['carbs']}г\n\n"
                f"Сколько грамм ты съел(а)?",
                parse_mode="Markdown"
            )
            await state.set_state(FoodTrackingStates.waiting_for_food_weight)
            break

@dp.message(FoodTrackingStates.waiting_for_food_weight)
async def process_food_weight(message: types.Message, state: FSMContext):
    try:
        weight = float(message.text.replace(',', '.'))
        if weight < 1 or weight > 5000:
            await message.answer("⚠️ Вес должен быть от 1 до 5000 грамм. Попробуй еще раз:")
            return
        data = await state.get_data()
        food_name = data['selected_food']
        food_data = data['food_data']
        factor = weight / 100
        calories = int(food_data['kcal'] * factor)
        protein = food_data['protein'] * factor
        fat = food_data['fat'] * factor
        carbs = food_data['carbs'] * factor
        await DatabaseManager.add_food_entry(
            message.from_user.id, food_name, calories, protein, fat, carbs
        )
        totals = await DatabaseManager.get_today_totals(message.from_user.id)
        user = await DatabaseManager.get_user(message.from_user.id)
        keyboard = await get_main_keyboard(message.from_user.id)
        await message.answer(
            f"✅ *Продукт добавлен!*\n\n"
            f"• {food_name.capitalize()}: {weight}г\n"
            f"• Калории: {calories} ккал\n"
            f"• Белки: {protein:.1f}г\n"
            f"• Жиры: {fat:.1f}г\n"
            f"• Углеводы: {carbs:.1f}г\n\n"
            f"*Сегодня:* {totals['calories']}/{user.daily_calories} ккал",
            parse_mode="Markdown", reply_markup=keyboard
        )
        await state.clear()
    except ValueError:
        await message.answer("⚠️ Пожалуйста, введи число (например: 150)")

@dp.callback_query(F.data == "today_food")
async def show_today_food(callback: types.CallbackQuery):
    entries = await DatabaseManager.get_today_food(callback.from_user.id)
    totals = await DatabaseManager.get_today_totals(callback.from_user.id)
    user = await DatabaseManager.get_user(callback.from_user.id)
    if not entries:
        await callback.message.edit_text(
            "📋 *Сегодня ты еще ничего не добавлял(а)*",
            parse_mode="Markdown", reply_markup=get_back_to_nutrition_button()
        )
        return
    text = "*📋 СЕГОДНЯШНИЙ РАЦИОН*\n\n"
    for i, entry in enumerate(entries, 1):
        text += f"{i}. {entry.food_name} - {entry.calories} ккал\n"
    text += f"\n*Итого:* {totals['calories']}/{user.daily_calories} ккал\n"
    text += f"*Белки:* {totals['protein']:.1f}г\n"
    text += f"*Жиры:* {totals['fat']:.1f}г\n"
    text += f"*Углеводы:* {totals['carbs']:.1f}г"
    await callback.message.edit_text(
        text, parse_mode="Markdown", reply_markup=get_back_to_nutrition_button()
    )

@dp.callback_query(F.data == "food_base")
async def food_base(callback: types.CallbackQuery):
    text = "*🍗 БАЗА ПРОДУКТОВ (КБЖУ на 100г)*\n\n"
    for name, data in list(FOODS.items())[:10]:
        text += f"• *{name.capitalize()}*: {data['kcal']} ккал, Б:{data['protein']}г, Ж:{data['fat']}г, У:{data['carbs']}г\n"
    text += f"\n📝 *Всего продуктов: {len(FOODS)}*"
    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=get_back_to_nutrition_button())

@dp.callback_query(F.data == "food_tips")
async def food_tips(callback: types.CallbackQuery):
    text = ("*🥑 СОВЕТЫ ПО ПИТАНИЮ*\n\n"
            "*ДЛЯ ПОХУДЕНИЯ:*\n"
            "• Дефицит калорий 10-20% от нормы\n"
            "• Больше белка (1.6-2г на кг веса)\n"
            "• Меньше быстрых углеводов (сладости, выпечка)\n"
            "• Продукты: курица, рыба, творог, яйца, овощи, гречка\n\n"
            "*ДЛЯ НАБОРА МАССЫ:*\n"
            "• Профицит калорий 10-20% от нормы\n"
            "• Достаточно углеводов до и после тренировки\n"
            "• Продукты: рис, макароны, картофель, мясо, орехи\n\n"
            "*ДЛЯ ПОДДЕРЖАНИЯ:*\n"
            "• Баланс БЖУ\n"
            "• Разнообразное питание\n"
            "• Контроль порций\n\n"
            "*ВОДА:* 30-40 мл на кг веса")
    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=get_back_to_nutrition_button())