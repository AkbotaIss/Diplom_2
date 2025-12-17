import pytest
import requests

from urls import REGISTER_URL, INGREDIENTS_URL
from helpers.data_generation import generate_random_email


@pytest.fixture
def new_user_data() -> dict:
    return {
        "email": generate_random_email(),
        "password": "password123",
        "name": "Test User",
    }


@pytest.fixture
def auth_headers(new_user_data) -> dict:
    """Регистрирует нового пользователя и возвращает заголовок Authorization."""
    response = requests.post(REGISTER_URL, json=new_user_data)
    assert response.status_code == 200

    body = response.json()
    access_token = body["accessToken"]  # 'Bearer ...'
    return {"Authorization": access_token}


@pytest.fixture
def valid_ingredient_ids() -> list[str]:
    """Получает список валидных id ингредиентов с сервера."""
    response = requests.get(INGREDIENTS_URL)
    response.raise_for_status()

    data = response.json()
    return [item["_id"] for item in data["data"][:3]]
