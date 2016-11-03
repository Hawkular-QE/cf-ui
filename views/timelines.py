from common.ui_utils import ui_utils
from hawkular.hawkular_api import hawkular_api
from views.servers import servers

class timelines():
    web_session = None
    web_driver = None
    ui_utils = None
    hawkular_api = None
    db = None

    APPLICATION_WAR = "cfui_test_war.war"
    TextFile = "TestFile.txt"

    def __init__(self, web_session):
        self.web_session = web_session
        self.web_driver = web_session.web_driver
        self.ui_utils = ui_utils(self.web_session)
        self.hawkular_api = hawkular_api(self.web_session)

    def test_event_for_successful_deployment(self):
        self.web_session.web_driver.get("{}/middleware_deployment/show_list".format(self.web_session.MIQ_URL))
        assert self.ui_utils.waitForTextOnPage("Middleware Deployments", 15)

        if self.ui_utils.get_elements_containing_text(self.APPLICATION_WAR):
            self.ui_utils.click_on_row_containing_text(self.APPLICATION_WAR)
        else:
            servers(self.web_session).deploy_application_archive()

        self.navigate_to_timeline()
        self.select_timepivot()
        self.select_event_group('Application')
        self.change_level()
        self.apply()
        self.verify_event('ok')

        return True

    def test_event_for_unsuccessful_deployment(self):

        # Existing issue: https://bugzilla.redhat.com/show_bug.cgi?id=1388040

        self.web_session.web_driver.get("{}//middleware_server/show_list".format(self.web_session.MIQ_URL))

        # Find EAP on which to deploy
        eap = servers(self.web_session).find_non_container_eap_in_state("running")
        assert eap, "No EAP found in desired state."

        self.ui_utils.click_on_row_containing_text(eap.get('Feed'))
        self.ui_utils.waitForTextOnPage('Version', 15)

        servers(self.web_session).add_server_deployment(self.TextFile)

        self.navigate_to_timeline()
        self.select_timepivot()
        self.select_event_group('Application')
        self.apply()
        self.verify_event('error')

        return True

    def select_event_group(self, group):

        # Select group from timeline ex: Application

        assert self.ui_utils.waitForTextOnPage("Options", 15)
        self.web_driver.find_element_by_xpath("//button[contains(@data-id,'tl_category_management')]").click()
        self.web_driver.find_element_by_xpath("//a[contains(.,'{}')]".format(group)).click()
        ui_utils(self.web_session).sleep(5)
        return True

    def change_level(self):

        # Check the 'Show Detailed Events' checkbox

        self.web_driver.find_element_by_xpath("//input[@name='showDetailedEvents']").click()

    def select_timepivot(self):

        # Select the 'starting' week

        self.web_driver.find_element_by_xpath("//button[@data-id='tl_timepivot']").click()
        self.web_driver.find_element_by_xpath("//span[contains(.,'starting')]").click()

    def apply(self):

        self.web_driver.find_element_by_xpath("//div[@ng-click='applyButtonClicked()']").click()
        ui_utils(self.web_session).sleep(10)

    def navigate_to_timeline(self):

        self.web_session.web_driver.get("{}//ems_middleware/show_list?type=list".format(self.web_session.MIQ_URL))
        ui_utils(self.web_session).click_on_row_containing_text(self.web_session.HAWKULAR_PROVIDER_NAME)
        self.web_driver.find_element_by_xpath("//button[@title='Monitoring']").click()
        self.web_driver.find_element_by_xpath("//a[contains(@id,'timeline')]").click()
        ui_utils(self.web_session).sleep(5)

    def verify_event(self, event_type):

        # Verify event where type for successful event is 'ok' and for unsuccessful event is 'error'

        self.web_driver.find_element_by_xpath(
            "//*[@id = 'chart_placeholder']/div[1]/*[name() = 'svg']/*[name() = 'g'][4]/*[name() = 'g'][1]/* [name() = 'text']").click()
        assert ui_utils(self.web_session).waitForTextOnPage("hawkular_deployment.{}".format(event_type), 15)
        return True