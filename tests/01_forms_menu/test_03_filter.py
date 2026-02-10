import logging
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import allure
import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


@allure.feature("Работа фильтра")
@allure.story("Переход в ДЕСЕРТЫ и работа фильтра")
@pytest.mark.regress
class TestFilterPizzas:
    @pytest.fixture(autouse=True)
    def setup(self, open_main_page):
        self.driver = open_main_page

    @allure.title("Кейс 10: Переход в десерты через выпадающее меню")
    def test_go_to_desserts(self):
        with allure.step("Наведение на 'Меню' и клик по 'Десерты'"):
            parent_menu = self.driver.find_element(By.CSS_SELECTOR, "#menu-item-389 > a")
            dessert_item = self.driver.find_element(By.CSS_SELECTOR, "#menu-item-391 > a")
            actions = ActionChains(self.driver)
            actions.move_to_element(parent_menu).pause(1).click(dessert_item).perform()
        with allure.step("Проверка перехода"):
            WebDriverWait(self.driver, 10).until(EC.url_contains("deserts"))
            header = self.driver.find_element(By.CSS_SELECTOR, "h1.entry-title").text
            logging.info(f"Заголовок найден: {header}")
            assert "ДЕСЕРТЫ" in header.upper()

    @allure.title("Кейс 11: Работа фильтра по цене")
    def test_price_filter(self):
        with allure.step("Запоминаем начальную макс. цену"):
            raw_text = self.driver.find_element(By.CSS_SELECTOR, ".price_label .to").text
            max_val = ''.join(filter(str.isdigit, raw_text))
            logging.info(f"Начальная макс. цена (только цифры): {max_val}")
        with allure.step("Снижаем цену до 140₽"):
            handle = self.driver.find_element(By.CSS_SELECTOR, "span.ui-slider-handle[style*='left: 100%']")
            actions = ActionChains(self.driver)
            for _ in range(60):
                current_to_text = self.driver.find_element(By.CSS_SELECTOR, ".price_label .to").text
                current_val = int(''.join(filter(str.isdigit, current_to_text)))
                if current_val <= 140:
                    logging.info(f"Цель достигнута: {current_val}")
                    break
                actions.click_and_hold(handle).move_by_offset(-50, 0).release().perform()
                time.sleep(0.5)
            else:
                pytest.fail(f"Не удалось снизить цену до 140. Остановились на: {current_to_text}")
        with allure.step("Нажатие кнопки 'Применить'"):
            apply_button = self.driver.find_element(By.CSS_SELECTOR, "button.button[type='submit']")
            apply_button.click()
        with allure.step("Валидация цен"):
            WebDriverWait(self.driver, 10).until(lambda d: "max_price=140" in d.current_url)
            prices = self.driver.find_elements(By.CSS_SELECTOR, ".price .amount")
            for p in prices:
                val = float(''.join(c for c in p.text if c.isdigit() or c in ',.').replace(',', '.'))
                logging.info(f"Проверка цены товара: {val}")
                assert val <= 140, f"Нашелся десерт дороже 140: {val}"
