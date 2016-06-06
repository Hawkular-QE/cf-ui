from common.ui_utils import ui_utils
from navigation.navigation import NavigationTree

class servers():
    web_session = None
    web_driver = None
    ui_utils = None

    PROVIDER = "Hawkular"

    def __init__(self, web_session):
        self.web_session = web_session
        self.web_driver = web_session.web_driver
        self.ui_utils = ui_utils(self.web_session)

    def validate_servers_list(self):

        ## Vaidate that a Hawkular Provider is in the Servers list
        ## To-Do: Validate Servers list contains all expected Servers

        ## Refactor when formal navigations are in place
        #self.web_session.web_driver.get("{}/middleware_server/show_list".format(self.web_session.MIQ_URL))
        NavigationTree(self.web_driver).navigate_to_middleware_servers_view()

        # 1) Get table as list
        # 2) Create row of cell-elements
        # 3) Search each row to validate whether "Hawkular" provider is present

        table = []
        table = self.__get_table_list__()

        for row in table:
            # Search the each item in the row, for Product "Hawkular"
            for value in row:
                if value == self.web_session.PROVIDER:
                    self.web_session.logger.info("Found {} Provider".format(self.web_session.PROVIDER))
                    return True

        self.web_session.logger.info("No {} Provider found".format(self.web_session.PROVIDER))
        return False


    def validate_server_details(self):

        ## Validate the Hawkular Server details

        ## Refactor when formal navigations are in place
        #self.web_session.web_driver.get("{}/middleware_server/show_list?type=list".format(self.web_session.MIQ_URL))
        NavigationTree(self.web_driver).navigate_to_middleware_servers_view()

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