from common.ui_utils import ui_utils
from parsing.table import table
from navigation.navigation import NavigationTree
from hawkular.hawkular_api import hawkular_api
from common.db import db

class datasources():
    web_session = None

    def __init__(self, web_session):
        self.web_session = web_session
        self.web_driver = web_session.web_driver
        self.ui_utils = ui_utils(self.web_session)
        self.hawkular_api = hawkular_api(self.web_session)


    def validate_datasource_list(self):
        nav= NavigationTree(self.web_session)
        nav.navigate_to_middleware_datasources_view()

        haw= hawkular_api(self.web_session)
        tab = table(self.web_session)
        dataDb = db(self.web_session)

        datasource_api = self.hawkular_api.get_hawkular_datasources()
        datasource_ui = table(self.web_session).get_middleware_datasources_table()
        datasource_db = db(self.web_session).get_datasources()
        assert len(datasource_db) == len(datasource_ui) == len(datasource_api), "Datasource length match"

        for data_ui in datasource_ui:
            datasource_name = data_ui.get('Datasource Name')
            data_api = self.ui_utils.find_row_in_list(datasource_api, 'Name', datasource_name)

            assert data_api, "Datasource Name {} not found".format(datasource_name)
            assert (datasource_name == data_api.get("Name")), \
                "Datasource Name mismatch ui:{}, hawk:{}".format(datasource_name, data_api.get("Name"))
            self.web_session.logger.info(
                "UI Datasource name is: {}, and Hawkular datasource is: {} ".format(datasource_name,
                                                                                    data_api.get("Name")))

        return True

    def validate_datasource_detail(self):
        datasource_ui = table(self.web_session).get_middleware_datasources_table()
        datasource_api = self.hawkular_api.get_hawkular_datasources()

        for dat in self.ui_utils.get_random_list(datasource_ui, 3):
            datasource_name = dat.get('Datasource Name')
            self.web_session.logger.info("Validate Datasource {}.".format(datasource_name))

            self.web_session.web_driver.get("{}/middleware_datasource/show_list".format(self.web_session.MIQ_URL))
            assert self.ui_utils.waitForTextOnPage("Middleware Datasources", 15)

            self.ui_utils.click_on_row_containing_text(datasource_name)
            self.ui_utils.waitForTextOnPage("Nativeid", 15)
            dat_details_ui = self.ui_utils.get_generic_table_as_dict()
            self.web_session.logger.info("dat_details_ui: {}".format(dat_details_ui))
            dat_details_api = self.ui_utils.find_row_in_list(datasource_api, 'Name', datasource_name)
            self.web_session.logger.info("dat_details_api: {}".format(dat_details_api))

            assert dat_details_ui.get('Name') == dat_details_api.get('Name')
            assert dat_details_ui.get('Nativeid') == dat_details_api.get('Nativeid')

        return True

    def count_datasources(self):
        return len(self.web_session.web_driver.find_elements_by_xpath("//tbody/tr"))
