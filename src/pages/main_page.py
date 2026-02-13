from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage
import time
from selenium.webdriver.support import expected_conditions as EC


class MainPage(BasePage):

    # мои локаторы
    PIZZA_NAMES = (By.CSS_SELECTOR, "#product1 .slick-track .slick-active h3")
    NEXT_BUTTON = (By.CSS_SELECTOR, ".slick-next")
    SLIDER_BLOCK = (By.CSS_SELECTOR, "#product1")
    ACTIVE_CARD = (By.CSS_SELECTOR, "#product1 li.slick-active")
    PIZZA_IMG = (By.CSS_SELECTOR, "img.wp-post-image")
    BUY_BTN = (By.CSS_SELECTOR, ".add_to_cart_button")
    DETAILS_LNK = (By.XPATH, "//a[contains(@class, 'added_to_cart') and contains(text(), 'Подробнее')]")
    def get_active_pizza_names(self):
        self.wait.until(EC.visibility_of_any_elements_located(self.PIZZA_NAMES))
        elements = self.find_elements(self.PIZZA_NAMES)
        names = [el.text.strip() for el in elements if el.text.strip()]
        return names
    def scroll_slider_right(self, steps=4):
        slider = self.find_element(self.SLIDER_BLOCK)
        from selenium.webdriver import ActionChains
        ActionChains(self.driver).move_to_element(slider).perform()
        btn = self.find_element(self.NEXT_BUTTON)
        self.scroll_to_element(btn)
        for _ in range(steps):
            self.click(btn)
            time.sleep(0.5)
    def hover_first_active_pizza(self):
        card = self.find_element(self.ACTIVE_CARD)
        img = card.find_element(*self.PIZZA_IMG)
        self.scroll_to_element(img)
        ActionChains(self.driver).move_to_element(img).perform()
        return card

    def get_buy_button(self):
        """Возвращает кнопку 'В корзину' на активной карточке."""
        card = self.find_element(self.ACTIVE_CARD)
        return card.find_element(*self.BUY_BTN)

    def add_pizza_to_cart(self):
        """Надежное добавление в корзину с проверкой результата."""
        btn_locator = (By.CSS_SELECTOR, "li.slick-active .add_to_cart_button")
        btn = self.find_element(btn_locator)
        self.driver.execute_script("arguments[0].click();", btn)
        self.wait.until(EC.presence_of_element_located(self.DETAILS_LNK))

    def get_details_link_text(self):
        element = self.wait.until(EC.presence_of_element_located(self.DETAILS_LNK))
        return element.text

    def click_details_link(self):
        """Переход по ссылке 'Подробнее'."""
        link = self.wait.until(EC.element_to_be_clickable(self.DETAILS_LNK))
        self.scroll_to_element(link)
        self.driver.execute_script("arguments[0].click();", link)

    def click_first_pizza_image(self):
        """Клик по изображению первой активной пиццы через JS."""
        card = self.wait.until(EC.visibility_of_element_located(self.ACTIVE_CARD))
        img = card.find_element(*self.PIZZA_IMG)
        self.scroll_to_element(img)
        self.driver.execute_script("arguments[0].click();", img)

        from src.pages.product_page import ProductPage
        return ProductPage(self.driver)

