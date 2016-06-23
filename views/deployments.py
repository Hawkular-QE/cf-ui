from common.ui_utils import ui_utils
from parsing.table import table
from navigation.navigation import NavigationTree
from hawkular.hawkular_api import hawkular_api

class deployments():
    web_session = None
    ui_utils = None
    hawkular_api = None

    def __init__(self, web_session):
        self.web_session = web_session
        self.ui_utils = ui_utils(self.web_session)
        self.hawkular_api = hawkular_api(self.web_session)

    def validate_deployment_details(self):
        deployments_ui = table(self.web_session).get_middleware_deployments_table()
        deployments_hawk = self.hawkular_api.get_hawkular_deployments()

        # Test only a random sameple of the entire Deployments list
        for dep in self.ui_utils.get_random_list(deployments_ui, 3):
            deployment_name = dep.get('Deployment Name')

            self.web_session.web_driver.get("{}/middleware_deployment/show_list".format(self.web_session.MIQ_URL))

            self.ui_utils.click_on_row_containing_text(deployment_name)
            self.ui_utils.waitForTextOnPage("Properties", 15)
            dep_details_ui = self.ui_utils.get_generic_table_as_dict()

            dep_details_hawk = self.hawkular_api.find_row_in_list(deployments_hawk, 'Name', deployment_name)
            assert dep_details_hawk, "Hawkular Deployment {} not found.".format(deployment_name)

            assert dep_details_ui.get('Middleware Provider') == self.web_session.HAWKULAR_PROVIDER_NAME
            assert dep_details_ui.get('Name') == dep_details_hawk.get('Name')
            assert dep_details_ui.get('Nativeid') == dep_details_hawk.get('Nativeid')

        return True
