from common.ui_utils import ui_utils
from parsing.table import table
from navigation.navigation import NavigationTree

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

        self.__find_and_click_on_provider__(self.web_session.PROVIDER)

        # 1) Get table as list
        # 2) Convert to Dictionary
        # 3) Return Dictionary

        table = []
        table = self.__get_table_list__()

        ## Convert to Dictionary
        pairs = {}
        for pair in table:
            pairs[pair[0]] = pair[1]

        return pairs

    def __getTable_list__(self):
        return self.web_driver.find_elements_by_xpath('.//tr')


    def __get_table_list__(self):
        table = []
        for tr in self.__getTable_list__():
            tds = tr.find_elements_by_tag_name('td')
            if tds:
                table.append([td.text for td in tds])  # Create the row/list

        return table

    def __find_and_click_on_provider__(self, product_name):

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