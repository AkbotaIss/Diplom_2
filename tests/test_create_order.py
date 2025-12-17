import requests
import allure


@allure.suite("Создание заказа")
class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией и валидными ингредиентами")
    def test_create_order_with_auth_and_ingredients(
        self, orders_url, auth_headers, valid_ingredient_ids
    ):
        payload = {"ingredients": valid_ingredient_ids}

        with allure.step("Отправляем запрос на создание заказа с токеном"):
            response = requests.post(orders_url, headers=auth_headers, json=payload)

        with allure.step("Проверяем успешный статус-код и номер заказа"):
            assert response.status_code == 200

            body = response.json()
            assert body["success"] is True
            assert "order" in body
            assert "number" in body["order"]

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth_with_ingredients(
        self, orders_url, valid_ingredient_ids
    ):
        payload = {"ingredients": valid_ingredient_ids}

        with allure.step("Отправляем запрос на создание заказа без токена"):
            response = requests.post(orders_url, json=payload)

        with allure.step("Проверяем фактическое поведение сервиса"):
            assert response.status_code == 200

            body = response.json()
            assert body["success"] is True
            assert "order" in body
            assert "number" in body["order"]

    @allure.title("Создание заказа без ингредиентов возвращает 400")
    def test_create_order_with_auth_without_ingredients(
        self, orders_url, auth_headers
    ):
        payload = {"ingredients": []}

        with allure.step("Отправляем запрос на создание заказа без ингредиентов"):
            response = requests.post(orders_url, headers=auth_headers, json=payload)

        with allure.step("Проверяем статус-код и текст ошибки"):
            assert response.status_code == 400

            body = response.json()
            assert body["success"] is False
            assert body["message"] == "Ingredient ids must be provided"

    @allure.title("Создание заказа с неверным хэшем ингредиента возвращает 500")
    def test_create_order_with_auth_and_invalid_ingredient_hash(
        self, orders_url, auth_headers
    ):
        payload = {"ingredients": ["invalid_ingredient_id"]}

        with allure.step("Отправляем запрос с невалидным идентификатором ингредиента"):
            response = requests.post(orders_url, headers=auth_headers, json=payload)

        with allure.step("Проверяем код 500 и HTML-страницу ошибки"):
            assert response.status_code == 500
            assert "Internal Server Error" in response.text
