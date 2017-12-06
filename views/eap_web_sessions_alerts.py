from common.ui_utils import ui_utils
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from common.navigate import navigate

'''

Created on December 1st

@author: gbaufake

'''

class eap_web_session_alerts:
    web_session = None
    alerts_description = "Web Session Alert"

    def __init__(self, web_session):
        self.web_session = web_session
        self.web_driver = webdriver

    def add_alert(self):

        navigate(self.web_session).get("{}/miq_policy/explorer".format(self.web_session.MIQ_URL))
        assert ui_utils(self.web_session).waitForTextOnPage("All Policy Profiles", 15)
        self.click_alerts()
        assert ui_utils(self.web_session).waitForTextOnPage("All Alerts", 80)

        assert ui_utils(self.web_session).waitForTextOnPage("Description", 80)
        #ui_utils(self.web_session).sleep(10)
        self.web_session.web_driver.find_element_by_xpath("//button[@title='Configuration']").click()

        self.web_session.logger.info("Click done")

        self.web_session.web_driver.find_element_by_xpath("//a[@title='Add a New Alert']").click()
        assert ui_utils(self.web_session).waitForTextOnPage("Adding a new Alert", 90)


        self.web_session.web_driver.find_element_by_xpath("//button[@data-original-title='VM and Instance']").click()
        self.web_session.web_driver.find_element_by_xpath("//span[contains(.,'Middleware Server')]").click()

        self.web_session.web_driver.find_element_by_xpath("//button[@data-original-title='Nothing']").click()
        self.web_session.web_driver.find_element_by_xpath("//span[contains(.,'Web Sessions - Active')]").click()

        # Notification Frequency
        self.web_session.web_driver.find_element_by_xpath("//button[@data-original-title='10 Minutes']").click()
        self.web_session.web_driver.find_element_by_xpath("//span[contains(.,'1 Minute')]").click()

        ui_utils(self.web_session).sleep(10)



        # assert ui_utils(self.web_session).waitForTextOnPage("Nothing", 90)
        # self.web_session.web_driver.find_element_by_xpath("//button[@data-original-title='Nothing']").click()
        self.web_session.web_driver.find_element_by_xpath("//input[@id='description']").send_keys(self.alerts_description)

        #assert ui_utils(self.web_session).waitForTextOnPage("Web Sessions - Active", 0)

        # self.web_session.web_driver.find_element_by_xpath(".//*[@id='value_mw_greater_than']").send_keys('4')
        # self.web_session.web_driver.find_element_by_xpath(".//*[@id='value_mw_less_than']").send_keys('2')
        # self.web_session.web_driver.find_element_by_xpath(".//*[@id='send_evm_event_cb']").click()
        # ui_utils(self.web_session).sleep(20)

        # self.web_session.web_driver.find_element_by_xpath("//button[contains(.,'Add')]").click()
        # assert ui_utils(self.web_session).waitForTextOnPage('Alert "{}" was added'.format(self.alert_desc), 90)

        return True

    def click_alerts(self):
        self.web_session.web_driver.find_element_by_xpath('//*[@id="accordion"]/div[7]/div[1]/h4/a').click()
        ui_utils(self.web_session).sleep(1)