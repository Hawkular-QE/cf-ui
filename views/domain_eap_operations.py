from common.ui_utils import ui_utils
from domains import domains
from servers import servers
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from common.session import session
import pytest
from common.navigate import navigate

class domain_eap_operations():

    web_session = None
    power_stop = {'action': 'Stop Server', 'wait_for': 'Stop initiated for selected server', 'start_state': 'running',
                  'end_state': None}
    power_restart = {'action': 'Restart Server', 'wait_for': 'Restart initiated for selected server',
                     'start_state': 'running', 'end_state': 'running'}
    power_start = {'action': 'Start Server', 'wait_for': 'Start initiated for selected server',
                     'start_state': None, 'end_state': None}
    power_reload = {'action': 'Reload Server', 'wait_for': 'Reload initiated for selected server',
                    'start_state': 'running', 'end_state': 'running'}
    power_kill = {'action': 'Kill Server',
                               'wait_for': 'Kill initiated for selected server', 'start_state': 'running',
                               'end_state': None}
    power_suspend = {'action': 'Suspend Server', 'wait_for': 'Suspend initiated for selected server',
                     'start_state': 'running', 'end_state': 'running'}
    power_resume = {'action': 'Resume Server', 'wait_for': 'Resume initiated for selected server',
                    'start_state': 'running', 'end_state': 'running'}

    def __init__(self, web_session):

        self.web_session = web_session
        self.web_driver = web_session.web_driver
        self.ui_utils = ui_utils(self.web_session)
        self.domains = domains(self.web_session)
        self.servers = servers(self.web_session)
        self.provider_name = self.web_session.HAWKULAR_PROVIDER_NAME

    def stop_eap(self):

        power = self.power_stop
        self.nav_to_single_server()
        self.web_session.logger.info("About to Stop EAP server one")
        self.eapdomain_power_action(power)
        self.ui_utils.sleep(5)

        return True

    def restart_eap(self):

        power = self.power_restart
        self.nav_to_single_server()
        self.web_session.logger.info("About to Restart EAP server one")
        self.eapdomain_power_action(power)
        self.ui_utils.sleep(5)

        return True

    def kill_eap(self):

        power = self.power_kill
        self.nav_to_single_server()
        self.web_session.logger.info("About to Kill EAP server one")
        self.eapdomain_power_action(power)
        self.ui_utils.sleep(5)

        return True

    def reload_eap(self):

        power = self.power_reload
        self.nav_to_single_server()
        self.web_session.logger.info("About to Reload EAP server one")
        self.eapdomain_power_action(power)
        self.ui_utils.sleep(5)

        return True

    def suspend_eap(self):

        power = self.power_suspend
        self.nav_to_single_server()
        self.web_session.logger.info("About to Suspend EAP server one")
        self.eapdomain_power_action(power, alert_button_name='Suspend')
        self.ui_utils.sleep(5)

        return True

    def resume_eap(self):

        power = self.power_resume
        self.nav_to_single_server()
        self.web_session.logger.info("About to Resume EAP server one")
        self.eapdomain_power_action(power)
        self.ui_utils.sleep(5)

        return True

    def start_eap(self):

        power = self.power_start
        self.nav_to_single_server()
        self.web_session.logger.info("About to Start EAP server one")
        self.eapdomain_power_action(power)
        self.ui_utils.sleep(5)

        return True

    def nav_to_single_server(self):
        navigate(self.web_session).get("{}/middleware_domain/show_list".format(self.web_session.MIQ_URL))
        assert self.ui_utils.waitForTextOnPage(self.provider_name, 30)
        domains_ui = self.ui_utils.get_list_table()

        if not domains_ui:
            self.web_session.logger.warning("No Domains found.")
            pytest.skip("Skip test - No Domains found.")

        self.domains.nav_to_all_middleware_server_groups(domains_ui[0].get('Domain Name'))
        assert ui_utils(self.web_session).waitForTextOnPage("Server Group Name", 30)
        self.web_session.web_driver.find_element_by_xpath("//td[contains(.,'main-server-group')]").click()
        assert ui_utils(self.web_session).waitForTextOnPage("Middleware Servers", 30)
        self.web_session.web_driver.find_element_by_xpath("//td[contains(.,'Middleware Servers')]").click()
        assert ui_utils(self.web_session).waitForTextOnPage("server-one", 30)
        self.web_session.web_driver.find_element_by_xpath("//td[contains(.,'server-one')]").click()
        assert ui_utils(self.web_session).waitForTextOnPage("Properties", 30)

        return True

    def eapdomain_power_action(self, power, alert_button_name=None):

        self.web_session.logger.info("About to {} EAP server".format(power.get('action')))

        self.web_driver.find_element_by_xpath("//button[@title='Power']").click()
        self.ui_utils.waitForElementOnPage(By.XPATH, "//a[contains(.,'{}')]".format(power.get('action')), 5)
        self.web_driver.find_element_by_xpath("//a[contains(.,'{}')]".format(power.get('action'))).click()
        self.ui_utils.accept_alert(10, alert_button_name)
        assert self.ui_utils.waitForTextOnPage(power.get('wait_for'), 15)

        # To Do - Validate expected end state











