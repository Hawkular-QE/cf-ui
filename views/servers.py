from common.ui_utils import ui_utils

class servers():
    web_session = None
    ui_utils = None

    def __init__(self, web_session):
        self.web_session = web_session
        self.ui_utils = ui_utils(self.web_session)

    def validate_servers_list(self):
        ## Refactor when formal navigations are in place
        self.web_session.web_driver.get("{}/middleware_server/show_list".format(self.web_session.MIQ_URL))

        ## Refactore when table directory is in place
        return self.ui_utils.isTextOnPage(self.web_session.HAWKULAR_PROVIDER_NAME)
