from common.ui_utils import ui_utils
from parsing.table import table
from navigation.navigation import NavigationTree
from hawkular.hawkular_api import hawkular_api
from views.servers import servers
from common.view import view
from selenium.webdriver.support.ui import WebDriverWait

class timelines():
    web_session = None
    web_driver = None
    ui_utils = None
    hawkular_api = None
    db = None

    def __init__(self, web_session):
        self.web_session = web_session
        self.web_driver = web_session.web_driver
        self.ui_utils = ui_utils(self.web_session)
        self.hawkular_api = hawkular_api(self.web_session)

    def test_event_for_successful_deployment(self):

        servers(self.web_session).deploy_application_archive()
        self.navigate_to_timeline()
        self.select_event_group('Application')
        self.change_level('Detail')
        self.verify_event('ok')

        return True

    def test_event_for_unsuccessful_deployment(self):

        """
        TO-DO

    1) Deploy a war - should fail ( maybe a text file )
    2) then navigate to Monitoring->Timelines
    3) Select Event Groups  - "Application"
    4) Select Level as "Summary"
    5) See whether the element is present
    6) test if pop up is present with summary having text 'Event Type: hawkular_deployment.error'

        """
        return True

    def select_event_group(self, group):

        # Select group from timeline ex: Application

        self.web_driver.find_element_by_xpath("//button[@data-dismiss='alert']").click()
        ui_utils(self.web_session).sleep(5)

        self.web_driver.find_element_by_xpath("//button[contains(@data-id,'tl_fl_grp1')]").click()
        self.web_driver.find_element_by_xpath("//span[contains(.,'{}')]".format(group)).click()
        ui_utils(self.web_session).sleep(15)
        return True

    def change_level(self, level):

        # Select the level either 'Detail' or 'Summary'

        self.web_driver.find_element_by_xpath("//button[contains(@data-id,'tl_fl_typ')]").click()
        self.web_driver.find_element_by_xpath("//span[contains(.,'{}')]".format(level)).click()
        ui_utils(self.web_session).sleep(15)
        return True

    def navigate_to_timeline(self):

        self.web_session.web_driver.get("{}//ems_middleware/show_list?type=list".format(self.web_session.MIQ_URL))
        ui_utils(self.web_session).click_on_row_containing_text(self.web_session.HAWKULAR_PROVIDER_NAME)
        self.web_driver.find_element_by_xpath("//button[@title='Monitoring']").click()
        self.web_driver.find_element_by_xpath("//a[contains(@id,'timeline')]").click()
        ui_utils(self.web_session).sleep(15)

    def verify_event(self, type):

        # Verify event where type for successful event is 'ok' and for unsuccessful event is 'error'

        self.web_driver.find_element_by_xpath("//img[contains(@src,'/assets/timeline/vm_event')]").click()
        assert ui_utils(self.web_session).waitForTextOnPage("hawkular_deployment.{}".format(type), 15)
        return True