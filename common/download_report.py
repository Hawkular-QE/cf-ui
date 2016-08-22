from common.ui_utils import ui_utils
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
'''

Created on August 4, 2016

@author: pyadav

'''

class download_report():

    web_session = None

    def __init__(self, web_session, view_name):
        #def __init__(self, web_session, view_name): (keeping it for future edit)
        self.web_session = web_session
        self.web_driver = web_session.web_driver
        #self.web_session.web_driver.get("{}/{}/show_list".format(self.web_session.MIQ_URL, view_name))
        self.download = self.web_driver.find_element_by_id("download_choice")


    def text_format(self):
        assert ui_utils(self.web_session).waitForElementOnPage(By.XPATH, ".//*[@id='download_choice']", 15)
        self.download.click()
        text= self.web_driver.find_element_by_id("download_choice__download_text")
        text.click()
        return True

    def csv_format(self):
        assert ui_utils(self.web_session).waitForElementOnPage(By.XPATH, ".//*[@id='download_choice']", 15)
        self.download.click()
        csv= self.web_driver.find_element_by_id("download_choice__download_csv")
        csv.click()
        return True
