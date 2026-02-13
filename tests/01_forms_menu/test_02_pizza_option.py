import logging
import allure
import pytest
import time
from selenium.webdriver.common.by import By
from src.pages.main_page import MainPage
from selenium.webdriver.support import expected_conditions as EC


@allure.feature("Описание пиццы")
@allure.story("Описание товара, опции пиццы и удаление")
@pytest.mark.regress
class TestPizzaOptions:
    @pytest.fixture(autouse=True)
    def setup(self, open_main_page):
        self.driver = open_main_page
        self.main_page = MainPage(self.driver)
        self.driver.get("https://pizzeria.skillbox.cc/")

    @allure.title("Кейс 5: Переход в описание определённого товара")
    def test_go_to_pizza_details(self):
        with allure.step("Выбор пиццы и запоминание названия"):
            names = self.main_page.get_active_pizza_names()
            expected_name = names[0].upper()
            logging.info(f"Выбрана пицца: {expected_name}")

        with allure.step("Клик по картинке пиццы"):
            product_page = self.main_page.click_first_pizza_image()
            TestPizzaOptions.expected_url = self.main_page.driver.current_url
            logging.info(f"Перешли по адресу: {TestPizzaOptions.expected_url}")

        with allure.step("Проверка соответствия открытого товара"):
            actual_name = product_page.get_product_name()
            assert expected_name in actual_name, f"Открылась не та пицца! Ожидали {expected_name}, а видим {actual_name}"
            logging.info(f"Успешный переход в карточку: {actual_name}")

    @allure.title("Кейс 6: Обновление цены товара при выборе опции СЫРНЫЙ БОРТ")
    def test_cheese_border_price(self):
        product_page = self.main_page.click_first_pizza_image()
        base_price = product_page.get_price()
        logging.info(f"Базовая цена: {base_price}")

        with allure.step("Выбор опции 'Сырный борт'"):
            product_page.select_border("Сырный - 55.00 р.")
        with allure.step("Проверка изменения цены"):
            self.main_page.wait.until(lambda d: product_page.get_price() != base_price)
            new_price = product_page.get_price()
            logging.info(f"Цена с сырным бортом: {new_price}")
            assert new_price == base_price + 55.00

    @allure.title("Кейс 7: обновление цены товара при выборе опции КОЛБАСНЫЙ БОРТ")
    def test_sausage_border_price(self):
        product_page = self.main_page.click_first_pizza_image()
        base_price = product_page.get_price()

        with allure.step("Выбор опции 'Колбасный борт'"):
            product_page.select_border("Колбасный - 65.00 р.")

        with allure.step("Проверка изменения цены"):
            self.main_page.wait.until(lambda d: product_page.get_price() != base_price)
            assert product_page.get_price() == base_price + 65.00

    @allure.title("Кейс 8: Наличие выбранных товаров в корзине")
    def test_product_in_cart(self):
        product_page = self.main_page.click_first_pizza_image()
        expected_url = self.driver.current_url

        with allure.step("Нажимаем кнопку 'В корзину'"):
            add_button = self.driver.find_element(By.NAME, "add-to-cart")
            add_button.click()
            time.sleep(2)

        with allure.step("Переход в корзину"):
            self.driver.get("https://pizzeria.skillbox.cc/cart/")
            logging.info("Переход в корзину")
            time.sleep(1)

        with allure.step("Проверка наличия товара"):
            product_link = self.driver.find_element(By.CSS_SELECTOR, "td.product-name a")
            actual_url = product_link.get_attribute("href")
            def clean_url(url):
                return url.replace("https://", "").replace("http://", "").rstrip('/')
            assert clean_url(expected_url) == clean_url(actual_url), \
                f"В корзине не тот товар! Ждали {expected_url}, получили {actual_url}"
            logging.info("Наш товар успешно найден в корзине")

    @allure.title("Кейс 9: Удаление позиции из корзины")
    def test_remove_from_cart(self):
        product_page = self.main_page.click_first_pizza_image()

        with allure.step("Подготовка: Добавление товара в корзину"):
            add_button = self.driver.find_element(By.NAME, "add-to-cart")
            add_button.click()
            time.sleep(2)
            self.driver.get("https://pizzeria.skillbox.cc/cart/")

        with allure.step("Нажатие на кнопку удаления (крестик)"):
            remove_button = self.main_page.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.remove"))
            )
            remove_button.click()
            logging.info("Нажат крестик удаления товара")

        with allure.step("Проверка, что корзина стала пустой"):
            empty_cart_locator = (By.CSS_SELECTOR, "p.cart-empty")
            self.main_page.wait.until(EC.visibility_of_element_located(empty_cart_locator))

            empty_msg = self.driver.find_element(*empty_cart_locator).text
            logging.info(f"Статус после удаления: {empty_msg}")

            assert "пуста" in empty_msg.lower(), f"Ожидали сообщение о пустой корзине, получили: {empty_msg}"