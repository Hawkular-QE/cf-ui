from common.ui_utils import ui_utils
from parsing.table import table
from navigation.navigation import NavigationTree
import random
import selenium

class servers():
    web_session = None
    web_driver = None
    ui_utils = None

    def __init__(self, web_session):
        self.web_session = web_session
        self.web_driver = web_session.web_driver
        self.ui_utils = ui_utils(self.web_session)

    def validate_servers_list(self):

        servers_list = table(self.web_session).get_middleware_servers_table()

        # Search each row to validate whether "Hawkular" provider is present
        # To-Do: Validate all servers, once there is a way to get the expected servers list

        for server in servers_list:
             if server.get('Product') == self.web_session.PROVIDER:
                self.web_session.logger.info("Found {} Provider".format(self.web_session.PROVIDER))
                return True

        self.web_session.logger.error("No {} Provider found".format(self.web_session.PROVIDER))

        return False


    def validate_server_details(self):

        ## Validate the Hawkular Server details

        NavigationTree(self.web_session).navigate_to_middleware_servers_view()

        self.__find_and_click_on_server__(self.web_session.PROVIDER)

        # 1) Get table as list
        # 2) Convert to Dictionary
        # 3) Return Dictionary

        pairs = self.ui_utils.get_generic_table_as_dict()

        return pairs


    def server_plocy_edit(self):
        origValue = -1
        newValue = None

        NavigationTree(self.web_session).navigate_to_middleware_servers_view()

        self.__find_and_click_on_server__(self.web_session.PROVIDER)

        server_details = self.ui_utils.get_generic_table_as_dict()
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
        tag = 'data-original-index=0'
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


    def __getTable_list__(self):
        return self.web_driver.find_elements_by_xpath('.//tr')


    def __get_table_list__(self):
        table = []
        for tr in self.__getTable_list__():
            tds = tr.find_elements_by_tag_name('td')
            if tds:
                table.append([td.text for td in tds])  # Create the row/list

        return table

    def __find_and_click_on_server__(self, product_name):

        ## Click on first row that is found to contain Product-name
        ## To-Do: how to handle multiple providers with same Product-name

        table = []
        for tr in self.__getTable_list__():
            tds = tr.find_elements_by_tag_name('td')
            if tds:
                table.append([td.text for td in tds])
                for row in table:
                    for value in row:
                        if value == product_name:
                            self.web_session.logger.info("Click on {} Provider".format(product_name))
                            tds[3].click()
                            return;

        assert False, "Did not find {} Provider".format(product_name)
