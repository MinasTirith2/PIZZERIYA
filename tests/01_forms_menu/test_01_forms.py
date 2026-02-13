import logging
import allure
import pytest
import time
from selenium.webdriver.support import expected_conditions as EC
from src.pages.main_page import MainPage

@allure.feature("Главная страница")
@allure.story("Работа форм выбора и добавления пиццы")
@pytest.mark.regress
class TestFormsPizzas:
    @pytest.fixture(autouse=True)
    def setup(self, open_main_page):
        self.main_page = MainPage(open_main_page)
        logging.info("Инициализация MainPage и переход на сайт")

    @allure.title("Кейс 1: Работа слайдера на главной странице сайта")
    def test_slider_work(self):
        with allure.step("Сбор названий пицц до прокрутки"):
            initial_pizzas = self.main_page.get_active_pizza_names()
            logging.info(f"Пиццы до прокрутки: {initial_pizzas}")
        with allure.step("Прокрутка слайдера вправо"):
            time.sleep(1)
            self.main_page.scroll_slider_right(4)
            logging.info("Выполнена прокрутка на 4 шага")
        with allure.step("Сбор названий пицц после прокрутки"):
            new_pizzas = self.main_page.get_active_pizza_names()
            logging.info(f"Пиццы после прокрутки: {new_pizzas}")
        assert initial_pizzas != new_pizzas
        logging.info("Тест слайдера завершен успешно")

    @allure.title("Кейс 2: Появление кнопки 'В корзину' при наведении")
    def test_buy_button_hover(self):
        logging.info("Старт теста: Проверка появления кнопки 'В корзину'")
        with allure.step("Наведение на карточку пиццы"):
            self.main_page.hover_first_active_pizza()
            time.sleep(1)
        with allure.step("Проверка отображения кнопки"):
            buy_btn = self.main_page.get_buy_button()
            assert buy_btn.is_displayed(), "Кнопка 'В корзину' не появилась!"
            logging.info("Кнопка 'В корзину' успешно отображена")

    @allure.title("Кейс 3: Добавление пиццы в корзину")
    def test_add_to_cart(self):
        logging.info("--- Старт Кейса 3: Добавление в корзину ---")

        with allure.step("Наведение на карточку пиццы"):
            self.main_page.hover_first_active_pizza()
            logging.info("Навели курсор на карточку для появления кнопки покупки")
        with allure.step("Нажимаем кнопку 'В КОРЗИНУ'"):
            self.main_page.add_pizza_to_cart()
            logging.info("Нажата кнопка добавления товара")
        with allure.step("Проверка смены кнопки на 'ПОДРОБНЕЕ'"):
            time.sleep(1)
            text = self.main_page.get_details_link_text()
            logging.info(f"Текст новой кнопки: {text}")
            assert text == "ПОДРОБНЕЕ", f"Ожидали 'ПОДРОБНЕЕ', но получили '{text}'"
        logging.info("Кейс 3 завершен успешно: товар в корзине")

    @allure.title("Кейс 4: Переход по кнопке 'Подробнее'")
    def test_go_to_cart_via_details(self):
        logging.info("--- Старт Кейса 4: Переход в корзину через карточку ---")

        with allure.step("Подготовка: добавление товара в корзину"):
            self.main_page.hover_first_active_pizza()
            self.main_page.add_pizza_to_cart()
            logging.info("Товар добавлен для проверки перехода")
        with allure.step("Клик по ссылке 'ПОДРОБНЕЕ'"):
            self.main_page.click_details_link()
            self.main_page.wait.until(EC.url_contains("/cart/"))
            logging.info("Выполнен клик по ссылке перехода в корзину")
        with allure.step("Проверка URL страницы корзины"):
            time.sleep(2)
            current_url = self.main_page.driver.current_url
            logging.info(f"Текущий URL после перехода: {current_url}")
            assert "/cart/" in current_url, f"Не удалось перейти в корзину. Мы на: {current_url}"
        logging.info("Кейс 4 завершен успешно: переход в корзину подтвержден")
