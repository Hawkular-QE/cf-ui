from common.ui_utils import ui_utils
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from common.navigate import navigate

'''

Created on September 22, 2016

@author: pyadav

'''

class eap_alerts():

    web_session = None
    alert_desc = "Heap-Alert"
    editalert_desc = "Heap-Alert-edited"
    copyalert_desc = "Heap-Alert-copied"

    def __init__(self, web_session):

        self.web_session = web_session
        self.web_driver = web_session.web_driver


    def add_alert(self):

        navigate(self.web_session).get("{}/miq_policy/explorer".format(self.web_session.MIQ_URL))
        assert ui_utils(self.web_session).waitForTextOnPage("All Policy Profiles", 15)
        #self.web_session.web_driver.find_element_by_xpath("//a[contains(.,'Alerts')]").click()
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
        ui_utils(self.web_session).sleep(10)
        assert ui_utils(self.web_session).waitForTextOnPage("Nothing", 90)
        self.web_session.web_driver.find_element_by_xpath("//button[@data-original-title='Nothing']").click()
        self.web_session.web_driver.find_element_by_xpath("//span[contains(.,'JVM Heap Used')]").click()
        assert ui_utils(self.web_session).waitForTextOnPage("> Heap Max (%)", 90)

        self.web_session.web_driver.find_element_by_xpath("//button[@data-id='miq_alert_severity']").click()
        assert ui_utils(self.web_session).waitForTextOnPage("Info", 90)
        self.web_session.web_driver.find_element_by_xpath("//a[contains(.,'Info')]").click()

        self.web_session.web_driver.find_element_by_xpath(".//*[@id='value_mw_greater_than']").send_keys('4')
        self.web_session.web_driver.find_element_by_xpath(".//*[@id='value_mw_less_than']").send_keys('2')
        ui_utils(self.web_session).sleep(10)
        self.web_session.web_driver.find_element_by_xpath("//input[@id='send_evm_event_cb']").click()
        ui_utils(self.web_session).sleep(10)
        self.web_session.web_driver.find_element_by_xpath("//input[@id='description']").send_keys(self.alert_desc)

        self.web_session.web_driver.find_element_by_xpath("//button[contains(.,'Add')]").click()

        assert ui_utils(self.web_session).waitForTextOnPage('Alert "{}" was added'.format(self.alert_desc),90)

        return True

    def copy_alert(self):
        self.navigate_to_all_alerts()
        ui_utils(self.web_session).get_list_table_as_elements()
        ui_utils(self.web_session).click_on_row_containing_text(self.alert_desc)

        assert ui_utils(self.web_session).waitForTextOnPage('Alert "{}"'.format(self.alert_desc), 90)
        self.web_session.web_driver.find_element_by_xpath("//button[@title='Configuration']").click()
        assert ui_utils(self.web_session).waitForTextOnPage("Copy", 90)
        self.web_session.web_driver.find_element_by_xpath("//a[@id='miq_alert_vmdb_choice__alert_copy']").click()
        ui_utils(self.web_session).accept_alert(20)
        assert ui_utils(self.web_session).waitForTextOnPage("Adding a new Alert", 90)
        self.web_session.web_driver.find_element_by_xpath("//input[@id='description']").clear()
        self.web_session.web_driver.find_element_by_xpath("//input[@id='description']").send_keys(self.copyalert_desc)
        ui_utils(self.web_session).sleep(10)
        self.web_driver.find_element_by_xpath(".//*[@id='buttons_on']/button[1]").click()
        assert ui_utils(self.web_session).waitForTextOnPage('Alert "{}" was added'.format(self.copyalert_desc), 20)
        return True

    def edit_alert(self):

        self.navigate_to_all_alerts()
        ui_utils(self.web_session).get_list_table_as_elements()
        ui_utils(self.web_session).click_on_row_containing_text(self.alert_desc)
        assert ui_utils(self.web_session).waitForTextOnPage('Alert "{}"'.format(self.alert_desc), 90)
        self.web_session.web_driver.find_element_by_xpath("//button[@title='Configuration']").click()
        assert ui_utils(self.web_session).waitForTextOnPage("Copy", 90)

        self.web_session.web_driver.find_element_by_xpath("//a[@id='miq_alert_vmdb_choice__alert_edit']").click()
        assert ui_utils(self.web_session).waitForTextOnPage("Description", 90)
        self.web_session.web_driver.find_element_by_xpath("//input[@id='description']").clear()
        self.web_session.web_driver.find_element_by_xpath("//input[@id='description']").send_keys(self.editalert_desc)
        self.web_session.web_driver.find_element_by_xpath(".//*[@id='value_mw_greater_than']").clear()
        self.web_session.web_driver.find_element_by_xpath(".//*[@id='value_mw_greater_than']").send_keys('5')
        self.web_session.web_driver.find_element_by_xpath(".//*[@id='value_mw_less_than']").clear()
        self.web_session.web_driver.find_element_by_xpath(".//*[@id='value_mw_less_than']").send_keys('4')
        ui_utils(self.web_session).sleep(10)
        self.web_session.web_driver.find_element_by_xpath("//button[contains(.,'Save')]").click()
        assert ui_utils(self.web_session).waitForTextOnPage('Alert "{}" was saved'.format(self.editalert_desc), 50)

        return True

    def delete_alert(self, alertdesc):

        self.navigate_to_all_alerts()
        ui_utils(self.web_session).get_list_table_as_elements()

        if ui_utils(self.web_session).get_elements_containing_text(alertdesc):
            ui_utils(self.web_session).click_on_row_containing_text(alertdesc)
            assert ui_utils(self.web_session).waitForTextOnPage('Alert "{}"'.format(alertdesc), 90)
            self.web_session.web_driver.find_element_by_xpath("//button[@title='Configuration']").click()
            assert ui_utils(self.web_session).waitForTextOnPage("Copy", 90)
            self.web_session.web_driver.find_element_by_xpath("//a[@id='miq_alert_vmdb_choice__alert_delete']").click()
            ui_utils(self.web_session).accept_alert(20)
            assert ui_utils(self.web_session).waitForTextOnPage('Alert "{}": Delete successful'.format(alertdesc), 50)
            self.web_session.logger.info("The alert {} is removed successfully.".format(alertdesc))

            return True

    def navigate_to_all_alerts(self):
        navigate(self.web_session).get("{}/miq_policy/explorer".format(self.web_session.MIQ_URL))
        assert ui_utils(self.web_session).waitForTextOnPage("All Alerts", 15)
        self.web_session.web_driver.find_element_by_xpath("//li[@title='All Alerts']").click()
        ui_utils(self.web_session).sleep(20)

    def click_alerts(self):
        self.web_session.web_driver.find_element_by_xpath('//*[@id="accordion"]/div[7]/div[1]/h4/a').click()
        ui_utils(self.web_session).sleep(1)