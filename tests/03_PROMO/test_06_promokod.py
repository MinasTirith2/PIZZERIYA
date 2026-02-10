import logging
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Keys
import allure
import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


@allure.feature("Промокоды")
@allure.story("Промокоды GIVEMEHALYAVA ")
@pytest.mark.regress
class TestPromoCod:
    @pytest.fixture(autouse=True)
    def setup(self, open_main_page):
        self.driver = open_main_page

    @allure.title("Кейс 16: Применение купона GIVEMEHALYAVA")
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
        with allure.step("Применяем промокод GIVEMEHALYAVA"):
            coupon_input = self.driver.find_element(By.ID, "coupon_code")
            coupon_input.send_keys("GIVEMEHALYAVA")
            self.driver.find_element(By.NAME, "apply_coupon").click()
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".woocommerce-message"))
            )
            logging.info("Купон GIVEMEHALYAVA применён")
            time.sleep(5)
        with allure.step("Проверяем применение купона на цене"):
            total_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".order-total .amount"))
            )
            price_after_text = total_element.text.replace("₽", "").replace(",", ".").replace(" ", "").strip()
            price_after = float(price_after_text)
            expected_price = round(price_before * 0.9, 2)
            logging.info(f"До скидки: {price_before}, После: {price_after}, Ожидали: {expected_price}")
            assert price_after == expected_price, f"Скидка рассчитана неверно! Ожидали {expected_price}, получили {price_after}"
        with allure.step("Переход к оплате"):
            self.driver.find_element(By.CLASS_NAME, "checkout-button").click()
            fields = {
                "billing_first_name": "Dmitry",
                "billing_last_name": "Test",
                "billing_address_1": "Pizzeria St, 1",
                "billing_state": "Крайняя",
                "billing_city": "Moscow",
                "billing_postcode": "123456",
                "billing_phone": "89990001122",
                "billing_email": "tedt@test.co"
            }
            for field_id, value in fields.items():
                input_field = self.driver.find_element(By.ID, field_id)
                input_field.clear()
                input_field.send_keys(value)
        with allure.step("Выбор способа оплаты и подтверждение условий"):
            payment_method = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "payment_method_cod"))
            )
            if not payment_method.is_selected():
                self.driver.execute_script("arguments[0].click();", payment_method)
            terms_checkbox = self.driver.find_element(By.ID, "terms")
            self.driver.execute_script("arguments[0].click();", terms_checkbox)
        with allure.step("Нажатие кнопки 'Оформить заказ'"):
            place_order_btn = self.driver.find_element(By.ID, "place_order")
            self.driver.execute_script("arguments[0].scrollIntoView(true);", place_order_btn)
            time.sleep(1)
            place_order_btn.click()
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "woocommerce-thankyou-order-received"))
            )
            logging.info("Заказ успешно оформлен")
        time.sleep(1)
        with allure.step("Выход из системы сразу после заказа"):
            logout_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "logout"))
            )
            self.driver.get(logout_btn.get_attribute("href"))

            try:
                confirm = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='customer-logout']"))
                )
                confirm.click()
            except TimeoutException:
                pass

            WebDriverWait(self.driver, 15).until(
                EC.url_to_be("https://pizzeria.skillbox.cc/")
            )
            logging.info("Пользователь разлогинен и перенаправлен на главную")

    @allure.title("Кейс 17: Повторное применение купона GIVEMEHALYAVA")
    def test_second_time_G(self):
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
        with allure.step("Применяем промокод GIVEMEHALYAVA"):
            coupon_input = self.driver.find_element(By.ID, "coupon_code")
            coupon_input.send_keys("GIVEMEHALYAVA")
            self.driver.find_element(By.NAME, "apply_coupon").click()
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".woocommerce-message"))
            )
            logging.info("Купон GIVEMEHALYAVA применён")
            time.sleep(5)
        with allure.step("Проверка: купон НЕ должен был примениться"):
            total_element = self.driver.find_element(By.CSS_SELECTOR, ".order-total .amount")
            price_after = float(total_element.text.replace("₽", "").replace(",", ".").replace(" ", "").strip())
            logging.info(f"До применения: {price_before}, После: {price_after}")
            assert price_after == price_before, (
                f"БАГ! Купон применился повторно для одного и того же пользователя. "
                f"Цена до: {price_before}, Цена после: {price_after}"
            )
            logging.info("Тест пройден: купон не применился повторно, сумма осталась прежней.")

    @allure.title("Кейс 18: Применение купона DC120")
    def test_coupon_DC120(self):
        with allure.step("Удаляем предыдущий промокод"):
            self.driver.find_element(By.CLASS_NAME, "woocommerce-remove-coupon").click()
            logging.info("Предыдущий купон успешно удален")
            time.sleep(1)
        with allure.step("Применяем промокод DC120"):
            apply_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.NAME, "apply_coupon"))
            )
            coupon_input = self.driver.find_element(By.ID, "coupon_code")
            coupon_input.send_keys("DC120")
            apply_btn.click()
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".woocommerce-message"))
            )
            logging.info("Купон DC120 введён")
            subtotal_text = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".cart-subtotal .amount"))
            ).text
            price_before = float(subtotal_text.replace("₽", "").replace(",", ".").replace(" ", "").strip())
        with allure.step("Проверяем наличие ошибки и неизменность цены"):
            error_msg = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".woocommerce-error"))
            ).text
            logging.info(f"Получена ошибка: {error_msg}")
            total_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".order-total .amount"))
            )
            total_text = total_element.text
            price_after = float(total_text.replace("₽", "").replace(",", ".").replace(" ", "").strip())
            assert price_before == price_after, f"Цена изменилась, а не должна была! Была {price_before}, стала {price_after}"
