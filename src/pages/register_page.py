from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage

class RegisterPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    USERNAME_FIELD = (By.ID, "reg_username")
    EMAIL_FIELD = (By.ID, "reg_email")
    PASSWORD_FIELD = (By.ID, "reg_password")
    REGISTER_BUTTON = (By.NAME, "register")

    def register_new_user(self, login, email, password):
        self.open("http://pizzeria.skillbox.cc/register/")
        self.type(self.USERNAME_FIELD, login)
        self.type(self.EMAIL_FIELD, email)
        self.type(self.PASSWORD_FIELD, password)
        self.click(self.REGISTER_BUTTON)