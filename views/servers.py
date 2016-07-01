from common.ui_utils import ui_utils
from parsing.table import table
from navigation.navigation import NavigationTree
from hawkular.hawkular_api import hawkular_api
import time

class servers():
    web_session = None
    web_driver = None
    ui_utils = None
    hawkular_api = None

    power_stop = {'action':'Stop Server', 'wait_for':'Stop initiated for selected server', 'start_state':'running', 'end_state':'stopped'}
    power_reload = {'action': 'Reload Server', 'wait_for': 'Reload initiated for selected server', 'start_state':'running', 'end_state':'running'}

    def __init__(self, web_session):
        self.web_session = web_session
        self.web_driver = web_session.web_driver
        self.ui_utils = ui_utils(self.web_session)
        self.hawkular_api = hawkular_api(self.web_session)

    def server_policy_edit(self, product):
        origValue = -1

        servers_ui = table(self.web_session).get_middleware_servers_table()
        server = self.ui_utils.find_row_in_list(servers_ui, 'Product', product)
        assert server, "No server {} found.".format(product)

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
        servers_ui = table(self.web_session).get_middleware_servers_table()
        servers_hawk = self.hawkular_api.get_hawkular_servers()

        assert len(servers_ui) == len(servers_hawk), "Servers lists size mismatch."

        for serv_ui in servers_ui:
            serv_hawk = self.ui_utils.find_row_in_list(servers_hawk, 'Feed', serv_ui.get('Feed'))

            assert serv_hawk, "Feed {} not found in Hawkular Server".format(serv_ui.get('Feed'))
            assert (serv_ui.get('Host Name') == serv_hawk.get("details").get("Hostname")), \
                "Host Name mismatch ui:{}, hawk:{}".format(serv_ui.get('Feed'), serv_hawk.get("details").get("Hostname"))
            assert (serv_ui.get('Product') == serv_hawk.get("details").get("Product Name")), \
                "Product mismatch ui:{}, hawk:{}".format(serv_ui.get('Product'), serv_hawk.get("details").get("Product Name"))

        return True

    def eap_power(self, action):
        feed = None
        power = {}

        if (action == 'stop'):
            power = self.power_stop
        elif (action == 'reload'):
            power = self.power_reload
        else:
            self.web_session.logger.error("Power action not recognized: {}".format(action))
            return False

        # At present, can only get EAP state via Hawkular API.
        # Find an EAP in 'start' state, which will then have power 'action' applied

        eap_hawk = self.find_eap_in_state(power.get('start_state'))
        assert eap_hawk, "No EAP Servers found to be in state {}".format(power.get('start_state'))
        feed = eap_hawk.get('Feed')
        self.web_session.logger.info("About to {} EAP server {} Feed {}".format(action, eap_hawk.get('Product'), feed))

        NavigationTree(self.web_session).navigate_to_middleware_servers_view()

        self.ui_utils.click_on_row_containing_text(eap_hawk.get('Feed'))
        self.ui_utils.waitForTextOnPage("Properties", 15)

        self.web_driver.find_element_by_xpath("//button[@title='Power']").click()
        self.web_driver.find_element_by_xpath("//a[contains(.,'{}')]".format(power.get('action'))).click()
        self.web_driver.switch_to_alert().accept()
        assert self.ui_utils.waitForTextOnPage(power.get('wait_for'), 15)

        # Validate backend - Hawkular
        assert self.wait_for_eap_state(feed, power.get('end_state'), 15)

        # TO-DO: Bring EAP back to start-state

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
            if row.get("Product Name") != 'Hawkular' and row.get("details").get("Server State") == state:
                return row

        return None