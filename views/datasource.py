from common.ui_utils import ui_utils
from parsing.table import table
from navigation.navigation import NavigationTree
from hawkular.hawkular_api import hawkular_api
from common.db import db

class datasources():
    web_session = None

    def __init__(self, web_session):
        self.web_session = web_session
        self.ui_utils = ui_utils(self.web_session)


    def validate_datasource_list(self):
        nav= NavigationTree(self.web_session)
        nav.navigate_to_middleware_datasources_view()

        haw= hawkular_api(self.web_session)
        tab = table(self.web_session)
        dataDb = db(self.web_session)

        datasource_api = haw.get_hawkular_datasources()
        datasource_ui = tab.get_middleware_datasources_table()
        datasource_db = dataDb.get_datasources()
        assert len(datasource_api) == len(datasource_ui) == len(datasource_db), "Datasource lenght match"

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


