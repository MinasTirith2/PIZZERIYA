import logging
from selenium.webdriver.support.ui import Select
import allure
import pytest
import time
from selenium.webdriver.common.by import By


@allure.feature("Описание пиццы")
@allure.story("Описание товара, опции пиццы и удаление")
@pytest.mark.regress
class TestPizzaOptions:
    @pytest.fixture(autouse=True)
    def setup(self, open_main_page):
        self.driver = open_main_page

    @allure.title("Кейс 5: Переход в описание определённого товара")
    def test_go_to_pizza_details(self):
        with allure.step("Выбор пиццы и запоминание названия"):
            active_card = self.driver.find_element(By.CSS_SELECTOR, "#product1 li.slick-active")
            expected_name = active_card.find_element(By.CSS_SELECTOR, "h3").text.upper()
            logging.info(f"Выбрана пицца: {expected_name}")
        with allure.step("Клик по картинке пиццы"):
            pizza_image = active_card.find_element(By.CSS_SELECTOR, "img.wp-post-image")
            pizza_image.click()
            TestPizzaOptions.expected_url = self.driver.current_url
            time.sleep(1)
        with allure.step("Проверка соответствия открытого товара"):
            actual_name = self.driver.find_element(By.CSS_SELECTOR, "h1.product_title").text.upper()
            assert expected_name in actual_name, f"Открылась не та пицца! Ожидали {expected_name}, а видим {actual_name}"
            logging.info(f"Успешный переход в карточку: {actual_name}")

    @allure.title("Кейс 6: Обновление цены товара при выборе опции СЫРНЫЙ БОРТ")
    def test_cheese_border_price(self):
        time.sleep(2)
        price_element = self.driver.find_element(By.CSS_SELECTOR, "p.price .amount")
        base_price = price_element.text.replace('₽', '').strip()
        logging.info(f"Базовая цена: {base_price}")
        with allure.step("Выбор опции 'Сырный борт'"):
            dropdown = self.driver.find_element(By.ID, "board_pack")
            select = Select(dropdown)
            select.select_by_visible_text("Сырный - 55.00 р.")
            time.sleep(2)
        with allure.step("Проверка изменения цены"):
            new_price_element = self.driver.find_element(By.CSS_SELECTOR, "p.price .amount")
            new_price = new_price_element.text.replace('₽', '').strip()
            logging.info(f"Цена с сырным бортом: {new_price}")
            assert base_price != new_price, "Цена не изменилась!"

    @allure.title("Кейс 7: обновление цены товара при выборе опции КОЛБАСНЫЙ БОРТ'")
    def test_sausage_border_price(self):
        time.sleep(2)
        with allure.step("Выбор опции 'Колбасный борт'"):
            dropdown = self.driver.find_element(By.ID, "board_pack")
            select = Select(dropdown)
            select.select_by_visible_text("Колбасный - 65.00 р.")
            time.sleep(2)
        with allure.step("Проверка изменения цены"):
            raw_final_price = self.driver.find_element(By.CSS_SELECTOR, "p.price .amount").text
            final_price = raw_final_price.replace('₽', '').strip()
            logging.info(f"Цена с колбасным бортом: {final_price}")
            assert final_price != "", "Цена не должна быть пустой"

    @allure.title("Кейс 8: Наличие выбранных тоавров в корзине")
    def test_product_in_cart(self):
        with allure.step("Нажимаем кнопку 'В корзину'"):
            add_button = self.driver.find_element(By.NAME, "add-to-cart")
            add_button.click()
            time.sleep(2)
        with allure.step("Переход в корзину"):
            self.driver.get("http://pizzeria.skillbox.cc/cart/")
            logging.info("Переход в корзину")
            time.sleep(1)
        with allure.step("Проверка наличия товара"):
            actual_url = self.driver.find_element(By.CSS_SELECTOR, "td.product-name a").get_attribute("href")
            expected = TestPizzaOptions.expected_url.replace("https://", "").replace("http://", "")
            actual = actual_url.replace("https://", "").replace("http://", "")
            assert expected == actual, f"URL не совпадают! Ждали {expected}, получили {actual}"
            logging.info("Наш товар в корзине")
            time.sleep(2)

    @allure.title("Кейс 9: Удаление позиции из корзины")
    def test_remove_from_cart(self):
        with allure.step("Нажатие на кнопку удаления (крестик)"):
            remove_button = self.driver.find_element(By.CSS_SELECTOR, "a.remove")
            remove_button.click()
            logging.info("Удаляем товар")
            time.sleep(1)
        with allure.step("Проверка, что корзина стала пустой"):
            empty_msg = self.driver.find_element(By.CSS_SELECTOR, "p.cart-empty").text
            logging.info(f"Статус после удаления: {empty_msg.replace('₽', 'руб')}")
            assert "пуста" in empty_msg.lower(), "Корзина не очистилась после нажатия на крестик!"
