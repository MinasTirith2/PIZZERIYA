import logging
import allure
import pytest
import time

from pages.cart_page import CartPage


@allure.feature("Падение сервера")
@allure.story("Сервер упал")
@pytest.mark.regress
class TestPromoCod:
    @pytest.fixture(autouse=True)
    def setup(self, open_main_page):
        self.driver = open_main_page

    @allure.title("Кейс 19: Применение купона, Падение сервера")
    def test_coupon_server_failure(self):
        cart_page = CartPage(self.driver)

        with allure.step("Подготовка: добавляем товар в корзину"):
            self.driver.get("https://pizzeria.skillbox.cc/?add-to-cart=427")

        with allure.step("Переходим в корзину и фиксируем цену"):
            self.driver.get("https://pizzeria.skillbox.cc/cart/")
            price_before = cart_page.get_price_subtotal()

        with allure.step("Включаем блокировку сетевых запросов"):
            self.driver.execute_cdp_cmd('Fetch.enable', {
                'patterns': [{'urlPattern': '*wc-ajax=apply_coupon*', 'requestStage': 'Request'}]
            })
            self.driver.execute_cdp_cmd('Network.setBlockedURLs', {
                'urls': ['*wc-ajax=apply_coupon*']
            })

        with allure.step("Попытка применить купон"):
            cart_page.type(cart_page.COUPON_INPUT, "GIVEMEHALYAVA")
            cart_page.click(cart_page.APPLY_COUPON_BTN)

            time.sleep(3)

        with allure.step("Проверка: сумма НЕ изменилась"):
            price_after = cart_page.get_price_total()

            self.driver.execute_cdp_cmd('Fetch.disable', {})
            self.driver.execute_cdp_cmd('Network.setBlockedURLs', {'urls': []})

            assert price_after == price_before, f"Скидка применилась при упавшем сервере! {price_before} -> {price_after}"