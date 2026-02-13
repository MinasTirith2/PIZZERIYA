import logging
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import allure
import pytest
from selenium.webdriver.support.wait import WebDriverWait

from pages.bonus_page import BonusPage


@allure.feature("Бонусная программа")
@allure.story("Заполнение и проверка полей бонусной программы")
@pytest.mark.regress
class TestPromoCod:
    @pytest.fixture(autouse=True)
    def setup(self, open_main_page):
        self.driver = open_main_page

    @allure.title("Кейс 20: Бонусная программа — проверка формата телефона")
    def test_bonus_phone_validation(self):
        bonus_page = BonusPage(self.driver)

        with allure.step("Переход на страницу бонусов"):
            self.driver.get("https://pizzeria.skillbox.cc/bonus/")

        with allure.step("Заполнение данных"):
            bonus_page.fill_bonus_form("Dmitryi", "77758867986")

        with allure.step("Проверка результата"):
            try:
                WebDriverWait(self.driver, 5).until(EC.alert_is_present())
                alert = self.driver.switch_to.alert
                alert_text = alert.text
                alert.accept()
                logging.info(f"Алерт обработан: {alert_text}")

                assert "Заявка отправлена" in alert_text

            except TimeoutException:
                logging.info("Алерт не появился, проверяем текст на странице")
                message = bonus_page.get_result_message()
                assert "Введен неверный формат телефона" not in message