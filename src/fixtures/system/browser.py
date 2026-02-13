import logging
import logging.config
import time

import pytest
from allure_commons._allure import step
from selenium.webdriver import Remote
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def get_browser_options(bn, bv):
    if bn == "chrome":
        options = ChromeOptions()
    elif bn == "firefox":
        options = FirefoxOptions()
    else:
        options = ChromeOptions()
    if bv and bv != "None":
        options.set_capability("browserVersion", bv)
    selenoid_caps = {
        "enableVNC": True,
        "enableVideo": False  # Можно включить, если нужен файл записи
    }
    options.set_capability("selenoid:options", selenoid_caps)
    options.page_load_strategy = 'eager'
    return options


@pytest.fixture(scope="class")
def selenium(pytestconfig):
    logging.config.fileConfig('logging.ini')
    bn = pytestconfig.getoption("--bn")
    if bn == "None" or bn is None:
        bn = pytestconfig.getini("browser_name")
    bv = pytestconfig.getoption("--browser_version")
    if bv == "None" or bv is None:
        bv = pytestconfig.getini("browser_version")
    options = get_browser_options(bn, bv)
    base_url = pytestconfig.getini("selenium_url")
    with step("Запуск браузера"):
        driver = Remote(
            command_executor=f"{base_url}/wd/hub",
            options=options
        )
        driver.maximize_window()
        logging.info(f'Браузер {bn} запустился')
    print(f"Браузер в сессии: {driver.capabilities['browserName']}")
    yield driver
    logging.info(f'Браузер {bn} закрылся')
    driver.quit()

@pytest.fixture(scope="class") # Добавляем scope="class"
def open_main_page(selenium):
    """Фикстура для перехода на главную страницу один раз для класса."""
    selenium.get("https://pizzeria.skillbox.cc/")
    selenium.delete_all_cookies()
    selenium.execute_script("window.localStorage.clear();")
    selenium.execute_script("window.sessionStorage.clear();")
    selenium.refresh()
    return selenium

@pytest.fixture(scope="class")
def user_data():
    """Фикстура для генерации уникальных данных пользователя на уровне класса."""
    timestamp = int(time.time())
    return {
        "login": f"R{timestamp}",
        "email": f"{timestamp}@t.co",
        "pass": "123456",
        "first_name": f"Имя{timestamp % 1000}",
        "last_name": f"Фамилия{timestamp % 1000}"
    }