from common.ui_utils import ui_utils
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from common.ui_utils import ui_utils
from hawkular.hawkular_api import hawkular_api
from common.db import db


class server_group_deploymnt():
    web_session = None
    web_driver = None
    ui_utils = None
    db = None
    hawkular_api = None

    def __init__(self, web_session):
        self.web_session = web_session
        self.web_driver = web_session.web_driver
        self.hawkular_api = hawkular_api(self.web_session)

    def add_deployment(self):
        self.web_session.web_driver.get("{}/middleware_domain/show_list".format(self.web_session.MIQ_URL))
        #assert ui_utils(self.web_session).waitForTextOnPage("Middleware Domains", 15)
        self.web_session.web_driver.find_element_by_xpath("//td[contains(.,'Unnamed Domain')]").click()
        #assert ui_utils(self.web_session).waitForTextOnPage("Unnamed Domain (Summary)", 15)
        self.web_session.web_driver.find_element_by_xpath("//td[contains(.,'Middleware Server Groups')]").click()
        #assert ui_utils(self.web_session).waitForTextOnPage("Server Group Name ", 15)
        self.web_session.web_driver.find_element_by_xpath("//td[contains(.,'other-server-group')]").click()
        #assert ui_utils(self.web_session).waitForTextOnPage("Properties ", 15)
        self.web_session.web_driver.find_element_by_xpath("//button[@title='Deployments']").click()
        self.web_session.web_driver.find_element_by_xpath("//a[@title='Add a new Deployment']").click()

        self.web_driver.switch_to_alert()

        #assert ui_utils(self.web_session).waitForElementOnPage(By.ID,'deploy_div',15)

        #for handle in self.web_driver.window_handles:
         #self.web_driver.switch_to_window(handle)
         #self.web_session.logger.info("switch to new window")


        self.web_session.logger.info("switch to new window")
        #assert ui_utils(self.web_session).waitForTextOnPage("Add Middleware Deployment ", 15)

        button=self.web_session.web_driver.find_element_by_xpath("//span[@class='buttonText']")
        button.send_keys("/home/pyadav/clusterwebapp/ClusterWebApp.war")

        self.web_session.web_driver.find_element_by_xpath("//button[@alt='Deploy']").click()

        return True








