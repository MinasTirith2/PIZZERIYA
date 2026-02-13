import logging
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
        def __init__(self, driver):
            self.driver = driver
            self.wait = WebDriverWait(driver, 15)  # Увеличим чуть-чуть для стабильности

        def find(self, locator):
            """Базовый поиск одного элемента с ожиданием."""
            return self.wait.until(EC.presence_of_element_located(locator))

        def find_element(self, locator):  # Для совместимости с твоим текущим кодом
            return self.find(locator)

        def find_elements(self, locator):
            return self.driver.find_elements(*locator)

        def scroll_to_element(self, element):
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

        def click(self, element_or_locator):
            """Умный клик: принимает и локатор, и уже найденный элемент."""
            if isinstance(element_or_locator, tuple):
                target = self.wait.until(EC.element_to_be_clickable(element_or_locator))
            else:
                target = element_or_locator

            try:
                target.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", target)

        def type(self, locator, text):
            element = self.find(locator)
            element.clear()
            element.send_keys(text)

        def open(self, url):
            self.driver.get(url)

        def delete_cookies(self):
            self.driver.delete_all_cookies()
            self.driver.refresh()

        def mock_server_failure(self, url_pattern):
            # Включаем перехват
            self.driver.execute_cdp_cmd("Fetch.enable", {
                "patterns": [{"urlPattern": url_pattern, "requestStage": "Request"}]
            })
