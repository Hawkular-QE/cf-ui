from common.ui_utils import ui_utils
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from views.servers import servers
import os
from common.navigate import navigate

from common.ui_utils import ui_utils
from hawkular.hawkular_api import hawkular_api
from common.db import db
import pytest


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
        self.ui_utils = ui_utils(self.web_session)

    def add_deployment(self, app_to_deploy,runtime_name=None, enable_deploy=True, overwrite=False, cancel=False):

        app = "{}/data/{}".format(os.getcwd(), app_to_deploy)

        navigate(self.web_session).get("{}/middleware_domain/show_list".format(self.web_session.MIQ_URL))
        assert ui_utils(self.web_session).waitForTextOnPage("master", 15)

        domains_ui = self.ui_utils.get_list_table()
        if not domains_ui:
            self.web_session.logger.warning("No Domains found.")
            pytest.skip("Skip test - No Domains found.")

        self.ui_utils.click_on_row_containing_text(domains_ui[0].get('Domain Name'))
        assert ui_utils(self.web_session).waitForTextOnPage("State", 15)
        self.web_session.web_driver.find_element_by_xpath("//td[contains(.,'Middleware Server Groups')]").click()
        assert ui_utils(self.web_session).waitForTextOnPage("Server Group Name", 30)
        self.web_session.web_driver.find_element_by_xpath("//td[contains(.,'other-server-group')]").click()
        assert ui_utils(self.web_session).waitForTextOnPage("other-server-group (Summary)", 15)

        self.web_session.web_driver.find_element_by_xpath("//button[@title='Deployments']").click()
        self.web_session.web_driver.find_element_by_xpath("//a[@title='Add a new Deployment']").click()

        self.web_session.logger.info("Deploying App: {}".format(app))
        assert ui_utils(self.web_session).waitForTextOnPage("Select the file to deploy", 15)

        el = self.web_session.web_driver.find_element_by_id("upload_file")
        el.send_keys(app)
        ui_utils(self.web_session).sleep(2)

        if cancel:
            self.web_driver.find_element_by_xpath(".//*[@id='deploy_div']//button[1]").click()
        elif runtime_name:
            self.web_driver.find_element_by_id('runtime_name_input').clear()
            self.web_driver.find_element_by_id('runtime_name_input').send_keys(runtime_name)
            self.web_driver.find_element_by_xpath("//button[@ng-click='addDeployment()']").click()
            assert ui_utils(self.web_session).waitForTextOnPage('Deployment "{}" has been initiated on this group.'.format(runtime_name), 30)

        elif overwrite:
            self.web_driver.find_element_by_xpath("//*[contains(@class,'bootstrap-switch bootstrap-switch-wrapper bootstrap-switch-off bootstrap-switch-id-force_deployment_cb bootstrap-switch-animate')]").click()
            self.web_driver.find_element_by_xpath("//button[@ng-click='addDeployment()']").click()
            assert ui_utils(self.web_session).waitForTextOnPage('Deployment "{}" has been initiated on this group.'.format(app_to_deploy), 30)

        elif not enable_deploy:
            self.web_driver.find_element_by_xpath("//span[contains(.,'Yes')]").click()
            self.web_driver.find_element_by_xpath("//button[@ng-click='addDeployment()']").click()
            assert ui_utils(self.web_session).waitForTextOnPage('Deployment "{}" has been initiated on this group.'.format(app_to_deploy), 30)
        else:
            self.web_driver.find_element_by_xpath("//button[@ng-click='addDeployment()']").click()
            assert ui_utils(self.web_session).waitForTextOnPage('Deployment "{}" has been initiated on this group.'.format(app_to_deploy), 30)

        return True







