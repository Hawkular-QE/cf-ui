from common.ui_utils import ui_utils
from navigation.navigation import NavigationTree
from parsing.table import table

class topology():
    web_session = None
    web_driver = None
    ui_utils = None

    entities = {'servers':'Middleware Servers','deployments':'Middleware Deployments'}

    def __init__(self, web_session):
        self.web_session = web_session
        self.web_driver = web_session.web_driver
        self.ui_utils = ui_utils(self.web_session)

    def validate_display_names_checkbox(self, select = True):

        # By default, the MW Provider is always displayed in the Topology
        # Thus, use MW Prover Name for checkbock validation

        provider_name = self.web_session.HAWKULAR_PROVIDER_NAME

        self.web_driver.get("{}/middleware_topology/show".format(self.web_session.MIQ_URL))

        self.__display_names__()

        if not self.__is_name_displayed__(provider_name):
            self.web_session.logger.failure("Display Names - {} Not Displayed.".format(provider_name))
            return False

        self.__display_names__(select = False)

        if self.__is_name_displayed__(provider_name):
            self.web_session.logger.error("Display Names - {} Unexpectedly Displayed.".format(provider_name))
            return False

        return True

    def validate_default_topology_view(self):
        provider_name = self.web_session.HAWKULAR_PROVIDER_NAME

        self.web_session.logger.info("Validate that default Topology View displays {}".format(provider_name))

        self.web_driver.get("{}/middleware_topology/show".format(self.web_session.MIQ_URL))

        self.__display_names__(select = True)

        ## To-Do: Deselect "Middleware Servers" and "Middleware Deployments"

        return self.ui_utils.waitForTextOnPage(provider_name, 5)


    def validate_middleware_servers_entities(self):

        # Validate that each Server Name is displayed in Topology:
        # 1) get Servers list (from Servers view)
        # 2) Enable Display Names
        # 3) Enable Middleware Servers entities (by validating whether 1st Server Name in Servers-List is displayed)
        # 4) Validate that each Server in Servers-List is displayed

        self.web_session.logger.info("Validate that Topology View expcted Servers")

        servers_list = table(self.web_session).get_middleware_servers_table()

        self.web_driver.get("{}/middleware_topology/show".format(self.web_session.MIQ_URL))

        self.__display_names__(select=True)

        # Select "Middleware Servers"
        self.__select_entities_view__(self.entities.get('servers'), servers_list[0].get('Server Name'))

        for server in servers_list:
            if not self.__is_name_displayed__(server.get('Server Name')):
                self.web_session.logger.failure("Display Names - {} Not Displayed.".format(server.get("Server Name")))
                return False

        return True

    def validate_middleware_deployments_entities(self):
        self.web_session.logger.info("Validate that Topology View expcted Deployments")

        # Validate that each Deployment is displayed in Topology:
        # 1) get Deployment list (from Deployments view)
        # 2) Enable Display Names
        # 3) Enable Middleware Deployment entities (by validating whether 1st Deployment Name in Deployment-List is displayed)
        # 4) Validate that each Deployment in Deployments-List is displayed

        deployments_list = table(self.web_session).get_middleware_deployments_table()

        self.web_driver.get("{}/middleware_topology/show".format(self.web_session.MIQ_URL))

        self.__display_names__(select=True)

        # Select "Middleware Deployments"
        self.__select_entities_view__(self.entities.get('deployments'), deployments_list[0].get('Deployment Name'))

        for deployment in deployments_list:
            if not self.__is_name_displayed__(deployment.get('Deployment Name')):
                self.web_session.logger.failure("Display Names - {} Not Displayed.".format(deployment.get("Deployment Name")))
                return False

        return True


    def __display_names__(self, select = True):
        el = self.web_session.web_driver.find_element_by_xpath('//*[@id="box"]')

        if select and not el.is_selected():
            el.click()

        elif not select and  el.is_selected():
            el.click()

        self.ui_utils.sleep(1)

    def __select_entities_view__(self, entities_to_view, name):

        # Currently, not able to determine if Entity button is already selected:
        # 1) If "name" is already visible - Entity button already selected
        # 2) If "name" is not visible - Click entity button
        # 3) If "name" still not visible - assert

        if self.__is_name_displayed__(name):
            return

        # Select Entities view (aka: buttons "Middleware Servers" and "Middleware Deployments"):
        #  1) Get elements by Name (list of elements)
        #  2) 2nd element contains needed entities element

        el = self.ui_utils.get_elements_containing_text(entities_to_view)
        el[1].click()

        if self.__is_name_displayed__(name):
            return

        assert False, "Entity button {} failed to display entity {}.".format(entities_to_view, name)

    def __refresh__(self):
        self.web_driver.find_element_by_class_name('btn-default').click()


    def __is_name_displayed__(self, name):

        # Check if a a Name is displayed:
        #  1) Get elements by Name (list of elements)
        #  2) 2nd element can be checked if "name" is Displayed or not
        el = self.ui_utils.get_elements_containing_text(name)
        return el[1].is_displayed()
