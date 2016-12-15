from common.ui_utils import ui_utils
from selenium.webdriver.common.by import By

'''

Created on August 4, 2016

@author: pyadav

'''

class download_report():

    web_session = None
    ui_utils = None

    def __init__(self, web_session, view_name):
        self.web_session = web_session
        self.web_driver = web_session.web_driver
        self.ui_utils = ui_utils(self.web_session)

    def text_format(self):
        el = self.web_driver.find_element_by_xpath('.//*[@title="Download"]')
        assert self.ui_utils.wait_util_element_displayed(el, 15)
        el.click()
        el = self.web_driver.find_element_by_id("download_choice__download_text")
        assert self.ui_utils.wait_util_element_displayed(el, 10)
        el.click()
        return True

    def csv_format(self):
        el = self.web_driver.find_element_by_xpath('.//*[@title="Download"]')
        assert self.ui_utils.wait_util_element_displayed(el, 15)
        el.click()
        el = self.web_driver.find_element_by_id("download_choice__download_csv")
        assert self.ui_utils.wait_util_element_displayed(el, 10)
        el.click()
        return True

    def pdf_format(self):
        el = self.web_driver.find_element_by_id('download_view')
        assert self.ui_utils.wait_util_element_displayed(el, 15)
        el.click()
        return True