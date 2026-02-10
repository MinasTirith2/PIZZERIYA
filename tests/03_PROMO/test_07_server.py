import logging
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Keys
import allure
import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


@allure.feature("Падение сервера")
@allure.story("Сервер упал")
@pytest.mark.regress
class TestPromoCod:
    @pytest.fixture(autouse=True)
    def setup(self, open_main_page):
        self.driver = open_main_page

    @allure.title("Кейс 19: Применение купона, Падение сервера")
    def test_coupon_G(self):
        with (allure.step("Авторизация на сайте")):
            self.driver.get("https://pizzeria.skillbox.cc/my-account/")
            self.driver.find_element(By.ID, "username").send_keys("Dmitryi")
            self.driver.find_element(By.ID, "password").send_keys("123456", Keys.ENTER)
            self.driver.get("https://pizzeria.skillbox.cc/product-category/menu/")
            time.sleep(2)
        with allure.step("добавляем товары в корзину"):
            p1 = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a[data-product_id='427']"))
            )
            self.driver.execute_script("arguments[0].click();", p1)
            p2 = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a[data-product_id='423']"))
            )
            self.driver.execute_script("arguments[0].click();", p2)
            time.sleep(2)
        with allure.step("Переходим в корзину"):
            self.driver.get("https://pizzeria.skillbox.cc/cart/")
            subtotal_text = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".cart-subtotal .amount"))
            ).text
            price_before = float(subtotal_text.replace("₽", "").replace(",", ".").replace(" ", "").strip())
        with allure.step("Включаем перехват сетевых запросов"):
            self.driver.execute_cdp_cmd('Network.enable', {})
            self.driver.execute_cdp_cmd('Network.setExtraHTTPHeaders', {
                "headers": {"X-Mock-Status": "500"}  # Это один из способов, если есть мок-прокси
            })
            self.driver.execute_cdp_cmd('Fetch.enable', {
                'patterns': [{'urlPattern': '*apply_coupon*', 'requestStage': 'Request'}]
            })

            def handle_request(event):
                self.driver.execute_cdp_cmd('Fetch.failRequest', {
                    'requestId': event['requestId'],
                    'errorReason': 'Failed'  # Имитируем сетевую ошибку
                })
            logging.info("Эмуляция падения сервера активирована")
        with allure.step("Применяем промокод GIVEMEHALYAVA"):
            coupon_input = self.driver.find_element(By.ID, "coupon_code")
            coupon_input.send_keys("GIVEMEHALYAVA")
            self.driver.find_element(By.NAME, "apply_coupon").click()
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, ".woocommerce-error"))
                )
                logging.info("Сайт корректно отобразил ошибку при падении сервера")
            except TimeoutException:
                logging.warning("Сообщение об ошибке не появилось, проверяем сумму")
            with allure.step("Проверка: сумма НЕ изменилась"):
                total_text = self.driver.find_element(By.CSS_SELECTOR, ".order-total .amount").text
                price_after = float(total_text.replace("₽", "").replace(",", ".").replace(" ", "").strip())
                assert price_after == price_before, f"Баг! Сервер лёг, но скидка прошла. Было {price_before}, стало {price_after}"
                logging.info(f"Тест пройден: цена осталась прежней ({price_after})")
