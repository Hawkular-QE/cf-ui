from common.ui_utils import ui_utils
from hawkular.hawkular_api import hawkular_api


class topology_crosslink():
    web_session = None
    MIQ_BASE_VERSION = "master"
    ui_utils = None

    def __init__(self, web_session):
        self.web_session = web_session
        self.web_driver = web_session.web_driver
        self.hawkular_api = hawkular_api(self.web_session)

    def crosslink_topology(self):
        self.web_session.web_driver.get("{}/middleware_topology/show".format(self.web_session.MIQ_URL))
        ui_utils(self.web_session).sleep(10)
        assert ui_utils(self.web_session).waitForTextOnPage("Servers", 40)
        return True
