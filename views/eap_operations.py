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

class eap_operations():

    web_session = None

    def __init__(self, web_session):

        self.web_session = web_session
        self.web_driver = web_session.web_driver

    def eap_power(self):
        self.web_session.web_driver.get("{}/middleware_domain/show_list".format(self.web_session.MIQ_URL))
        assert ui_utils(self.web_session).waitForTextOnPage("Middleware Domains", 15)
        self.web_session.web_driver.find_element_by_xpath("//td[contains(.,'master')]").click()
        assert ui_utils(self.web_session).waitForTextOnPage("master (Summary)", 15)
        self.web_session.web_driver.find_element_by_xpath("//td[contains(.,'Middleware Server Groups')]").click()
        assert ui_utils(self.web_session).waitForTextOnPage("Server Group Name", 15)
        self.web_session.web_driver.find_element_by_xpath("//td[contains(.,'main-server-group')]").click()
        assert ui_utils(self.web_session).waitForTextOnPage("main-server-group (Summary)", 15)
        self.web_session.web_driver.find_element_by_xpath("//td[contains(.,'Middleware Servers')]").click()
        assert ui_utils(self.web_session).waitForTextOnPage("Server Name", 15)
        self.web_session.web_driver.find_element_by_xpath("//td[contains(.,'server-one')]").click()
        assert ui_utils(self.web_session).waitForTextOnPage("Properties", 15)
        self.web_session.web_driver.find_element_by_xpath("//button[@title='Power']").click()



    def stop_eap(self):
        self.eap_power()
        self.web_session.web_driver.find_element_by_xpath("//a[@title='Stop this server']").click()
        ui_utils(self.web_session).accept_alert(20)
        assert ui_utils(self.web_session).waitForTextOnPage("Stop initiated for selected server(s)", 30)
        return True

    def restart_eap(self):
        self.eap_power()
        self.web_session.web_driver.find_element_by_xpath("//a[@title='Restart this server']").click()
        ui_utils(self.web_session).accept_alert(20)
        assert ui_utils(self.web_session).waitForTextOnPage("Restart initiated for selected server(s)", 15)
        return True

    def kill_eap(self):
        self.eap_power()
        self.web_session.web_driver.find_element_by_xpath("//a[@title='Kill this server']").click()
        ui_utils(self.web_session).accept_alert(20)
        assert ui_utils(self.web_session).waitForTextOnPage("Kill initiated for selected server(s)", 15)
        return True

    def reload_eap(self):
        self.eap_power()
        self.web_session.web_driver.find_element_by_xpath("//a[contains(@id,'reload')]").click()
        ui_utils(self.web_session).accept_alert(20)
        assert ui_utils(self.web_session).waitForTextOnPage("Reload initiated for selected server(s)", 15)
        return True

    def suspend_eap(self):
        self.eap_power()
        self.web_session.web_driver.find_element_by_xpath("//a[contains(@id,'suspend')]").click()
        ui_utils(self.web_session).sleep(10)
        self.web_session.web_driver.find_element_by_xpath("//button[@alt='Suspend']").click()
        assert ui_utils(self.web_session).waitForTextOnPage("Suspend initiated for selected server(s)", 15)
        return True

    def resume_eap(self):
        self.eap_power()
        self.web_session.web_driver.find_element_by_xpath("//a[contains(@id,'resume')]").click()
        ui_utils(self.web_session).accept_alert(20)
        ui_utils(self.web_session).sleep(10)
        assert ui_utils(self.web_session).waitForTextOnPage("Resume initiated for selected server(s)", 15)
        return True

    def start_eap(self):
        self.eap_power()
        self.web_session.web_driver.find_element_by_xpath("//a[contains(@title,'Start this server')]").click()
        ui_utils(self.web_session).accept_alert(20)
        assert ui_utils(self.web_session).waitForTextOnPage("Resume initiated for selected server(s)", 20)
        return True







