from common.ui_utils import ui_utils
from parsing.table import table
from navigation.navigation import NavigationTree
from hawkular.hawkular_api import hawkular_api
from common.db import db

class deployments():
    web_session = None
    ui_utils = None
    hawkular_api = None
    db = None

    def __init__(self, web_session):
        self.web_session = web_session
        self.ui_utils = ui_utils(self.web_session)
        self.hawkular_api = hawkular_api(self.web_session)
        self.db = db(self.web_session)

    def validate_deployment_details(self):
        deployments_ui = table(self.web_session).get_middleware_deployments_table()
        assert deployments_ui, "No UI Deployments found."

        deployments_hawk = self.hawkular_api.get_hawkular_deployments()
        assert deployments_hawk, "No Hawkular Deployments found."

        deployments_db = self.db.get_deployments()
        assert deployments_db, "No DB Deployments found."

        # Test only a random sample of the entire Deployments list
        for dep in self.ui_utils.get_random_list(deployments_ui, 3):
            deployment_name = dep.get('Deployment Name')
            self.web_session.logger.info("Validate Deployment {}.".format(deployment_name))

            self.web_session.web_driver.get("{}/middleware_deployment/show_list".format(self.web_session.MIQ_URL))
            assert self.ui_utils.waitForTextOnPage("Middleware Deployments", 15)

            self.ui_utils.click_on_row_containing_text(deployment_name)
            self.ui_utils.waitForTextOnPage("Nativeid", 15)

            dep_details_ui = self.ui_utils.get_generic_table_as_dict()
            assert dep_details_ui, "UI Deployment {} not found.".format(deployment_name)
            self.web_session.logger.info("dep_details_ui: {}".format(dep_details_ui))

            dep_details_hawk = self.ui_utils.find_row_in_list(deployments_hawk, 'Name', deployment_name)
            assert dep_details_hawk, "Hawkular Deployment {} not found.".format(deployment_name)
            self.web_session.logger.info("dep_details_hawk: {}".format(dep_details_hawk))

            dep_details_db = self.ui_utils.find_row_in_list(deployments_db, 'name', deployment_name)
            assert dep_details_db, "DB Deployment {} not found.".format(deployment_name)
            self.web_session.logger.info("dep_details_hawk: {}".format(dep_details_db))

            assert dep_details_ui.get('Middleware Provider') == self.web_session.HAWKULAR_PROVIDER_NAME

            assert deployment_name in dep_details_hawk.get('Name') and deployment_name == dep_details_db.get('name')

            ui_nativeid = dep_details_ui.get('Nativeid')
            assert ui_nativeid == dep_details_hawk.get('Nativeid') and ui_nativeid == dep_details_db.get('nativeid')

        return True

    def validate_deployments_list(self):
        deployments_ui = table(self.web_session).get_middleware_deployments_table()
        assert deployments_ui, "No UI Deployments found."
        deployments_hawk = self.hawkular_api.get_hawkular_deployments()
        assert deployments_hawk, "No Hawkular Deployments found."

        self.web_session.logger.debug(
            "UI Deployments: {}  HW Deployments: {}".format(deployments_ui.get('Middleware Deployments'), str(len(deployments_hawk))))
        #assert len(deployments_ui) == len(deployments_hawk), "Deployments lists size mismatch."

        for dep_ui in deployments_ui:
            deployment_name = dep_ui.get('Deployment Name')
            dep_hawk = self.ui_utils.find_row_in_list(deployments_hawk, 'Name', deployment_name)

            #assert dep_hawk, "Deployment Name {} not found".format(deployment_name)
            #assert (deployment_name in dep_hawk.get("Name")), \
            #    "Deployment Name mismatch ui:{}, hawk:{}".format(deployment_name, dep_hawk.get("Name"))
            self.web_session.logger.info(
                "UI Deployment name is: {}, and Hawkular deployment is: {} ".format(deployment_name,
                                                                                    dep_hawk.get("Name")))

        return True
