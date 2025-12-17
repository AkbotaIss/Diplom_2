import requests
import allure


@allure.suite("Авторизация пользователя")
class TestLoginUser:

    @allure.title("Успешный вход под существующим пользователем")
    def test_login_existing_user_success(
        self, register_url, login_url, new_user_data
    ):
        with allure.step("Регистрируем нового пользователя"):
            register_response = requests.post(register_url, json=new_user_data)
            assert register_response.status_code == 200

        login_payload = {
            "email": new_user_data["email"],
            "password": new_user_data["password"],
        }

        with allure.step("Отправляем запрос на авторизацию"):
            login_response = requests.post(login_url, json=login_payload)

        with allure.step("Проверяем успешный статус-код и токены"):
            assert login_response.status_code == 200

            body = login_response.json()
            assert body["success"] is True
            assert "accessToken" in body
            assert "refreshToken" in body
            assert body["user"]["email"] == new_user_data["email"]

    @allure.title("Вход с неверным паролем возвращает 401")
    def test_login_with_incorrect_password_returns_401(
        self, register_url, login_url, new_user_data
    ):
        with allure.step("Регистрируем пользователя"):
            register_response = requests.post(register_url, json=new_user_data)
            assert register_response.status_code == 200

        wrong_credentials = {
            "email": new_user_data["email"],
            "password": "wrong_password",
        }

        with allure.step("Пытаемся авторизоваться с неверным паролем"):
            login_response = requests.post(login_url, json=wrong_credentials)

        with allure.step("Проверяем статус-код 401 и текст ошибки"):
            assert login_response.status_code == 401

            body = login_response.json()
            assert body["success"] is False
            assert body["message"] == "email or password are incorrect"
