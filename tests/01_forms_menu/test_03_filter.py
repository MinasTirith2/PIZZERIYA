import logging
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


@allure.feature("Работа фильтра")
@allure.story("Переход в ДЕСЕРТЫ и работа фильтра")
@pytest.mark.regress
class TestFilterPizzas:
    @pytest.fixture(autouse=True)
    def setup(self, open_main_page):
        self.driver = open_main_page
        self.driver.get("https://pizzeria.skillbox.cc/")

    def test_go_to_desserts_logic(self):
            parent_menu = self.driver.find_element(By.CSS_SELECTOR, "#menu-item-389 > a")
            desert_item = self.driver.find_element(By.CSS_SELECTOR, "#menu-item-391 > a")
            actions = ActionChains(self.driver)
            actions.move_to_element(parent_menu).pause(0.5).click(desert_item).perform()
            WebDriverWait(self.driver, 10).until(EC.url_contains("deserts"))

    @allure.title("Кейс 10: Переход в десерты через выпадающее меню")
    def test_go_to_desserts(self):
        with allure.step("Наведение на 'Меню' и клик по 'Десерты'"):
            self.test_go_to_desserts_logic()

        with allure.step("Проверка перехода"):
            header = self.driver.find_element(By.CSS_SELECTOR, "h1.entry-title").text
            logging.info(f"Заголовок найден: {header}")
            assert "ДЕСЕРТЫ" in header.upper()

    @allure.title("Кейс 11: Работа фильтра по цене")
    def test_price_filter(self):
        self.test_go_to_desserts_logic()

        with allure.step("Снижаем цену до 140₽"):
            handles = self.driver.find_elements(By.CSS_SELECTOR, ".ui-slider-handle")
            right_handle = handles[1]
            actions = ActionChains(self.driver)

            for _ in range(60):
                current_val = int(
                    ''.join(filter(str.isdigit, self.driver.find_element(By.CSS_SELECTOR, ".price_label .to").text)))
                if current_val <= 140:
                    logging.info(f"Цель достигнута: {current_val}")
                    break
                right_handle.send_keys("\ue012")

        with allure.step("Нажатие кнопки 'Применить'"):
            self.driver.find_element(By.CSS_SELECTOR, "button.button[type='submit']").click()

        with allure.step("Валидация цен"):
            WebDriverWait(self.driver, 10).until(EC.url_contains("max_price=140"))

            prices = self.driver.find_elements(By.CSS_SELECTOR, ".price .amount")
            for p in prices:
                clean_price = ''.join(c for c in p.text if c.isdigit() or c in ',.')
                val = float(clean_price.replace(',', '.'))
                assert val <= 140, f"Ошибка! Товар стоит {val}, что больше 140"
