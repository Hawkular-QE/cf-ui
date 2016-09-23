from common.ui_utils import ui_utils
from hawkular.hawkular_api import hawkular_api
from common.db import db

class messagings():
    web_session = None
    ui_utils = None
    hawkular_api = None
    db = None

    def __init__(self, web_session):
        self.web_session = web_session
        self.ui_utils = ui_utils(self.web_session)
        self.hawkular_api = hawkular_api(self.web_session)
        self.db = db(self.web_session)

    def validate_messagings_view(self):
        self.__navigate_to_messagings_view()

        ui_messagings = self.ui_utils.get_list_table()
        assert ui_messagings, "No UI Messagings."
        hawk_messagings = self.hawkular_api.get_hawkular_messagings()
        assert hawk_messagings, "No Hawkular-API Messagings."
        db_messagings = self.db.get_messagings()
        assert db_messagings , "No DB Messagings."

        assert len(ui_messagings) == len(hawk_messagings) == len(db_messagings), "Messagings size mismatch."

        return True

    def validate_messageing_details(self):
        self.__navigate_to_messagings_view()

        ui_messagings = self.ui_utils.get_list_table()
        assert ui_messagings, "No UI Messagings."
        hawk_messagings = self.hawkular_api.get_hawkular_messagings()
        assert hawk_messagings, "No Hawkular-API Messagings."
        db_messagings = self.db.get_messagings()
        assert db_messagings , "No DB Messagings."

        for mess in self.ui_utils.get_random_list(ui_messagings, 3):
            self.__navigate_to_messagings_view()

            messageing_name = mess.get('Messaging Name')
            self.web_session.logger.info("Validate Messaging {}.".format(messageing_name))

            self.ui_utils.click_on_row_containing_text(messageing_name)
            assert self.ui_utils.waitForTextOnPage("Summary", 15)

            ui_mess = self.ui_utils.get_generic_table_as_dict()

            hawk_mess = self.ui_utils.find_row_in_list(hawk_messagings, 'name', messageing_name)
            assert hawk_mess, "No Hawkular-API Messaging found for {}.".format(messageing_name)
            db_mess = self.ui_utils.find_row_in_list(db_messagings, 'name', messageing_name)
            assert db_mess, "No DB Messaging found for {}.".format(messageing_name)

            assert ui_mess.get('Name') == hawk_mess.get('name') == db_mess.get('name'), "Failed name check: UI:{}  Hawkular-API:{}   DB:{}"\
                .format(ui_mess.get('Name'), hawk_mess.get('name'), db_mess.get('name'))

            assert ui_mess.get('Messaging type') == db_mess.get('messaging_type'), "Bad Messaging-Type"

        return True

    def __navigate_to_messagings_view(self):
        self.web_session.web_driver.get("{}//middleware_messaging/show_list".format(self.web_session.MIQ_URL))
        assert self.ui_utils.waitForTextOnPage("Middleware Messagings", 15)