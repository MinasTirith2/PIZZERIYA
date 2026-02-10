import logging
from selenium.webdriver.support import expected_conditions as EC
import allure
import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


@allure.feature("Авторизация")
@allure.story("Авторизация через корзину")
@pytest.mark.regress
class TestSignIn:
    @pytest.fixture(autouse=True)
    def setup(self, open_main_page):
        self.driver = open_main_page

    @allure.title("Кейс 12: Авторизация через оформление заказа")
    def test_auth_at_checkout(self):
        with allure.step("Добавление первого товара в корзину"):
            add_button = self.driver.find_element(By.CSS_SELECTOR, "a[data-product_id='425']")
            add_button.click()
            time.sleep(2)
        with allure.step("Переход в корзину через шапку"):
            cart_icon = self.driver.find_element(By.CSS_SELECTOR, "a.cart-contents")
            cart_icon.click()
        with allure.step("Нажатие 'ПЕРЕЙТИ К ОПЛАТЕ'"):
            checkout_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.checkout-button"))
            )
            checkout_btn.click()
        with allure.step("Проверка ссылки на авторизацию"):
            login_link = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a.showlogin"))
            )
            logging.info(f"Ссылка на вход найдена: {login_link.text}")
            assert login_link.is_displayed(), "Ссылка 'Авторизуйтесь' не видна на странице!"
