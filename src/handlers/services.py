from aiogram import types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice, PreCheckoutQuery
from datetime import datetime, timedelta
import re
from src.loader import dp, bot
from src.payments import TARIFFS, show_tariffs, get_back_to_tariffs_button
from src.config import PAYMENT_CONTACT, PREMIUM_STARS_PRICE
from src.db import DatabaseManager, AsyncSessionLocal
from src.models import Payment, PaymentMethod, PaymentStatus

@dp.message(F.text == "💰 Услуги")
async def services_menu(message: types.Message):
    await show_tariffs(message)

@dp.callback_query(F.data.startswith("tariff_"))
async def show_tariff_detail(callback: types.CallbackQuery):
    tariff_id = callback.data.replace("tariff_", "")
    tariff = TARIFFS.get(tariff_id)
    if not tariff:
        await callback.answer("Тариф не найден")
        return

    text = (
        f"{tariff['description']}\n\n"
        f"*Стоимость:* {tariff['price']}₽\n"
        f"*Длительность:* {tariff['duration']}\n\n"
        f"👇 *Выберите способ оплаты:*"
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⭐️ Оплатить Stars", callback_data=f"pay_stars_{tariff_id}")],
        [InlineKeyboardButton(text="◀ К тарифам", callback_data="show_tariffs")]
    ])

    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=kb)

# ------------------ Telegram Stars ------------------
@dp.callback_query(F.data.startswith("pay_stars_"))
async def confirm_stars_payment(callback: types.CallbackQuery):
    await callback.answer()
    tariff_id = callback.data.replace("pay_stars_", "")
    tariff = TARIFFS.get(tariff_id)
    if not tariff:
        await callback.message.answer("Тариф не найден")
        return

    # Показываем подтверждение перед отправкой счёта
    text = (
        f"⭐️ *Оплата через Telegram Stars*\n\n"
        f"*Тариф:* {tariff['name']}\n"
        f"*Стоимость:* {PREMIUM_STARS_PRICE} Stars\n"
        f"*Длительность:* {tariff['duration']}\n\n"
        f"Подтвердите оплату или вернитесь назад."
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Подтвердить оплату", callback_data=f"confirm_stars_{tariff_id}")],
        [InlineKeyboardButton(text="◀ Назад", callback_data="show_tariffs")]
    ])

    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=kb)

@dp.callback_query(F.data.startswith("confirm_stars_"))
async def process_stars_payment(callback: types.CallbackQuery):
    await callback.answer()
    tariff_id = callback.data.replace("confirm_stars_", "")
    tariff = TARIFFS.get(tariff_id)
    if not tariff:
        await callback.message.answer("Тариф не найден")
        return

    user = await DatabaseManager.get_user(callback.from_user.id)
    if not user:
        user = await DatabaseManager.create_user(telegram_id=callback.from_user.id)

    # Создаём запись о платеже
    async with AsyncSessionLocal() as session:
        payment = Payment(
            user_id=user.id,
            tariff_id=tariff_id,
            amount=PREMIUM_STARS_PRICE,
            currency="XTR",
            payment_method=PaymentMethod.STARS,
            status=PaymentStatus.PENDING
        )
        session.add(payment)
        await session.commit()
        await session.refresh(payment)

    # Отправляем счёт
    prices = [LabeledPrice(label="Премиум-доступ", amount=PREMIUM_STARS_PRICE)]
    await callback.message.answer_invoice(
        title="Оплата премиум-доступа",
        description=f"Тариф: {tariff['name']}\nДлительность: {tariff['duration']}",
        payload=f"premium_{payment.id}",
        provider_token="",
        currency="XTR",
        prices=prices,
        start_parameter="premium-payment"
    )

@dp.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_q: PreCheckoutQuery):
    await pre_checkout_q.answer(ok=True)

@dp.message(F.successful_payment)
async def successful_payment_handler(message: types.Message):
    payment_info = message.successful_payment
    payload = payment_info.invoice_payload

    if payload.startswith("premium_"):
        payment_id = int(payload.split("_")[1])

        async with AsyncSessionLocal() as session:
            payment = await session.get(Payment, payment_id)
            if payment and payment.status == PaymentStatus.PENDING:
                payment.status = PaymentStatus.PAID
                payment.provider_payment_id = payment_info.telegram_payment_charge_id
                await session.commit()

                user = await DatabaseManager.get_user(message.from_user.id)
                if user:
                    tariff = TARIFFS.get(payment.tariff_id)
                    days = 30
                    if tariff:
                        match = re.search(r'(\d+)', tariff['duration'])
                        if match:
                            days = int(match.group(1))
                        elif "месяц" in tariff['duration']:
                            days = 30
                        elif "пол года" in tariff['duration']:
                            days = 180

                    await DatabaseManager.update_user(
                        user.telegram_id,
                        is_premium=True,
                        premium_until=datetime.now() + timedelta(days=days)
                    )

        await message.answer(
            "✅ Оплата прошла успешно! Премиум-доступ активирован.",
            reply_markup=get_back_to_tariffs_button()
        )

# ------------------ Возврат к тарифам ------------------
@dp.callback_query(F.data == "show_tariffs")
async def back_to_tariffs(callback: types.CallbackQuery):
    await show_tariffs(callback)