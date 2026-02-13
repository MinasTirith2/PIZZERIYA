import logging
import allure
import pytest
import time
from selenium.webdriver.common.by import By
from src.pages.register_page import RegisterPage
from src.pages.checkout_page import CheckoutPage


@allure.feature("Регистрация")
@allure.story("Регистрация через МОЙ АККАУНТ")
@pytest.mark.regress
class TestSignUp:
    @pytest.fixture(autouse=True)
    def setup(self, open_main_page):
        self.driver = open_main_page

    @allure.title("Кейс 13: Успешная регистрация")
    def test_sign_up(self, user_data):
        login = user_data["login"]
        email = user_data["email"]
        with allure.step("Переходим на страницу МОЙ АККАУНТ"):
            self.driver.get("http://pizzeria.skillbox.cc/register/")
            logging.info("Выполнен переход в МОЙ АККАУНТ")

        with allure.step(f"Заполнение полей для {login}"):
            self.driver.find_element(By.ID, "reg_username").send_keys(login)
            self.driver.find_element(By.ID, "reg_email").send_keys(email)
            self.driver.find_element(By.ID, "reg_password").send_keys(user_data["pass"])
            logging.info("Все поля заполнены")

    @allure.title("Кейс 14: Авторизация через оформление заказа")
    def test_auth_on_checkout(self, user_data):
        reg_page = RegisterPage(self.driver)
        checkout_page = CheckoutPage(self.driver)

        with allure.step("Предусловие: Регистрация и очистка кук"):
            reg_page.register_new_user(user_data["login"], user_data["email"], user_data["pass"])
            time.sleep(1)
            reg_page.delete_cookies()

        with allure.step("Добавление товара и переход к оплате"):
            self.driver.get("https://pizzeria.skillbox.cc/?add-to-cart=425")
            checkout_page.open("https://pizzeria.skillbox.cc/checkout/")
            logging.info("Товар добавлен")

        with allure.step("Авторизация на чекауте"):
            checkout_page.login_on_checkout(user_data["email"], user_data["pass"])
            logging.info("Авторизация прошла")


        with allure.step("Проверка: Авторизация успешна (поля доступны)"):
            result = checkout_page.is_billing_visible()
            assert result is True, "Авторизация не удалась или поля биллинга не подгрузились"

    @allure.title("Кейс 15: Оформление заказа (POM стиль)")
    def test_checkout_order(self, user_data):
        reg_page = RegisterPage(self.driver)
        checkout_page = CheckoutPage(self.driver)
        logging.info("Начат кейс 15")

        with allure.step("Предусловие: Регистрация и подготовка корзины"):
            reg_page.register_new_user(user_data["login"], user_data["email"], user_data["pass"])
            reg_page.delete_cookies()  # Очистим, чтобы зайти именно через форму чекаута

            self.driver.get("https://pizzeria.skillbox.cc/?add-to-cart=425")
            checkout_page.open("https://pizzeria.skillbox.cc/checkout/")
            logging.info("Товар добавлен")

        with allure.step("Авторизация на чекауте"):
            checkout_page.login_on_checkout(user_data["email"], user_data["pass"])

        with allure.step("Заполнение данных покупателя"):
            checkout_page.fill_billing_form(
                user_data["first_name"],
                user_data["last_name"],
                user_data["email"]
            )

        with allure.step("Финальное оформление"):
            checkout_page.select_cod_and_accept_terms()
            checkout_page.place_order()

            msg = checkout_page.get_success_message()
            assert "получен" in msg.lower()