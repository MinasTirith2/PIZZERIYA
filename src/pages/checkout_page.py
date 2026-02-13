import logging
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage

class CheckoutPage(BasePage):
    SHOW_LOGIN = (By.CLASS_NAME, "showlogin")
    LOGIN_INPUT = (By.ID, "username")
    PASS_INPUT = (By.ID, "password")
    LOGIN_SUBMIT = (By.NAME, "login")
    BILLING_FIRST_NAME = (By.ID, "billing_first_name")
    EMAIL_FIELD = (By.ID, "billing_email")
    COD_PAYMENT_LABEL = (By.CSS_SELECTOR, "label[for='payment_method_cod']")
    TERMS_CHECKBOX = (By.ID, "terms")
    SUCCESS_NOTICE = (By.CSS_SELECTOR, ".woocommerce-notice--success")
    ERROR_NOTICE = (By.CSS_SELECTOR, ".woocommerce-error")

    def login_on_checkout(self, email, password):
        show_login_link = self.find(self.SHOW_LOGIN)
        self.driver.execute_script("arguments[0].click();", show_login_link)

        user_input = self.wait.until(
            EC.visibility_of_element_located(self.LOGIN_INPUT)
        )

        user_input.clear()
        user_input.send_keys(email)
        self.type(self.PASS_INPUT, password)

        login_btn = self.find(self.LOGIN_SUBMIT)
        self.driver.execute_script("arguments[0].click();", login_btn)

        self.wait.until(EC.invisibility_of_element_located(self.LOGIN_SUBMIT))

    def is_billing_visible(self):
        try:
            element = self.wait.until(
                EC.visibility_of_element_located(self.BILLING_FIRST_NAME)
            )
            return element.is_displayed()
        except:
            return False

    def fill_billing_form(self, first_name, last_name, email):
        logging.info("Начинаю заполнение полей заказ")
        self.type(self.BILLING_FIRST_NAME, first_name)
        self.type((By.ID, "billing_last_name"), last_name)
        self.type((By.ID, "billing_address_1"), "Ул. Тестовая 10")
        self.type((By.ID, "billing_city"), "Алматы")
        self.type((By.ID, "billing_state"), "МО")
        self.type((By.ID, "billing_postcode"), "123456")
        self.type((By.ID, "billing_phone"), "87761234567")
        self.type(self.EMAIL_FIELD, email)

    def select_cod_and_accept_terms(self):
        logging.info("Выбираю оплату при доставке и принимаю условия")
        self.click(self.COD_PAYMENT_LABEL)
        self.click(self.TERMS_CHECKBOX)

    def place_order(self):
        logging.info("Нажимаю кнопку оформления заказа")
        btn = self.find((By.ID, "place_order"))
        self.scroll_to_element(btn)
        self.click(btn)

    def get_success_message(self):
        return self.find(self.SUCCESS_NOTICE).text

    def logout(self):
        self.open("https://pizzeria.skillbox.cc/my-account/customer-logout/")
        confirm = self.find((By.CSS_SELECTOR, "a[href*='customer-logout']"))
        self.click(confirm)

    def get_error_message(self):
        return self.find(self.ERROR_NOTICE).text