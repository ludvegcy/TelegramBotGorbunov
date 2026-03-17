"""Тесты для API эндпоинтов."""

import pytest
import json
from urllib.parse import parse_qs
from fastapi.testclient import TestClient
from webapp.server import app
from src.db import DatabaseManager

client = TestClient(app)

# Тестовые данные
TEST_USER_ID = 123456789
TEST_INIT_DATA = "query_id=AAHdF6IQAAAAAN0XohDhrOrc&user=%7B%22id%22%3A123456789%2C%22first_name%22%3A%22Test%22%2C%22last_name%22%3A%22User%22%7D&auth_date=1552773500&hash=abc123"


@pytest.fixture(autouse=True)
async def clear_db():
    """Очищает базу данных перед каждым тестом."""
    # В реальном проекте здесь должна быть очистка БД
    yield


def test_root_endpoint():
    """Тест главной страницы."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_get_user_not_found():
    """Тест получения несуществующего пользователя."""
    response = client.get(
        "/api/user",
        headers={"X-Init-Data": TEST_INIT_DATA}
    )
    assert response.status_code == 200
    assert response.json()["exists"] is False


def test_get_user_unauthorized():
    """Тест получения пользователя без авторизации."""
    response = client.get("/api/user")
    assert response.status_code == 401


def test_create_user():
    """Тест создания пользователя."""
    user_data = {
        "age": 25,
        "height": 175,
        "weight": 75.5,
        "gender": "male"
    }

    response = client.post(
        "/api/user",
        headers={
            "X-Init-Data": TEST_INIT_DATA,
            "Content-Type": "application/json"
        },
        json=user_data
    )

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["user_id"] == TEST_USER_ID


def test_update_user():
    """Тест обновления пользователя."""
    # Сначала создаем пользователя
    client.post(
        "/api/user",
        headers={"X-Init-Data": TEST_INIT_DATA},
        json={"age": 25}
    )

    # Обновляем данные
    update_data = {
        "age": 26,
        "weight": 80.0
    }

    response = client.post(
        "/api/user",
        headers={
            "X-Init-Data": TEST_INIT_DATA,
            "Content-Type": "application/json"
        },
        json=update_data
    )

    assert response.status_code == 200

    # Проверяем обновленные данные
    get_response = client.get(
        "/api/user",
        headers={"X-Init-Data": TEST_INIT_DATA}
    )

    user_data = get_response.json()
    assert user_data["age"] == 26
    assert user_data["weight"] == 80.0


def test_get_user_after_create():
    """Тест получения пользователя после создания."""
    # Создаем пользователя
    client.post(
        "/api/user",
        headers={"X-Init-Data": TEST_INIT_DATA},
        json={
            "age": 25,
            "height": 175,
            "weight": 75.5
        }
    )

    # Получаем данные
    response = client.get(
        "/api/user",
        headers={"X-Init-Data": TEST_INIT_DATA}
    )

    data = response.json()
    assert data["exists"] is True
    assert data["telegram_id"] == TEST_USER_ID
    assert data["first_name"] == "Test"  # Из initData
    assert data["age"] == 25
    assert data["height"] == 175
    assert data["weight"] == 75.5


def test_create_user_with_all_fields():
    """Тест создания пользователя со всеми полями."""
    user_data = {
        "first_name": "Custom",
        "last_name": "Name",
        "age": 30,
        "height": 180,
        "weight": 85.5,
        "gender": "male",
        "activity": "moderate",
        "goal": "weight_loss",
        "daily_calories": 2200
    }

    response = client.post(
        "/api/user",
        headers={
            "X-Init-Data": TEST_INIT_DATA,
            "Content-Type": "application/json"
        },
        json=user_data
    )

    assert response.status_code == 200

    # Проверяем сохраненные данные
    get_response = client.get(
        "/api/user",
        headers={"X-Init-Data": TEST_INIT_DATA}
    )

    saved_data = get_response.json()
    for key, value in user_data.items():
        assert saved_data[key] == value