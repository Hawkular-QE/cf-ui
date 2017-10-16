from common.ui_utils import ui_utils
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from hawkular.hawkular_api import hawkular_api
from common.view import view
from common.db import db
from common.openshift_utils import openshift_utils
import time
from common.timeout import timeout

class eap_crosslink():
    web_session = None
    MIQ_BASE_VERSION = "master"
    ui_utils = None

    def __init__(self, web_session):
        self.web_session = web_session
        self.web_driver = web_session.web_driver
        self.hawkular_api = hawkular_api(self.web_session)

    def crosslink_eap(self):
        self.web_session.web_driver.get("{}/middleware_server/show_list".format(self.web_session.MIQ_URL))
        ui_utils(self.web_session).sleep(10)
        assert ui_utils(self.web_session).waitForTextOnPage("Middleware Servers", 40)
        self.web_driver.find_element_by_xpath("//span[contains(.,'Local')]").click()
        assert ui_utils(self.web_session).waitForTextOnPage("Local (Summary)", 15)
        self.web_driver.find_element_by_xpath("//td[contains(.,'Underlying Container')]").click()
        assert ui_utils(self.web_session).waitForTextOnPage("hawkular-services (Summary)", 15)
        self.web_driver.find_element_by_xpath("//td[contains(.,'Containers Provider')]").click()
        assert ui_utils(self.web_session).waitForTextOnPage("Aggregated Node Utilization", 15)

        return True


