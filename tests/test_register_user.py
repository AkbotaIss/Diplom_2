import pytest
import requests
import allure


@allure.suite("Регистрация пользователя")
class TestRegisterUser:

    @allure.title("Создание уникального пользователя — успешная регистрация")
    def test_create_unique_user_success(self, register_url, new_user_data):
        with allure.step("Отправляем запрос на регистрацию нового пользователя"):
            response = requests.post(register_url, json=new_user_data)

        with allure.step("Проверяем успешный статус-код и тело ответа"):
            assert response.status_code == 200

            body = response.json()
            assert body["success"] is True
            assert "user" in body
            assert body["user"]["email"] == new_user_data["email"]

    @allure.title("Регистрация уже существующего пользователя возвращает 403")
    def test_create_existing_user_returns_403(self, register_url, new_user_data):
        with allure.step("Регистрируем пользователя первый раз"):
            first_response = requests.post(register_url, json=new_user_data)
            assert first_response.status_code == 200

        with allure.step("Пытаемся зарегистрировать пользователя повторно"):
            second_response = requests.post(register_url, json=new_user_data)

        with allure.step("Проверяем статус-код и сообщение об ошибке"):
            assert second_response.status_code == 403

            body = second_response.json()
            assert body["success"] is False
            assert body["message"] == "User already exists"

    @allure.title("Регистрация без обязательного поля возвращает 403")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_required_field_returns_403(
        self, register_url, new_user_data, missing_field
    ):
        with allure.step(f"Удаляем обязательное поле {missing_field} из тела запроса"):
            new_user_data.pop(missing_field)

        with allure.step("Отправляем запрос на регистрацию"):
            response = requests.post(register_url, json=new_user_data)

        with allure.step("Проверяем статус-код и текст ошибки"):
            assert response.status_code == 403

            body = response.json()
            assert body["success"] is False
            assert body["message"] == "Email, password and name are required fields"
