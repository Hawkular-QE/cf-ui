from common.ui_utils import ui_utils
from common.view import view
from views.servers import servers
from selenium.webdriver.common.by import By
from common.navigate import navigate
import pytest

class monitoring():
    web_session = None

    def __init__(self, web_session):
        self.web_session = web_session
        self.web_driver = web_session.web_driver
        self.ui_utils = ui_utils(self.web_session)

    def validate_provider_monitoring_timelines(self):
        navigate(self.web_session).get("{}/ems_middleware/show_list".format(self.web_session.MIQ_URL))
        view(self.web_session).list_View()
        assert self.ui_utils.waitForTextOnPage(self.web_session.HAWKULAR_PROVIDER_NAME, 10)
        self.ui_utils.click_on_row_containing_text(self.web_session.HAWKULAR_PROVIDER_NAME)
        assert self.ui_utils.waitForTextOnPage("Summary", 10)

        self.web_driver.find_element_by_xpath("//*[@title='Monitoring']").click()
        self.ui_utils.waitForElementOnPage(By.ID, 'ems_middlewarer_monitoring_choice__ems_middleware_timeline', 5)
        self.web_driver.find_element_by_id('ems_middlewarer_monitoring_choice__ems_middleware_timeline').click()
        assert self.ui_utils.waitForTextOnPage('Timeline View', 30)

        # Validate that graphs are present - TBD

        return True

    def validate_eap_servers_monitoring_utilization(self):
        navigate(self.web_session).get("{}/middleware_server/show_list".format(self.web_session.MIQ_URL))
        assert self.ui_utils.waitForTextOnPage(self.web_session.HAWKULAR_PROVIDER_NAME, 10)
        servers(self.web_session).navigate_to_non_container_eap()

        self.web_driver.find_element_by_xpath("//*[@title='Monitoring']").click()
        self.ui_utils.waitForElementOnPage(By.ID, 'middleware_server_monitoring_choice__middleware_server_perf', 5)
        self.web_driver.find_element_by_id('middleware_server_monitoring_choice__middleware_server_perf').click()
        assert self.ui_utils.waitForTextOnPage('Options', 30)

        # Validate that graphs are present
        assert self.ui_utils.isTextOnPage('JVM Heap Usage (Bytes)')
        assert self.ui_utils.isTextOnPage('Non Heap Usage (Bytes)')
        assert self.ui_utils.isTextOnPage('GC Duration (ms)')
        assert self.ui_utils.isTextOnPage('Web Sessions')
        assert self.ui_utils.isTextOnPage('Active')
        assert self.ui_utils.isTextOnPage('Expired')
        assert self.ui_utils.isTextOnPage('Rejected')

        assert self.ui_utils.isTextOnPage('Transactions')
        assert self.ui_utils.isTextOnPage('Committed')
        assert self.ui_utils.isTextOnPage('Timed-out')
        assert self.ui_utils.isTextOnPage('Heuristic')
        assert self.ui_utils.isTextOnPage('Aborted')
        assert self.ui_utils.isTextOnPage('Application Failure')
        assert self.ui_utils.isTextOnPage('Resource Failure')

        return True

    def validate_messagings_monitoring_utilization_jms_queues(self):

        servers(self.web_session).navigate_to_non_container_eap()
        if self.ui_utils.get_generic_table_as_dict().get('Middleware Messagings') =='0':
            pytest.skip("Skip test - EAP has \"0\" Middleware Messagings")

        self.web_session.web_driver.find_element_by_xpath("//td[contains(.,'Middleware Messagings')]").click()
        assert self.ui_utils.waitForTextOnPage('JMS Queue', 30)


        self.ui_utils.click_on_row_containing_text('JMS Queue')
        assert self.ui_utils.waitForTextOnPage("Summary", 30)

        self.web_driver.find_element_by_xpath("//*[@title='Monitoring']").click()
        self.ui_utils.waitForElementOnPage(By.ID, 'middleware_messaging_monitoring_choice__middleware_messaging_perf', 5)
        self.web_driver.find_element_by_id('middleware_messaging_monitoring_choice__middleware_messaging_perf').click()
        assert self.ui_utils.waitForTextOnPage('Options', 30)

        # Validate that graphs are present
        assert self.ui_utils.isTextOnPage('Messages')

        assert self.ui_utils.isTextOnPage('Consumers')

        return True

    def validate_messagings_monitoring_utilization_jms_topics(self):

        servers(self.web_session).navigate_to_non_container_eap()
        if self.ui_utils.get_generic_table_as_dict().get('Middleware Messagings') == '0':
            pytest.skip("Skip test - EAP has \"0\" Middleware Messagings")

        self.web_session.web_driver.find_element_by_xpath("//td[contains(.,'Middleware Messagings')]").click()
        assert self.ui_utils.waitForTextOnPage("Messaging Type", 10)
        self.ui_utils.click_on_row_containing_text('JMS Topic')
        assert self.ui_utils.waitForTextOnPage("Summary", 10)

        self.web_driver.find_element_by_xpath("//*[@title='Monitoring']").click()
        self.ui_utils.waitForElementOnPage(By.ID, 'middleware_messaging_monitoring_choice__middleware_messaging_perf', 5)
        self.web_driver.find_element_by_id('middleware_messaging_monitoring_choice__middleware_messaging_perf').click()

        assert self.ui_utils.waitForTextOnPage('Options', 30)

        # Validate that graphs are present
        assert self.ui_utils.isTextOnPage('Messages')

        assert self.ui_utils.isTextOnPage('Subscribers')

        return True

    def validate_datasources_monitoring_utilization(self):

        servers(self.web_session).navigate_to_non_container_eap()
        self.web_session.web_driver.find_element_by_xpath("//td[contains(.,'Middleware Datasources')]").click()
        assert self.ui_utils.waitForTextOnPage('ExampleDS', 15)


        self.web_driver.find_element_by_xpath("//td[contains(.,'ExampleDS')]").click()
        self.ui_utils.waitForTextOnPage("Nativeid", 15)

        self.web_driver.find_element_by_xpath("//*[@title='Monitoring']").click()
        self.ui_utils.waitForElementOnPage(By.ID, 'middleware_datasource_monitoring_choice__middleware_datasource_perf', 5)
        self.web_driver.find_element_by_id('middleware_datasource_monitoring_choice__middleware_datasource_perf').click()
        assert self.ui_utils.waitForTextOnPage('Options', 30)

        # Validate that graphs are present
        assert self.ui_utils.isTextOnPage('Availability')
        assert self.ui_utils.isTextOnPage('Available')
        assert self.ui_utils.isTextOnPage('In Use')
        assert self.ui_utils.isTextOnPage('Time-out')

        assert self.ui_utils.isTextOnPage('Responsiveness')
        assert self.ui_utils.isTextOnPage('Get Time')
        assert self.ui_utils.isTextOnPage('Creation Time')
        assert self.ui_utils.isTextOnPage('Wait Time')

        return True

