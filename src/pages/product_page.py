from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage
import time
from selenium.webdriver.support import expected_conditions as EC


class ProductPage(BasePage):
    # Локаторы страницы товара
    PRODUCT_TITLE = (By.CSS_SELECTOR, "h1.product_title")
    PRICE_AMOUNT = (By.CSS_SELECTOR, "p.price .amount")
    BORDER_DROPDOWN = (By.ID, "board_pack")

    def get_product_name(self):
        """Возвращает название пиццы на странице товара."""
        return self.find_element(self.PRODUCT_TITLE).text.strip().upper()

    def get_price(self):
        """Парсит цену и возвращает её как число."""
        element = self.find_element(self.PRICE_AMOUNT)
        text_price = element.text.replace('₽', '').replace(',', '.').strip()
        return float(text_price)

    def select_border(self, partial_text):
        """Выбирает опцию, если текст опции содержит partial_text."""
        dropdown = self.find_element(self.BORDER_DROPDOWN)
        from selenium.webdriver.support.ui import Select
        select = Select(dropdown)
        for option in select.options:
            if partial_text in option.text:
                select.select_by_visible_text(option.text)
                return
        raise Exception(f"Опция с текстом '{partial_text}' не найдена!")