from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage

class BonusPage(BasePage):
    NAME_FIELD = (By.NAME, "username")
    PHONE_FIELD = (By.NAME, "billing_phone")
    SUBMIT_BTN = (By.NAME, "bonus")
    RESULT_TEXT = (By.ID, "bonus_content")

    def fill_bonus_form(self, name, phone):
        self.type(self.NAME_FIELD, name)
        self.type(self.PHONE_FIELD, phone)
        self.click(self.SUBMIT_BTN)

    def get_result_message(self):
        return self.find(self.RESULT_TEXT).text