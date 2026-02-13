import logging
import allure
import pytest
import time
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


@allure.feature("Промокоды")
@allure.story("Промокоды GIVEMEHALYAVA ")
@pytest.mark.regress
class TestPromoCod:
    @pytest.fixture(autouse=True)
    def setup(self, open_main_page):
        self.driver = open_main_page

    @allure.title("Кейс 16: Применение купона GIVEMEHALYAVA")
    def test_coupon_giveme(self, user_data):
        checkout_page = CheckoutPage(self.driver)
        cart_page = CartPage(self.driver)
        try:

            with allure.step("Добавление товаров и переход на чекаут"):
                self.driver.get("https://pizzeria.skillbox.cc/?add-to-cart=427")
                self.driver.get("https://pizzeria.skillbox.cc/?add-to-cart=423")
                checkout_page.open("https://pizzeria.skillbox.cc/checkout/")
                logging.info("Добавляем товары, чтобы появились поля на чекауте")

            with allure.step("Авторизация на чекауте"):
                checkout_page.login_on_checkout("Dmitryi", "123456")
                logging.info("Вызываем правильный метод из твоего класса CheckoutPage")

            with allure.step("Переход в корзину для проверки купона"):
                cart_page.open("https://pizzeria.skillbox.cc/cart/")

            with allure.step("Применение купона и проверка цены"):
                price_before = cart_page.get_price_subtotal()
                cart_page.apply_coupon("GIVEMEHALYAVA")
                time.sleep(1)
                logging.info("Применение купона и проверка цены")
                price_after = cart_page.get_price_total()
                expected = round(price_before * 0.9, 2)

                assert price_after == expected, f"Ожидали {expected}, получили {price_after}"
        finally:
            checkout_page.logout()

    @allure.title("Кейс 17: Повторное применение купона (уже использованного)")
    def test_second_time_G(self, user_data):
        checkout_page = CheckoutPage(self.driver)
        cart_page = CartPage(self.driver)

        with allure.step("Авторизация и подготовка корзины"):
            self.driver.get("https://pizzeria.skillbox.cc/?add-to-cart=427")
            checkout_page.open("https://pizzeria.skillbox.cc/checkout/")
            checkout_page.login_on_checkout("Dmitryi", "123456")

        with allure.step("Переход в корзину"):
            cart_page.open("https://pizzeria.skillbox.cc/cart/")
            cart_page.remove_coupon_if_exists()
            price_before = cart_page.get_price_subtotal()
            logging.info("Очистка корзины от старых купонов")

        with allure.step("Попытка повторного применения купона"):
            cart_page.type(cart_page.COUPON_INPUT, "GIVEMEHALYAVA")
            cart_page.click(cart_page.APPLY_COUPON_BTN)

        with allure.step("Проверка результата"):
            notice_text = cart_page.get_any_notice()
            logging.info(f"Сайт ответил: {notice_text}")

            price_after = cart_page.get_price_total()

            if price_after != price_before:
                pytest.fail(f"БАГ! Купон применился (цена упала с {price_before} до {price_after}), "
                            f"хотя должен был отклониться как использованный!")
            assert "использован" in notice_text.lower() or "недействителен" in notice_text.lower()

        def teardown_method(self):
            self.driver.delete_all_cookies()
            self.driver.execute_script("window.localStorage.clear();")
            self.driver.execute_script("window.sessionStorage.clear();")

    @allure.title("Кейс 18: Применение несуществующего купона")
    def test_coupon_error_invalid(self):
        checkout_page = CheckoutPage(self.driver)
        cart_page = CartPage(self.driver)

        with allure.step("Авторизация и подготовка"):
            self.driver.get("https://pizzeria.skillbox.cc/?add-to-cart=427")
            checkout_page.open("https://pizzeria.skillbox.cc/checkout/")
            checkout_page.login_on_checkout("Dmitryi", "123456")

        with allure.step("Ввод неверного купона в корзине"):
            cart_page.open("https://pizzeria.skillbox.cc/cart/")
            cart_page.remove_coupon_if_exists()

            price_before = cart_page.get_price_subtotal()
            cart_page.apply_coupon("NOSUCHCOUPON123")

        with allure.step("Проверка сообщения об ошибке"):
            notice_text = cart_page.get_any_notice()
            logging.info(f"Сайт ответил: {notice_text}")

            price_after = cart_page.get_price_total()

            # 1. Проверяем, что цена не изменилась
            assert price_after == price_before, "Цена изменилась при неверном купоне!"
            # 2. Проверяем текст ошибки (в зависимости от языка сайта)
            assert "неверный купон." in notice_text.lower() or "does not exist" in notice_text.lower()

    def teardown_method(self):
        self.driver.delete_all_cookies()
        self.driver.execute_script("window.localStorage.clear();")
        self.driver.execute_script("window.sessionStorage.clear();")