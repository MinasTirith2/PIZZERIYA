import logging
from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC


class CartPage(BasePage):
    COUPON_INPUT = (By.ID, "coupon_code")
    APPLY_COUPON_BTN = (By.NAME, "apply_coupon")
    SUBTOTAL_PRICE = (By.CSS_SELECTOR, ".cart-subtotal .amount")
    TOTAL_PRICE = (By.CSS_SELECTOR, ".order-total .amount")
    REMOVE_COUPON_LINK = (By.CLASS_NAME, "woocommerce-remove-coupon")

    ANY_NOTICE = (By.CSS_SELECTOR, ".woocommerce-error, .woocommerce-message")

    def apply_coupon(self, code):
        self.type(self.COUPON_INPUT, code)
        self.click(self.APPLY_COUPON_BTN)
        self.wait.until(
            lambda d: d.find_element(*self.SUCCESS_NOTICE) or d.find_element(*self.ERROR_NOTICE)
        )

    def get_price_subtotal(self):
        return self._parse_price(self.find(self.SUBTOTAL_PRICE).text)

    def get_price_total(self):
        return self._parse_price(self.find(self.TOTAL_PRICE).text)

    def remove_coupon_if_exists(self):
        try:
            element = self.driver.find_element(*self.REMOVE_COUPON_LINK)
            element.click()
        except:
            pass

    def _parse_price(self, price_str):
        clean_price = price_str.replace("₽", "").replace(",", ".").replace(" ", "").strip()
        return float(clean_price)

    def get_error_message(self):
        return self.find(self.ERROR_NOTICE).text

    def apply_coupon(self, code):
        self.type(self.COUPON_INPUT, code)
        self.click(self.APPLY_COUPON_BTN)

    def get_price_subtotal(self):
        return self._parse_price(self.find(self.SUBTOTAL_PRICE).text)

    def get_price_total(self):
        return self._parse_price(self.find(self.TOTAL_PRICE).text)

    def remove_coupon_if_exists(self):
        try:
            self.driver.find_element(*self.REMOVE_COUPON_LINK).click()
            logging.info("Старый купон удален")
        except:
            pass

    def _parse_price(self, price_str):
        clean_price = price_str.replace("₽", "").replace(",", ".").replace(" ", "").strip()
        return float(clean_price)

    def get_any_notice(self):
        locator = (By.CSS_SELECTOR, ".woocommerce-error, .woocommerce-message")
        return self.find(locator).text

    def apply_coupon(self, code):
        self.type(self.COUPON_INPUT, code)
        self.click(self.APPLY_COUPON_BTN)
        # Ждем, пока появится ХОТЯ БЫ ОДНО сообщение (успех или ошибка)
        # Это критически важно для синхронизации с AJAX
        self.wait.until(
            EC.presence_of_element_located(self.ANY_NOTICE),
            message=f"Сообщение после применения купона {code} не появилось"
        )

    def get_price_subtotal(self):
        element = self.find(self.SUBTOTAL_PRICE)
        return self._parse_price(element.text)

    def get_price_total(self):
        element = self.find(self.TOTAL_PRICE)
        return self._parse_price(element.text)

    def remove_coupon_if_exists(self):
        try:
            # Используем find_elements, чтобы не ждать таймаут, если купона нет
            elements = self.driver.find_elements(*self.REMOVE_COUPON_LINK)
            if elements:
                elements[0].click()
                # Ждем, пока индикатор загрузки (если есть) исчезнет или цена обновится
                self.wait.until(EC.staleness_of(elements[0]))
                logging.info("Старый купон удален")
        except Exception as e:
            logging.warning(f"Не удалось удалить купон: {e}")

    def get_any_notice(self):
        return self.find(self.ANY_NOTICE).text

    def _parse_price(self, price_str):
        clean_price = price_str.replace("₽", "").replace(",", ".").replace("\xa0", "").replace(" ", "").strip()
        return float(clean_price)