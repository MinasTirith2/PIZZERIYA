pytest_plugins = ["src.fixtures.system.browser"]


def pytest_addoption(parser):
    def register_params(parser):
        """Регистрация параметров командной строки и ini-файла."""
        parser.addini("selenium_url", help="URL хаба Selenium")
        parser.addini("browser_name", help="Браузер по умолчанию")
        parser.addini("browser_version", help="Версия по умолчанию")
        parser.addoption("--bn", action="store", default="None")
        parser.addoption("--browser_version", action="store", default="None")
    register_params(parser)