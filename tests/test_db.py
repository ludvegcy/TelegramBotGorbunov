"""Тесты для работы с базой данных."""

import pytest
import asyncio
from datetime import datetime, timedelta
from src.db import DatabaseManager, AsyncSessionLocal, engine
from src.models import Base, User


@pytest.fixture(scope="session")
def event_loop():
    """Создает event loop для тестов."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True)
async def setup_database():
    """Создает таблицы перед тестами и удаляет после."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.mark.asyncio
async def test_create_user():
    """Тест создания пользователя."""
    user = await DatabaseManager.create_user(
        telegram_id=123456789,
        first_name="Test",
        last_name="User",
        age=25,
        height=175,
        weight=75.5,
        gender="male"
    )

    assert user is not None
    assert user.telegram_id == 123456789
    assert user.first_name == "Test"
    assert user.last_name == "User"
    assert user.age == 25


@pytest.mark.asyncio
async def test_get_user():
    """Тест получения пользователя."""
    # Создаем пользователя
    await DatabaseManager.create_user(telegram_id=123456789)

    # Получаем пользователя
    user = await DatabaseManager.get_user(123456789)

    assert user is not None
    assert user.telegram_id == 123456789


@pytest.mark.asyncio
async def test_update_user():
    """Тест обновления пользователя."""
    # Создаем пользователя
    await DatabaseManager.create_user(telegram_id=123456789)

    # Обновляем данные
    updated = await DatabaseManager.update_user(
        123456789,
        weight=80.0,
        age=26
    )

    assert updated is not None
    assert updated.weight == 80.0
    assert updated.age == 26


@pytest.mark.asyncio
async def test_add_weight_entry():
    """Тест добавления записи веса."""
    # Создаем пользователя
    user = await DatabaseManager.create_user(telegram_id=123456789)

    # Добавляем запись веса
    entry = await DatabaseManager.add_weight_entry(123456789, 75.5)

    assert entry is not None
    assert entry.weight == 75.5


@pytest.mark.asyncio
async def test_get_weight_history():
    """Тест получения истории веса."""
    # Создаем пользователя
    await DatabaseManager.create_user(telegram_id=123456789)

    # Добавляем несколько записей
    await DatabaseManager.add_weight_entry(123456789, 75.5)
    await DatabaseManager.add_weight_entry(123456789, 74.8)
    await DatabaseManager.add_weight_entry(123456789, 74.2)

    # Получаем историю
    history = await DatabaseManager.get_weight_history(123456789, days=30)

    assert len(history) == 3
    assert history[0].weight == 75.5


@pytest.mark.asyncio
async def test_add_food_entry():
    """Тест добавления записи о еде."""
    # Создаем пользователя
    await DatabaseManager.create_user(telegram_id=123456789)

    # Добавляем запись о еде
    entry = await DatabaseManager.add_food_entry(
        123456789,
        "курица",
        250,
        25.0,
        5.0,
        0.0
    )

    assert entry is not None
    assert entry.food_name == "курица"
    assert entry.calories == 250


@pytest.mark.asyncio
async def test_get_today_food():
    """Тест получения сегодняшней еды."""
    # Создаем пользователя
    await DatabaseManager.create_user(telegram_id=123456789)

    # Добавляем записи
    await DatabaseManager.add_food_entry(123456789, "курица", 250, 25, 5, 0)
    await DatabaseManager.add_food_entry(123456789, "гречка", 200, 6, 2, 40)

    # Получаем сегодняшнюю еду
    entries = await DatabaseManager.get_today_food(123456789)

    assert len(entries) == 2
    assert entries[0].food_name == "курица"
    assert entries[1].food_name == "гречка"


@pytest.mark.asyncio
async def test_get_today_totals():
    """Тест получения итогов за сегодня."""
    # Создаем пользователя
    user = await DatabaseManager.create_user(
        telegram_id=123456789,
        daily_calories=2000
    )

    # Добавляем записи
    await DatabaseManager.add_food_entry(123456789, "курица", 250, 25, 5, 0)
    await DatabaseManager.add_food_entry(123456789, "гречка", 200, 6, 2, 40)

    # Получаем итоги
    totals = await DatabaseManager.get_today_totals(123456789)

    assert totals['calories'] == 450
    assert totals['protein'] == 31.0
    assert totals['fat'] == 7.0
    assert totals['carbs'] == 40.0


@pytest.mark.asyncio
async def test_premium_user():
    """Тест премиум статуса пользователя."""
    # Создаем премиум пользователя
    premium_until = datetime.now() + timedelta(days=30)
    user = await DatabaseManager.create_user(
        telegram_id=123456789,
        is_premium=True,
        premium_until=premium_until
    )

    assert user.is_premium is True
    assert user.premium_until is not None


@pytest.mark.asyncio
async def test_get_users_count():
    """Тест подсчета пользователей."""
    # Создаем несколько пользователей
    await DatabaseManager.create_user(telegram_id=1)
    await DatabaseManager.create_user(telegram_id=2, is_premium=True)
    await DatabaseManager.create_user(telegram_id=3)

    total = await DatabaseManager.get_all_users_count()
    premium = await DatabaseManager.get_premium_users_count()

    assert total == 3
    assert premium == 1