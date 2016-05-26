from selenium.webdriver.common.keys import Keys
from common.ui_utils import ui_utils

LOGIN_TEXT = "Compute"

class miq_login(object):
    web_driver = None

    def __init__(self, web_driver):
        self.web_driver = web_driver

    def login(self, username, password):
        self.username = username
        self.password = password

        elem = self.web_driver.find_element_by_id("user_name")
        elem.send_keys(self.username)
        elem = self.web_driver.find_element_by_id("user_password")
        elem.send_keys(self.password)
        elem.send_keys(Keys.RETURN)
        assert ui_utils(self.web_driver).waitForTextOnPage(LOGIN_TEXT, 15)
