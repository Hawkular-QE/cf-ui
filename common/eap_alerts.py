from common.ui_utils import ui_utils
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
'''

Created on September 22, 2016

@author: pyadav

'''

class eap_alerts():

    web_session = None

    def __init__(self, web_session):

        self.web_session = web_session
        self.web_driver = web_session.web_driver


    def add_alert(self):

        self.web_session.web_driver.get("{}/miq_policy/explorer".format(self.web_session.MIQ_URL))

        alert= self.web_driver.find_element_by_xpath(".//*[@id='accordion']/div[7]/div[1]/h4")

        configurtion = self.web_driver.find_element_by_xpath('.//*[@title="Configuration"]')

        add_alert = self.web_driver.find_element_by_xpath(".//*[@id='miq_alert_vmdb_choice__alert_new']")

        alert_description = self.web_driver.find_element_by_xpath(".//*[@id='description']")
        select_based_on = self.web_driver.find_element_by_xpath(
            ".//*[@id='alert_info_div']/div[2]/div[3]/div/div/button")
        select_middleware = self.web_driver.find_element_by_xpath(
            ".//*[@id='alert_info_div']/div[2]/div[3]/div/div/div/ul/li[4]/a/span[1]")
        select_evaluate_button = self.web_driver.find_element_by_xpath(
            ".//*[@id='alert_info_div']/div[2]/div[4]/div/div/button")
        select_evaluate_item = self.web_driver.find_element_by_xpath(
            ".//*[@id='alert_info_div']/div[2]/div[4]/div/div/div/ul/li[3]/a")
        enter_greter_max_heap = self.web_driver.find_element_by_xpath(".//*[@id='value_mw_greater_than']")
        enter_less_max_heap = self.web_driver.find_element_by_xpath(".//*[@id='value_mw_less_than']")
        select_timeline_event = self.web_driver.find_element_by_xpath(".//*[@id='send_evm_event_cb']")
        add_button = self.web_driver.find_element_by_xpath(".//*[@id='buttons_on']/button[1]")

        alert().click()
        configurtion().click()
        assert ui_utils(self.web_session).waitForElementOnPage(By.ID, "miq_alert_vmdb_choice__alert_new", 15)
        add_alert().click
        assert ui_utils(self.web_session).waitForElementOnPage(By.ID,"description",15)
        alert_description().send_keys('Heap Alert')
        select_based_on().ckick()
        select_middleware().click()
        select_evaluate_button().click()
        select_evaluate_item().click()
        enter_greter_max_heap().send_keys('40')
        enter_less_max_heap().send_keys('10')
        select_timeline_event().click()
        add_button.click()

    def delete_alert(self):

        self.web_session.web_driver.get("{}/miq_policy/explorer".format(self.web_session.MIQ_URL))

assert ui_utils(self.web_session).waitForTextOnPage("Alerts", 15).click()
        assert ui_utils(self.web_session).waitForTextOnPage("All Alerts", 15).click()
        assert ui_utils(self.web_session).waitForTextOnPage("Heap Alert", 15).click()
        configurtion = self.web_driver.find_element_by_xpath('.//*[@title="Configuration"]').click()

        delete = self.web_driver.find_element_by_xpath(".//*[@id='miq_alert_vmdb_choice__alert_delete']").click()


    def edit_alert(self):
        self.web_session.web_driver.get("{}/miq_policy/explorer".format(self.web_session.MIQ_URL))

        assert ui_utils(self.web_session).waitForTextOnPage("Alerts", 15).click()
        assert ui_utils(self.web_session).waitForTextOnPage("All Alerts", 15).click()
        assert ui_utils(self.web_session).waitForTextOnPage("alert-test", 15).click()
        configurtion = self.web_driver.find_element_by_xpath('.//*[@title="Configuration"]').click()
        edit= self.web_driver.find_element_by_xpath(".//*[@id='miq_alert_vmdb_choice__alert_edit']").click()
        alert_description = self.web_driver.find_element_by_xpath(".//*[@id='description']")
        alert_description().send_keys('Heap-Alert')
        save= self.web_driver.find_element_by_xpath(".//*[@id='buttons_on']/button[1]").click()