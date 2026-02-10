import logging
from selenium.webdriver.support import expected_conditions as EC
import allure
import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


@allure.feature("Регистрация")
@allure.story("Регистрация через МОЙ АККАУНТ")
@pytest.mark.regress
class TestSignUp:
    @pytest.fixture(autouse=True)
    def setup(self, open_main_page):
        self.driver = open_main_page

    @allure.title("Кейс 13: Успешная регистрации через МОЙ АККАУНТ с валидными данными")
    def test_sign_up(self):
        timestamp = int(time.time())
        self.__class__.generated_login = f"R{timestamp}"
        self.__class__.generated_email = f"{timestamp}@j.co"
        self.__class__.user_pass = "123456"
        with allure.step("Переход в 'Мой Аккаунт'"):
            self.driver.find_element(By.CSS_SELECTOR, "#menu-item-30 > a").click()
        with allure.step("Нажатие кнопки 'Зарегистрироваться' для перехода к форме"):
            reg_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "custom-register-button"))
            )
            reg_btn.click()
        with allure.step(f"Заполнение полей (Логин: {self.generated_login})"):
            self.driver.find_element(By.ID, "reg_username").send_keys(self.generated_login)
            self.driver.find_element(By.ID, "reg_email").send_keys(self.generated_email)
            self.driver.find_element(By.ID, "reg_password").send_keys("123456")
        with allure.step("Нажатие финальной кнопки регистрации"):
            self.driver.find_element(By.NAME, "register").click()
        with allure.step("Проверка успешной регистрации"):
            result_header = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h2.post-title"))
            ).text
            logging.info(f"Текст заголовка после регистрации: {result_header}")
            assert "РЕГИСТРАЦИЯ" in result_header.upper() or "МОЙ АККАУНТ" in result_header.upper()
            time.sleep(5)

    @allure.title("Кейс 14: Авторизация через оформление заказа")
    def test_auth_on_checkout(self):
        with allure.step("Выход из аккаунта"):
            self.driver.find_element(By.CLASS_NAME, "logout").click()
            time.sleep(2)
        with allure.step("Добавление двух пицц в корзину"):
            time.sleep(1)
            self.driver.find_element(By.CSS_SELECTOR, "a[data-product_id='425']").click()
            time.sleep(1)
            pizza2 = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a[data-product_id='423']"))
            )
            self.driver.execute_script("arguments[0].click();", pizza2)
            logging.info("Обе пиццы добавлены через JS-click")
            time.sleep(1)
        with allure.step("Переход к оплате"):
            self.driver.find_element(By.CLASS_NAME, "cart-contents").click()
            self.driver.find_element(By.CLASS_NAME, "checkout-button").click()
            time.sleep(1)
        with allure.step("Авторизация на чекауте"):
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "showlogin"))
            ).click()
            time.sleep(1)
            user_input = self.driver.find_element(By.ID, "username")
            user_input.clear()
            user_input.send_keys(self.generated_email)
            pass_input = self.driver.find_element(By.ID, "password")
            pass_input.clear()
            pass_input.send_keys("123456")
            self.driver.find_element(By.NAME, "login").click()
        with allure.step("Проверка: поля оформления доступны"):
            billing_name = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "billing_first_name"))
            )
            assert billing_name.is_displayed()

    @allure.title("Кейс 15: Оформление заказа")
    def test_checkout_order(self):
        ts = int(time.time())
        with allure.step("Заполнение данных покупателя"):
            fields = {
                "billing_first_name": f"И{ts}",
                "billing_last_name": f"Ф{ts}",
                "billing_address_1": f"Ул. Тестовая, дом {ts % 100}",
                "billing_city": "Алматы",
                "billing_state": "МО",
                "billing_postcode": "123456",
                "billing_phone": f"8776{ts % 10000000:07d}"
            }
            for field_id, value in fields.items():
                element = self.driver.find_element(By.ID, field_id)
                element.clear()
                element.send_keys(value)

            email_field = self.driver.find_element(By.ID, "billing_email")
            email_field.clear()
            email_field.send_keys(self.generated_email)
        with allure.step("Выбор способа оплаты и принятие условий"):
            cod_payment = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='payment_method_cod']"))
            )
            cod_payment.click()

            terms_checkbox = self.driver.find_element(By.ID, "terms")
            self.driver.execute_script("arguments[0].click();", terms_checkbox)
        with allure.step("Нажатие кнопки 'Оформить заказ'"):
            place_order_btn = self.driver.find_element(By.ID, "place_order")
            self.driver.execute_script("arguments[0].scrollIntoView(true);", place_order_btn)
            time.sleep(1)
            place_order_btn.click()
        with allure.step("Проверка завершения заказа"):
            time.sleep(4)
            success_msg = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".woocommerce-notice--success"))
            ).text
            logging.info(f"Результат заказа: {success_msg}")
            assert "получен" in success_msg.lower() or "thank you" in success_msg.lower()
