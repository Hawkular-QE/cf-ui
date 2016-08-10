from common.ui_utils import ui_utils
from parsing.table import table
from navigation.navigation import NavigationTree
from hawkular.hawkular_api import hawkular_api
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os
import time
from common.db import db
from common.ssh import ssh
import socket

class servers():
    web_session = None
    web_driver = None
    ui_utils = None
    hawkular_api = None
    db = None
    EAP_JON_HOME = '/root/jboss-eap-7.0'
    EAP_WILDFLY_HOME = '/root/wildfly-'
    EAP_PROCESS = 'standalone.sh'

    power_stop = {'action':'Stop Server', 'wait_for':'Stop initiated for selected server', 'start_state':'running', 'end_state':None}
    power_restart = {'action': 'Restart Server', 'wait_for': 'Restart initiated for selected server', 'start_state': 'running', 'end_state': 'running'}
    # TO-DO - Validate Start / End states:
    power_reload = {'action': 'Reload Server', 'wait_for': 'Reload initiated for selected server', 'start_state':'running', 'end_state':'running'}
    power_graceful_shutdown = {'action': 'Gracefully shutdown Server', 'wait_for': 'Shutdown initiated for selected server', 'start_state':'running', 'end_state':'running'}
    power_suspend = {'action': 'Suspend Server', 'wait_for': 'Suspend initiated for selected server', 'start_state':'running', 'end_state':'running'}
    power_resume = {'action': 'Resume Server', 'wait_for': 'Resume initiated for selected server', 'start_state':'stopped', 'end_state':'running'}

    APPLICATION_WAR = "cfui_test_war.war"
    APPLICATION_JAR = "cfui_test_jar.jar"
    APPLICATION_EAR = "cfui_test_ear.ear"

    def __init__(self, web_session):
        self.web_session = web_session
        self.web_driver = web_session.web_driver
        self.ui_utils = ui_utils(self.web_session)
        self.hawkular_api = hawkular_api(self.web_session)

        try:
            self.db = db(self.web_session)
        except Exception, e:
            self.web_session.logger.warning("Unable to connecto to database. {}".format(e))

    def server_policy_edit(self, server_type):
        origValue = -1
        server = None

        servers_ui = table(self.web_session).get_middleware_servers_table()
        assert servers_ui, "No servers found."

        if server_type == 'provider':
            server = self.ui_utils.find_row_in_list(servers_ui, 'Product', self.web_session.PROVIDER)
        elif server_type == 'eap':
            for eap in {'WildFly', 'JBoss'}:
                server = self.ui_utils.find_row_in_list(servers_ui, 'Product', eap)
                if server: break

        assert server, "No server {} found.".format(server)

        # Feed is unique ID for this server
        self.ui_utils.click_on_row_containing_text(server.get('Feed'))

        server_details = self.ui_utils.get_generic_table_as_dict()
        assert server_details, "No server details found for {}.".format(self.web_session.PROVIDER)

        if not str(server_details.get('My Company Tags')).__contains__("No My Company Tags have been assigned"):
            origValue = int(server_details.get('My Company Tags')[-1:])

        self.web_session.logger.info("Current Company Tags: {}".format(origValue))

        self.web_driver.find_element_by_id('middleware_server_policy_choice').click()
        self.web_driver.find_element_by_id('middleware_server_policy_choice__middleware_server_tag').click()
        self.ui_utils.waitForTextOnPage('Tag Assignment', 5)

        # Click on Drop-down title Name
        tag = '"&lt;Select a value to assign&gt;"'
        self.web_driver.execute_script("return $('*[data-original-title={}]').trigger('click')".format(tag))
        self.ui_utils.sleep(1)

        # Select value - always just select first value in list (list is index):
        # By Browser type - for now - to-do, find a better approach
        if self.web_session.BROWSER == 'Firefox':
            self.web_driver.find_element_by_xpath('//th[3]/div/div/div/ul/li[1]/a').click()
        else:
            tag = 'data-original-index=1'
            el = self.web_driver.execute_script("return $('*[{}]')".format(tag))
            try:
                el[0].click()
            except:
                el[1].click()

        # To-Do: Need a better polling/wait mechanism
        self.ui_utils.sleep(3)

        el = self.web_driver.find_elements_by_xpath("//*[contains(text(), '{}')]".format('Save'))
        el[0].click()

        self.ui_utils.waitForTextOnPage("My Company Tags", 5)

        server_details = self.ui_utils.get_generic_table_as_dict()
        newValue = server_details.get('My Company Tags')[-1:]

        if newValue != origValue:
            return True
        else:
            return False


    def validate_server_details(self):

        servers_ui = table(self.web_session).get_middleware_servers_table()
        servers_hawk = self.hawkular_api.get_hawkular_servers()

        for serv_ui in servers_ui:
            feed = serv_ui.get('Feed')  # Unique Server identifier
            self.web_session.web_driver.get("{}/middleware_server/show_list".format(self.web_session.MIQ_URL))

            self.ui_utils.click_on_row_containing_text(serv_ui.get('Feed'))
            self.ui_utils.waitForTextOnPage("Properties", 15)

            server_details_ui = self.ui_utils.get_generic_table_as_dict()
            server_details_hawk = self.ui_utils.find_row_in_list(servers_hawk, 'Feed', feed)

            assert server_details_hawk, "Feed {} not found in Hawkular Server List".format(feed)

            assert (server_details_ui.get('Product') == server_details_hawk.get("details").get("Product Name")), \
                    "Product mismatch ui:{}, hawk:{}".format(server_details_ui.get('Product'), server_details_hawk.get("details").get("Product Name"))
            assert (server_details_ui.get('Version') == server_details_hawk.get("details").get("Version")), \
                    "Version mismatch ui:{}, hawk:{}".format(server_details_ui.get('Version'), server_details_hawk.get("details").get("Version"))

        return True

    def validate_servers_list(self):
        servers_db = None
        servers_ui = table(self.web_session).get_middleware_servers_table()
        servers_hawk = self.hawkular_api.get_hawkular_servers()

        if self.db:
            servers_db = self.db.get_servers()
            assert len(servers_ui) == len(servers_hawk) == len(servers_db), "Servers lists size mismatch."
        else:
            assert len(servers_ui) == len(servers_hawk), "Servers lists size mismatch."

        for serv_ui in servers_ui:
            serv_hawk = self.ui_utils.find_row_in_list(servers_hawk, 'Feed', serv_ui.get('Feed'))

            assert serv_hawk, "Feed {} not found in Hawkular Server".format(serv_ui.get('Feed'))
            assert (serv_ui.get('Host Name') == serv_hawk.get("details").get("Hostname")), \
                "Host Name mismatch ui:{}, hawk:{}".format(serv_ui.get('Feed'), serv_hawk.get("details").get("Hostname"))
            assert (serv_ui.get('Product') == serv_hawk.get("details").get("Product Name")), \
                "Product mismatch ui:{}, hawk:{}".format(serv_ui.get('Product'), serv_hawk.get("Product Name"))

        return True

    # BEGIN - EAP Power

    def __get_eap_app_path(self,eap_hawk):

        if "wildfly" in (eap_hawk.get('Product Name').lower()):
            return "{}{}/".format(self.EAP_WILDFLY_HOME,eap_hawk.get("details").get("Version"))
        else:
            return "{}/".format(self.EAP_JON_HOME)

    def eap_power_restart(self):

        # Find an EAP in 'start state'
        # Get EAP pid
        # Restart EAP
        # Validate that pid changed

        power = self.power_restart

        eap_hawk = self.find_non_container_eap_in_state(power.get('start_state'))
        assert eap_hawk

        # Example format: Djboss.server.base.dir=/root/wildfly-10.0.0.Final/standalone
        eap_app = "{}{}{}".format("Djboss.server.base.dir=", self.__get_eap_app_path(eap_hawk), "standalone")

        eap_host = eap_hawk.get("details").get("Hostname")
        ssh_ = ssh(self.web_session, eap_host)
        orig_pid = ssh_.get_pid(eap_app)

        self.web_session.logger.info("About to Restart EAP server {} Feed {}".format(eap_hawk.get('Product'), eap_hawk.get('Feed')))
        self.eap_power_action(power, eap_hawk)
        self.ui_utils.sleep(5)  # need a timer here
        print "eap_app: ", eap_app
        new_pid = ssh_.get_pid(eap_app)

        assert orig_pid != new_pid, "Orig Pid: {}  New Pid: {}".format(orig_pid, new_pid)

        return True

    def eap_power_stop(self):
        pid = None

        power = self.power_stop

        # Find an EAP in 'start state'
        # Get EAP pid (should be a pid)
        # Stop EAP
        # Validate that no pid (EAP has stopped)

        eap_hawk = self.find_non_container_eap_in_state(power.get('start_state'))
        assert eap_hawk

        # Example format: Djboss.server.base.dir=/root/wildfly-10.0.0.Final/standalone
        eap_app = "{}{}{}".format("Djboss.server.base.dir=", self.__get_eap_app_path(eap_hawk), "standalone")

        eap_hostname = eap_hawk.get("details").get("Hostname")
        ssh_ = ssh(self.web_session, eap_hostname)
        assert ssh_.get_pid(eap_app) != None, "No EAP pid found."

        self.eap_power_action(power, eap_hawk)
        self.ui_utils.sleep(3)
        assert ssh_.get_pid(eap_app) == None, "EAP pid unexpectedly found."

        start_str = 'nohup {}{} -Djboss.service.binding.set=ports-01 -b=0.0.0.0 -bmanagement=0.0.0.0  > /dev/null 2>&1 &\n'.format(self.__get_eap_app_path(eap_hawk), "bin/standalone.sh")
        self.web_session.logger.debug("About to start EAP: {}".format(start_str))
        ssh_.execute_command(start_str)
        assert ssh_.get_pid(eap_app) != None, "EAP pid not found."

        return True

    def eap_power_reload(self):
        power = self.power_reload

        # Find an EAP in 'start state'
        # Reload EAP
        # Validate - TO-DO

        eap_hawk = self.find_non_container_eap_in_state(power.get('start_state'))
        assert eap_hawk

        self.eap_power_action(power, eap_hawk)

        # TO-DO - Validate

        return True

    def eap_power_suspend(self):
        power = self.power_suspend

        # Find an EAP in 'start state'
        # Suspend EAP
        # Validate - TO-DO

        eap_hawk = self.find_non_container_eap_in_state(power.get('start_state'))
        assert eap_hawk

        self.eap_power_action(power, eap_hawk)

        # TO-DO - Validate

        return True

    def eap_power_resume(self):
        power = self.power_resume

        # Find an EAP in 'start state'
        # Resume EAP
        # Validate - TO-DO

        eap_hawk = self.find_non_container_eap_in_state(power.get('start_state'))
        assert eap_hawk

        self.eap_power_action(power, eap_hawk)

        # TO-DO - Validate

        return True

    def eap_power_graceful_shutdown(self):
        power = self.power_graceful_shutdown

        # Find an EAP in 'start state'
        # Graceful-Shutdown EAP
        # Validate - TO-DO

        eap_hawk = self.find_non_container_eap_in_state(power.get('start_state'))
        assert eap_hawk

        self.eap_power_action(power, eap_hawk)

        # TO-DO - Validate

        return True

    def eap_power_action(self, power, eap_hawk):

        self.web_session.logger.info(
            "About to {} EAP server {} Feed {}".format(power.get('action'), eap_hawk.get('Product'), eap_hawk.get('Feed')))

        feed = eap_hawk.get('Feed') # Unique server id

        NavigationTree(self.web_session).navigate_to_middleware_servers_view()

        self.ui_utils.click_on_row_containing_text(eap_hawk.get('Feed'))
        self.ui_utils.waitForTextOnPage("Properties", 15)

        self.web_driver.find_element_by_xpath("//button[@title='Power']").click()
        self.web_driver.find_element_by_xpath("//a[contains(.,'{}')]".format(power.get('action'))).click()
        self.web_driver.switch_to_alert().accept()
        assert self.ui_utils.waitForTextOnPage(power.get('wait_for'), 15)

        # Validate backend - Hawkular
        if power.get('end_state'):
            assert self.wait_for_eap_state(feed, power.get('end_state'), 15)

    def deploy_application_archive(self, app_to_deploy = APPLICATION_WAR):

        NavigationTree(self.web_session).navigate_to_middleware_servers_view()

        # Find EAP on which to deploy
        eap = self.find_non_container_eap_in_state("running")
        assert eap, "No EAP found in desired state."

        self.ui_utils.click_on_row_containing_text(eap.get('Feed'))
        self.ui_utils.waitForTextOnPage('Version', 15)

        self.add_server_deployment(self.APPLICATION_WAR)

        # Validate UI
        self.web_session.web_driver.get("{}/middleware_deployment/show_list".format(self.web_session.MIQ_URL))
        # deployments_ui = table(self.web_session).get_middleware_deployments_table()
        #assert self.ui_utils.find_row_in_list(deployments_ui, "Deployment Name", self.APPLICATION_WAR), "Deployment {} not found on UI.".format(app_to_deploy)
        self.ui_utils.refresh_until_text_appears(self.APPLICATION_WAR, 300)
        self.ui_utils.click_on_row_containing_text(app_to_deploy)
        assert self.ui_utils.refresh_until_text_appears('Enabled', 300)

        # Validate DB
        deployments_db = self.db.get_deployments()
        assert self.ui_utils.find_row_in_list(deployments_db, "name", self.APPLICATION_WAR), "Deployment {} not found in DB.".format(app_to_deploy)

        # Validate HS API
        deployments_hawk = hawkular_api(self.web_session).get_hawkular_deployments()
        assert self.ui_utils.find_row_in_list(deployments_hawk, "Name", self.APPLICATION_WAR), "Deployment {} not found in Hawkular.".format(app_to_deploy)

        return True

    def undeploy_application_archive(self, app_to_undeploy=APPLICATION_WAR):
        NavigationTree(self.web_session).navigate_to_middleware_deployment_view()

        deployments_ui = table(self.web_session).get_middleware_deployments_table()
        self.ui_utils.click_on_row_containing_text(app_to_undeploy)

        # Undeploy
        self.undeploy_server_deployment(app_to_undeploy)

        # Validate that application is "Disabled"
        assert self.ui_utils.refresh_until_text_appears('Disabled', 300)

        return True

    def redeploy_application_archive(self, app_to_redeploy=APPLICATION_WAR):

        # Find EAP with application to redeploy
        NavigationTree(self.web_session).navigate_to_middleware_deployment_view()

        deployments_ui = table(self.web_session).get_middleware_deployments_table()
        self.ui_utils.click_on_row_containing_text(app_to_redeploy)

        # Redeploy

        self.redeploy_server_deployment(app_to_redeploy)

        # Validate that application status is enabled:
        # ( Existing issues: https://github.com/ManageIQ/manageiq/issues/9876, Issue#10138 )

        assert self.ui_utils.refresh_until_text_appears('Enabled', 300)
        return True

    def stop_application_archive(self, app_to_stop=APPLICATION_WAR):

        # Find EAP with application to stop
        NavigationTree(self.web_session).navigate_to_middleware_deployment_view()

        deployments_ui = table(self.web_session).get_middleware_deployments_table()
        self.ui_utils.click_on_row_containing_text(app_to_stop)

        # Stop the application archive

        self.stop_server_deployment(app_to_stop)

        # Validate that application status is Disabled:
        # ( Existing issues: https://github.com/ManageIQ/manageiq/issues/10138 )

        assert self.ui_utils.refresh_until_text_appears('Disabled', 300)
        return True

    def start_application_archive(self, app_to_start=APPLICATION_WAR):

        # Find EAP with application to start
        NavigationTree(self.web_session).navigate_to_middleware_deployment_view()

        deployments_ui = table(self.web_session).get_middleware_deployments_table()
        self.ui_utils.click_on_row_containing_text(app_to_start)

        # Start the application archive

        self.start_server_deployment(app_to_start)

        # Validate that application status is Enabled:
        # ( Existing issues: https://github.com/ManageIQ/manageiq/issues/10138 )

        assert self.ui_utils.refresh_until_text_appears('Enabled', 300)
        return True

    def wait_for_eap_state(self, feed, expected_state, wait_time):
        currentTime = time.time()

        while True:
            servers_hawk = self.hawkular_api.get_hawkular_servers()
            assert servers_hawk, "No Hawkular Servers found."

            eap = self.ui_utils.find_row_in_list(servers_hawk, 'Feed', feed)
            assert eap, "No EAP found for Feed {}".format(feed)
            current_state = eap.get("details").get("Server State")

            if current_state == expected_state:
                self.web_session.logger.info("Feed {} found to be in state {}".format(feed, expected_state))
                break
            else:
                if time.time() - currentTime >= wait_time:
                    self.web_session.logger.error("Timed out waiting for EAP Feed {} to be in state {}, but is in state {}.".format(feed, expected_state, current_state))
                    return False
                else:
                    time.sleep(2)

        return True

    def find_eap_in_state(self, state):
        for row in self.hawkular_api.get_hawkular_servers():
            if row.get("Product Name") != 'Hawkular' and (state.lower() == "any" or row.get("details").get("Server State") == state.lower()):
                return row

        return None

    # EAPs that are running in a container will NOT have a resolvable Hostname (Hostname will be either POD or Container ID)
    def find_non_container_eap_in_state(self, state):
        for row in self.hawkular_api.get_hawkular_servers():
            if row.get("Product Name") != 'Hawkular' and (state.lower() == "any" or row.get("details").get("Server State") == state.lower()):
                    ip = row.get("details").get("Hostname")
                    try:
                        socket.gethostbyaddr(ip)
                        self.web_session.logger.info("Found EAP Hostname: {}  state: {}".format(ip, state))
                        return row
                    except:
                        self.web_session.logger.info("Note a resolvable Hostname/IP: {}".format(ip))

        return None

    def add_server_deployment(self, app_to_deploy):
        app = "{}/data/{}".format(os.getcwd(), app_to_deploy)

        self.web_session.logger.info("Deploying App: {}".format(app))

        self.web_driver.find_element_by_id('middleware_server_deployments_choice').click()
        self.web_driver.find_element_by_id('middleware_server_deployments_choice__middleware_deployment_add').click()
        self.ui_utils.waitForTextOnPage('Select the file to deploy', 15)

        el = self.web_driver.find_element_by_id("upload_file")
        el.send_keys(app)

        self.web_driver.find_element_by_xpath("//button[@ng-click='addDeployment()']").click()
        self.ui_utils.waitForTextOnPage('Deployment "{}" has been initiated on this server.'.format(app_to_deploy), 15)

    def undeploy_server_deployment(self, app_to_undeploy = APPLICATION_WAR):
        self.web_session.logger.info("Undeploying App: {}".format(app_to_undeploy))
        self.web_driver.find_element_by_id('middleware_deployment_deploy_choice').click()
        self.web_driver.find_element_by_id('middleware_deployment_deploy_choice__middleware_deployment_undeploy').click()
        self.ui_utils.sleep(2)
        self.web_driver.switch_to_alert().accept()
        self.ui_utils.waitForTextOnPage('Undeployment initiated for selected deployment(s)', 15)

    def redeploy_server_deployment(self, app_to_redeploy=APPLICATION_WAR):
        self.web_session.logger.info("Redeploying App: {}".format(app_to_redeploy))
        self.web_driver.find_element_by_id('middleware_deployment_deploy_choice').click()
        self.web_driver.find_element_by_id(
            'middleware_deployment_deploy_choice__middleware_deployment_redeploy').click()
        self.ui_utils.sleep(2)
        self.web_driver.switch_to_alert().accept()
        self.ui_utils.waitForTextOnPage('Redeployment initiated for selected deployment(s)', 15)

    def stop_server_deployment(self, app_to_stop=APPLICATION_WAR):
        self.web_session.logger.info("Stopping App: {}".format(app_to_stop))
        self.web_driver.find_element_by_id('middleware_deployment_deploy_choice').click()
        self.web_driver.find_element_by_id(
            'middleware_deployment_deploy_choice__middleware_deployment_stop').click()
        self.ui_utils.sleep(2)
        self.web_driver.switch_to_alert().accept()
        self.ui_utils.waitForTextOnPage('Stop initiated for selected deployment(s)', 15)

    def start_server_deployment(self, app_to_start=APPLICATION_WAR):
        self.web_session.logger.info("Starting App: {}".format(app_to_start))
        self.web_driver.find_element_by_id('middleware_deployment_deploy_choice').click()
        self.web_driver.find_element_by_id(
            'middleware_deployment_deploy_choice__middleware_deployment_start').click()
        self.ui_utils.sleep(2)
        self.web_driver.switch_to_alert().accept()
        self.ui_utils.waitForTextOnPage('Start initiated for selected deployment(s)', 15)

    def wait_for_deployment_state(self, deployment_name, state, wait_time):
        currentTime = time.time()
        deployment = None

        self.web_session.logger.info("Wait for Deployment: {} to be in state: ".format(deployment_name, state))

        while True:
            deployments = self.db.get_deployments()
            for row in deployments:
                if deployment_name in row['name']:
                    deployment = row
                    break

            assert deployment, "Deployment: {} not found in DB".format(deployment_name)

            if state.lower() == deployment['status'].lower():
                break
            else:
                if time.time() - currentTime >= wait_time:
                    self.web_session.logger.error(
                        "Timed out waiting for Deployment {} to be in state {}.".format(deployment_name, state))
                    return False
                else:
                    time.sleep(2)

        return True
