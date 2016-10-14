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

    def validate_eap_jms_queues(self):
        server_to_test = 'server-one'

        self.web_session.web_driver.get("{}/middleware_server/show_list".format(self.web_session.MIQ_URL))

        # Check that server to test is present
        if not self.ui_utils.isTextOnPage(server_to_test):
            self.web_session.logger.warning("Server not found: {}".format(server_to_test))
            return True

        # find 'Server Name' = 'server-one' ("should" have messagings)
        self.ui_utils.click_on_row_containing_text('server-one')
        self.ui_utils.waitForTextOnPage('Middleware Messagings', 10)

        # Validate that EAP Server has Middleware Messagings
        eap_server_detail = self.ui_utils.get_generic_table_as_dict()
        assert eap_server_detail.get('Middleware Messagings') > 0, 'No Messagings found for: EAP Server: {}  Feed: {}' \
                                      .format(eap_server_detail.get('Name'), eap_server_detail.get('Feed'))

        # Drill into EAP Server 'Middleware Messagings'
        self.ui_utils.get_elements_containing_text('Middleware Messagings')[0].click()
        self.ui_utils.waitForTextOnPage('Middleware Messagings', 10)

        # Get table and validate that table length == EAP Server Detail/Summary 'Middleware Messagings' count
        eap_jms_queues = self.ui_utils.get_list_table()
        assert len(eap_jms_queues) == int(eap_server_detail.get('Middleware Messagings'))
        hawk_jms_queues = self.hawkular_api.get_hawkular_messagings()

        for jms_queue in self.ui_utils.get_random_list(eap_jms_queues, 2):
            self.ui_utils.click_on_row_containing_text(jms_queue.get('Messaging Name'))
            self.ui_utils.waitForTextOnPage('Messaging type', 10)

            ui_queue_detail = self.ui_utils.get_generic_table_as_dict()
            hawk_queue_detail = self.ui_utils.find_row_in_list(hawk_jms_queues, 'name', jms_queue.get('Messaging Name'))
            assert hawk_queue_detail

            assert ui_queue_detail.get('Name') in hawk_queue_detail.get('name')

            self.web_session.web_driver.back()
            self.ui_utils.waitForTextOnPage('Middleware Messagings', 10)

        return True

    def __navigate_to_messagings_view(self):
        self.web_session.web_driver.get("{}//middleware_messaging/show_list".format(self.web_session.MIQ_URL))
        assert self.ui_utils.waitForTextOnPage("Middleware Messagings", 15)