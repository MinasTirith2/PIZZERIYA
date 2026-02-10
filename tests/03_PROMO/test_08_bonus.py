import logging
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import allure
import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


@allure.feature("Бонусная программа")
@allure.story("Заполнение и проверка полей бонусной программы")
@pytest.mark.regress
class TestPromoCod:
    @pytest.fixture(autouse=True)
    def setup(self, open_main_page):
        self.driver = open_main_page

    @allure.title("Кейс 20: Бонусная программа")
    def test_bonus(self):
        with (allure.step("Переходим на страницу бонусной программы")):
            self.driver.get("https://pizzeria.skillbox.cc/bonus/")
            time.sleep(1)
        with (allure.step("Заполняем поля валидными данными")):
            self.driver.find_element(By.NAME, "username").send_keys("Dmitryi")
            self.driver.find_element(By.NAME, "billing_phone").send_keys("77758867986")
            self.driver.find_element(By.NAME, "bonus").click()
            try:
                WebDriverWait(self.driver, 5).until(EC.alert_is_present())
                alert = self.driver.switch_to.alert
                logging.info(f"Вижу алерт: {alert.text}")
                alert.accept()
            except TimeoutException:
                logging.warning("Алерт не появился, идем дальше")
        with allure.step("Проверка валидации"):
            errors = self.driver.find_elements(By.ID, "bonus_content")
            if len(errors) > 0 and "Введен неверный формат телефона" in errors[0].text:
                error_msg = errors[0].text
                logging.error(f"Тест упал на валидации: {error_msg}")
                pytest.fail(f"Валидация не пройдена: {error_msg}")
            else:
                logging.info("Ошибок валидации не обнаружено, продолжаем...")
