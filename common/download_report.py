from common.ui_utils import ui_utils
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from time import sleep
'''

Created on August 4, 2016

@author: pyadav

'''

class download_report():

    web_session = None

    def __init__(self, web_session, view_name):
        self.web_session = web_session
        self.web_driver = web_session.web_driver

    def text_format(self):
        assert ui_utils(self.web_session).waitForElementOnPage(By.XPATH, ".//*[@title='Download']", 15)
        self.web_driver.find_element_by_xpath('.//*[@title="Download"]').click()
        text= self.web_driver.find_element_by_id("download_choice__download_text")
        text.click()
        sleep(5)
        return True

    def csv_format(self):
        assert ui_utils(self.web_session).waitForElementOnPage(By.XPATH, ".//*[@title='Download']", 15)
        self.web_driver.find_element_by_xpath('.//*[@title="Download"]').click()
        csv= self.web_driver.find_element_by_id("download_choice__download_csv")
        csv.click()
        sleep(5)
        return True

    def pdf_format(self):
        self.web_driver.find_element_by_id('download_view').click()
        sleep(5)
        return True