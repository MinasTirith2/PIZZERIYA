import logging
import allure
import pytest
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By


@allure.feature("Главная страница")
@allure.story("Работа форм выбора и добавления пиццы")
@pytest.mark.regress
class TestFormsPizzas:
    @pytest.fixture(autouse=True)
    def setup(self, open_main_page):
        self.driver = open_main_page

    @allure.title("Кейс 1: Работа слайдера на главной странице сайта")
    def test_slider_work(self):
        with allure.step("Сбор названий пицц до прокрутки"):
            time.sleep(2)
            initial_elements = self.driver.find_elements(By.CSS_SELECTOR, "#product1 .slick-track .slick-active h3")
            initial_pizzas = [el.text for el in initial_elements]
            logging.info(f"Пиццы до прокрутки: {initial_pizzas}")
        with allure.step("Прокрутка слайдера вправо на 4 позиции"):
            next_button = self.driver.find_element(By.CSS_SELECTOR, ".slick-next")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_button)
            for i in range(4):
                self.driver.execute_script("arguments[0].click();", next_button)
                time.sleep(0.5)
                logging.debug(f"Клик {i + 1} по стрелке 'Вправо'")
        with allure.step("Сбор названий пицц после прокрутки"):
            new_elements = self.driver.find_elements(By.CSS_SELECTOR, "#product1 .slick-track .slick-active h3")
            new_pizzas = [el.text for el in new_elements]
            logging.info(f"Пиццы после прокрутки: {new_pizzas}")
        with allure.step("Сравнение списков"):
            assert initial_pizzas != new_pizzas, "Слайдер не прокрутился: список пицц остался прежним"

    @allure.title("Кейс 2: Появление кнопки 'В корзину' при наведении")
    def test_buy_button_hover(self):
        with allure.step("Наведение на карточку пиццы"):
            active_card = self.driver.find_element(By.CSS_SELECTOR, "#product1 li.slick-active")
            pizza_image = active_card.find_element(By.CSS_SELECTOR, "img.wp-post-image")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", pizza_image)
            action = ActionChains(self.driver)
            action.move_to_element(pizza_image).perform()
            time.sleep(1)
        with allure.step("Проверка отображения кнопки"):
            buy_btn = active_card.find_element(By.CSS_SELECTOR, ".add_to_cart_button")
            assert buy_btn.is_displayed(), "Кнопка 'В корзину' не появилась после наведения на картинку!"
            logging.info("Кнопка 'В корзину' успешно отобразилась.")

    @allure.title("Кейс 3: Добавление пиццы в корзину")
    def test_add_to_cart(self):
        with allure.step("Наведение на карточку пиццы"):
            active_card = self.driver.find_element(By.CSS_SELECTOR, "#product1 li.slick-active")
            pizza_image = active_card.find_element(By.CSS_SELECTOR, "img.wp-post-image")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", pizza_image)
            action = ActionChains(self.driver)
            action.move_to_element(pizza_image).perform()
            time.sleep(1)
        with (allure.step("Нажимаем кнопку В КОРЗИНУ")):
            buy_btn = active_card.find_element(By.CSS_SELECTOR, ".add_to_cart_button")
            buy_btn.click()
            time.sleep(1)
        with allure.step("Проверка смены кнопки на 'Подробнее'"):
            details_link = active_card.find_element(By.CSS_SELECTOR, ".added_to_cart")
            assert details_link.text == "ПОДРОБНЕЕ", f"Ожидали 'Подробнее', а получили '{details_link.text}'"
            logging.info("Кнопка успешно сменилась на 'Подробнее'. Товар в корзине.")
            time.sleep(4)

    @allure.title("Кейс 4: Переход по кнопке 'Подробнее'")
    def test_go_to_cart_via_details(self):
        time.sleep(4)
        with allure.step("Клик по 'Подробнее'"):
            details_link = self.driver.find_element(By.CSS_SELECTOR, ".added_to_cart")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", details_link)
            details_link.click()
        with allure.step("Проверка перехода в корзину"):
            time.sleep(3)
            assert "/cart/" in self.driver.current_url
            logging.info(f"Успешный переход. Текущий URL: {self.driver.current_url}")
