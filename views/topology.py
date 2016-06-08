from common.ui_utils import ui_utils
from navigation.navigation import NavigationTree

class topology():
    web_session = None
    web_driver = None

    def __init__(self, web_session):
        self.web_session = web_session
        self.web_driver = web_session.web_driver

    def validate_default_topology_view(self):
        provider_name = self.web_session.HAWKULAR_PROVIDER_NAME

        self.web_session.logger.info("Validate that default Topology View displays {}".format(provider_name))

        ## Nav to Top view
        self.web_driver.get("{}/middleware_topology/show".format(self.web_session.MIQ_URL))

        self.__display_names__(select = True)

        ## To-Do: Deselect "Middleware Servers" and "Middleware Deployments"

        return ui_utils(self.web_session).waitForTextOnPage(provider_name, 5)


    def validate_middleware_servers_view(self):
        self.web_session.logger.info("Validate that Topology View expcted Servers")

        ## Nav to Top view

        ## Click "Display Names" and "Refresh"

        ## Select "Middleware Servers" and Deselect "Middleware Deployments"

        ## Validate Server names are displayed


    def validate_middleware_deployments_view(self):
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