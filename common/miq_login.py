from selenium.webdriver.common.keys import Keys
from common.ui_utils import ui_utils

LOGIN_TEXT = "Compute"

class miq_login(object):
    web_session = None
    web_driver = None

    def __init__(self, web_session):
        self.web_session = web_session
        self.web_driver = web_session.web_driver

    def login(self, username, password):
        self.username = username
        self.password = password

        elem = self.web_driver.find_element_by_id("user_name")
        elem.send_keys(self.username)
        elem = self.web_driver.find_element_by_id("user_password")
        elem.send_keys(self.password)
        elem.send_keys(Keys.RETURN)
        assert ui_utils(self.web_session).waitForTextOnPage(LOGIN_TEXT, 15)

    def logout(self):
        self.web_driver.find_element_by_id("username_display").click()
        ui_utils(self.web_session).waitForTextOnPage("Logout", 15)
        self.web_driver.find_element_by_css_selector("a[href*='/dashboard/logout']").click()
        ui_utils(self.web_session).waitForTextOnPage("Username", 15)
