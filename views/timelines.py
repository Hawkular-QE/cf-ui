from common.ui_utils import ui_utils
from hawkular.hawkular_api import hawkular_api
from views.servers import servers
from selenium.webdriver.common.by import By
from common.navigate import navigate

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
        navigate(self.web_session).get("{}/middleware_deployment/show_list".format(self.web_session.MIQ_URL))
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

        navigate(self.web_session).get("{}//middleware_server/show_list".format(self.web_session.MIQ_URL))

        # Find non-container EAP on which to deploy
        eap = servers(self.web_session).find_eap_in_state("Running", check_if_resolvable_hostname=True)
        assert eap, "No EAP found in desired state."

        self.ui_utils.click_on_row_containing_text(eap.get('Feed'))
        self.ui_utils.waitForTextOnPage('Version', 15)

        servers(self.web_session).add_server_deployment(self.TextFile, expected_failure=True)

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
        self.ui_utils.waitForElementOnPage(By.XPATH, "//a[contains(.,'{}')]".format(group), 5)
        self.web_driver.find_element_by_xpath("//a[contains(.,'{}')]".format(group)).click()
        ui_utils(self.web_session).sleep(5)
        return True

    def change_level(self):

        # Check the 'Show Detailed Events' checkbox

        self.web_driver.find_element_by_xpath("//input[@name='showDetailedEvents']").click()

    def select_timepivot(self):

        # Select the 'starting' week

        self.web_driver.find_element_by_xpath("//button[@data-id='tl_timepivot']").click()
        self.ui_utils.waitForElementOnPage(By.XPATH, "//span[contains(.,'starting')]", 5)
        self.web_driver.find_element_by_xpath("//span[contains(.,'starting')]").click()

    def apply(self):

        self.web_driver.find_element_by_xpath("//div[@ng-click='applyButtonClicked()']").click()
        ui_utils(self.web_session).sleep(60)

    def navigate_to_timeline(self):

        navigate(self.web_session).get("{}//ems_middleware/show_list?type=list".format(self.web_session.MIQ_URL))
        ui_utils(self.web_session).waitForTextOnPage(self.web_session.HAWKULAR_PROVIDER_NAME, 10)
        ui_utils(self.web_session).click_on_row_containing_text(self.web_session.HAWKULAR_PROVIDER_NAME)
        ui_utils(self.web_session).waitForTextOnPage('Relationships', 10)
        self.web_driver.find_element_by_xpath("//button[@title='Monitoring']").click()
        el = self.web_driver.find_element_by_xpath("//a[contains(@id,'timeline')]")
        self.ui_utils.wait_until_element_displayed(el, 5)
        el.click()
        ui_utils(self.web_session).sleep(60)
        self.ui_utils.waitForTextOnPage('Options', 120)

    def verify_event(self, event_type):
        try:
            el = self.web_driver.find_element_by_xpath(
                    "//*[@id = 'chart_placeholder']//*[name() = 'svg']//*[name() = 'text']")
        except:
            assert False, 'No Timeline events found'

        # Verify event where type for successful event is 'ok' and for unsuccessful event is 'error'
        self.ui_utils.wait_until_element_displayed(el, 60)
        el.click()
        assert ui_utils(self.web_session).waitForTextOnPage("hawkular_deployment.{}".format(event_type), 120)
        return True