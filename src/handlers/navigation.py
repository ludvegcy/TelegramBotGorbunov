from aiogram import types, F
from src.loader import dp
from src.keyboards import get_main_keyboard
from src.handlers.trainings import trainings_menu
from src.handlers.nutrition import nutrition_menu

@dp.callback_query(F.data == "back_to_main")
async def back_to_main(callback: types.CallbackQuery):
    keyboard = await get_main_keyboard(callback.from_user.id)
    await callback.message.delete()
    await callback.message.answer("Главное меню:", reply_markup=keyboard)

@dp.callback_query(F.data == "back_to_trainings")
async def back_to_trainings(callback: types.CallbackQuery):
    await callback.message.delete()
    await trainings_menu(callback.message)

@dp.callback_query(F.data == "back_to_nutrition")
async def back_to_nutrition(callback: types.CallbackQuery):
    await callback.message.delete()
    await nutrition_menu(callback.message)