from common.ui_utils import ui_utils
from navigation.navigation import NavigationTree

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

        # Be default, the MW Provider is always displayed in the Topology
        # Thus, use MW Prover Name for checkbock validation

        provider_name = self.web_session.HAWKULAR_PROVIDER_NAME

        self.web_driver.get("{}/middleware_topology/show".format(self.web_session.MIQ_URL))

        self.__display_names__()
        self.ui_utils.sleep(1)

        if not self.__is_provider_name_displayed__(provider_name):
            self.web_session.logger.failure("Display Names - {} Not Displayed.".format(provider_name))
            return False

        self.__display_names__(select = False)
        self.ui_utils.sleep(1)

        if self.__is_provider_name_displayed__(provider_name):
            self.web_session.logger.error("Display Names - {} Unexpectedly Displayed.".format(provider_name))
            return False

        return True

    def validate_default_topology_view(self):
        provider_name = self.web_session.HAWKULAR_PROVIDER_NAME

        self.web_session.logger.info("Validate that default Topology View displays {}".format(provider_name))

        ## Nav to Top view
        self.web_driver.get("{}/middleware_topology/show".format(self.web_session.MIQ_URL))

        self.__display_names__(select = True)

        ## To-Do: Deselect "Middleware Servers" and "Middleware Deployments"

        return self.ui_utils.waitForTextOnPage(provider_name, 5)


    def validate_middleware_servers_entities(self):
        self.web_session.logger.info("Validate that Topology View expcted Servers")

        # TO_DO - Get Servers List

        self.web_driver.get("{}/middleware_topology/show".format(self.web_session.MIQ_URL))

        self.__display_names__(select=True)

        ## Select "Middleware Servers" and Deselect "Middleware Deployments"
        self.__select_entities_view__(self.entities['servers'])

        ## Validate Server names are displayed


    def validate_middleware_deployments_entities(self):
        self.web_session.logger.info("Validate that Topology View expcted Deployments")

        ## Nav to Top view

        ## Click "Display Names" and "Refresh"

        ## Deselect "Middleware Servers" and select "Middleware Deployments"

        ## Validate Server names are displayed


    def __display_names__(self, select = True):
        el = self.web_session.web_driver.find_element_by_xpath('//*[@id="box"]')

        if select and not el.is_selected():
            el.click()

        elif not select and  el.is_selected():
            el.click()

    def __select_entities_view__(self, entities_to_view):

        # Select Entities view (aka: buttons "Middleware Servers" and "Middleware Deployments"):
        #  1) Get elements by Name (list of elements)
        #  2) 2nd element contains needed entities element

        el = self.ui_utils.get_elements_containing_text(entities_to_view)
        el[1].click()

    def __refresh__(self):
        self.web_driver.find_element_by_class_name('btn-default').click()


    def __is_provider_name_displayed__(self, name):

        # Check if a a Name is displayed:
        #  1) Get elements by Name (list of elements)
        #  2) 2nd element can be checked if "name" is Displayed or not

        el = self.ui_utils.get_elements_containing_text(name)
        return el[1].is_displayed()
