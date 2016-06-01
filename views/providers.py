from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from common.ui_utils import ui_utils
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from conf.properties import properties

class providers():
    web_session = None

    def __init__(self, web_session):
        self.web_session = web_session
        self.web_driver = web_session.web_driver

    def add_provider(self, providerName, hostName, port):
        self.providerName = providerName
        self.hostName = hostName
        self.port = port

        self.web_session.logger.info("Adding Middleware Provider to ManageIQ instance")

        #Navigate to Middleware Provider list page

        elem_compute = self.web_driver.find_element_by_xpath("//a[contains(@href,'/dashboard/maintab/?tab=compute')]")
        ActionChains(self.web_driver).move_to_element(elem_compute).perform()
        time.sleep(5)
        assert ui_utils(self.web_session).waitForTextOnPage("Middleware", 15)
        elem_middleware = self.web_driver.find_element_by_xpath("//a[contains(@href,'/dashboard/maintab/?tab=mdl')]")
        ActionChains(self.web_driver).move_to_element(elem_middleware).perform()
        time.sleep(5)
        assert ui_utils(self.web_session).waitForTextOnPage("Providers", 15)
        elem_providers = self.web_driver.find_element_by_xpath("//a[contains(@href,'/ems_middleware')]")
        elem_providers.click()
        assert ui_utils(self.web_session).waitForTextOnPage("Configuration", 15)

        # Navigate to add Provider form:

        elem_config = self.web_driver.find_element_by_xpath("//button[@title='Configuration']")
        elem_config.click()
        assert ui_utils(self.web_session).waitForTextOnPage("Add a New Middleware Provider", 15)
        elem_addNewProvider = self.web_driver.find_element_by_xpath("//a[@title='Add a New Middleware Provider']")
        elem_addNewProvider.click()
        assert ui_utils(self.web_session).waitForTextOnPage("Basic Information", 15)

        #Enter the form details and submit to add the provider

        elem_providerName = self.web_driver.find_element_by_xpath("//input[@id='name']")
        elem_providerName.send_keys(self.providerName)

        self.web_driver.find_element_by_xpath("//button[@data-id='server_emstype']").click()
        self.web_driver.find_element_by_xpath("//span[contains(.,'Hawkular')]").click()
        assert ui_utils(self.web_session).waitForTextOnPage("Hostname or IP address", 30)

        elem_providerHostname = self.web_driver.find_element_by_xpath("//input[@id='hostname']")
        elem_providerHostname.send_keys(self.hostName)

        elem_providerPort = self.web_driver.find_element_by_xpath("//input[@id='port']")
        elem_providerPort.send_keys(self.port)
        elem_hawkularUser = self.web_driver.find_element_by_xpath("//input[@id='default_userid']")
        elem_hawkularUser.send_keys(properties.HAWKULAR_USERNAME)
        elem_hawkularPassword = self.web_driver.find_element_by_xpath("//input[@id='default_password']")
        elem_hawkularPassword.send_keys(properties.HAWKULAR_PASSWORD)
        elem_hawkularVerifyPassword = self.web_driver.find_element_by_xpath("//input[@id='default_verify']")
        elem_hawkularVerifyPassword.send_keys(properties.HAWKULAR_PASSWORD)
        self.web_driver.find_element_by_xpath("//button[@alt='Add this Middleware Provider']").click()

        assert ui_utils(self.web_session).waitForTextOnPage('Middleware Providers "{}" was saved'.format(self.providerName), 15)
        elem_provider = self.web_driver.find_element_by_xpath("//a[contains(@title,'Name: {}')]".format(self.providerName))

        #TO-DO Replace below with assert using isElementOnPage method(to be written) in ui_util.py
        if elem_provider.is_displayed():
            self.web_session.logger.info("Middleware Provider added successfully.")

    def delete_provider(self):
        self.web_session.logger.info("To Do")
        # navigate_to_providers
        # delete_provider()

    def update_provider(self):
        self.web_session.logger.info("To Do")
        # navigate_to_providers
        # update_provider

    def add_provider_if_not_present(self):
        self.web_session.logger.info("To Do")
        # navigate_to_providers
        # If provider is not present, add provider

    def does_provider_exist(self):
        self.web_session.logger.info("To Do")
        # navigate_to_providers
        # is_provider_present (note: use ui_utils.isTextOnPage OR create new ui_utils.isElementPresent)