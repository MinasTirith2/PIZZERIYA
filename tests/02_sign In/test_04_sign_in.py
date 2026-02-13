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
        self.driver.get("https://pizzeria.skillbox.cc/")

        with allure.step("Добавление любого товара в корзину"):
            add_buttons_locator = (By.CLASS_NAME, "add_to_cart_button")
            logging.info(f"Товар добавлен в корзину")
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(add_buttons_locator)
            )

            all_buttons = self.driver.find_elements(*add_buttons_locator)
            target_button = all_buttons[0]

            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_button)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", target_button)

        with allure.step("Ожидание обновления корзины и переход"):
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a.added_to_cart"))
            )
            self.driver.get("https://pizzeria.skillbox.cc/cart/")
            logging.info("Переходим в корзину")

        with allure.step("Переход к оплате"):
            checkout_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.checkout-button"))
            )
            checkout_btn.click()

        with allure.step("Проверка ссылки на авторизацию"):
            login_link = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "a.showlogin"))
            )
            assert login_link.is_displayed(), "Ссылка 'Авторизуйтесь' не видна!"