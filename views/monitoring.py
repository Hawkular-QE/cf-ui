from common.ui_utils import ui_utils
from common.view import view

class monitoring():
    web_session = None

    def __init__(self, web_session):
        self.web_session = web_session
        self.web_driver = web_session.web_driver
        self.ui_utils = ui_utils(self.web_session)

    def validate_provider_monitoring_timelines(self):
        self.web_session.web_driver.get("{}/ems_middleware/show_list".format(self.web_session.MIQ_URL))
        view(self.web_session).list_View()

        self.ui_utils.click_on_row_containing_text(self.web_session.HAWKULAR_PROVIDER_NAME)
        assert self.ui_utils.waitForTextOnPage("Summary", 10)

        self.web_driver.find_element_by_xpath("//*[@title='Monitoring']").click()
        self.ui_utils.sleep(1)
        self.web_driver.find_element_by_id('ems_middlewarer_monitoring_choice__ems_middleware_timeline').click()
        assert self.ui_utils.waitForTextOnPage('Timeline View', 30)

        # Validate that graphs are present - TBD

        return True

    def validate_servers_monitoring_utilization(self):
        self.web_session.web_driver.get("{}/middleware_server/show_list".format(self.web_session.MIQ_URL))

        self.ui_utils.click_on_row_containing_text('server-one')
        assert self.ui_utils.waitForTextOnPage("Summary", 10)

        self.web_driver.find_element_by_xpath("//*[@title='Monitoring']").click()
        self.ui_utils.sleep(1)
        self.web_driver.find_element_by_id('middleware_server_monitoring_choice__middleware_server_perf').click()
        assert self.ui_utils.waitForTextOnPage('Options', 30)

        # Validate that graphs are present
        assert self.ui_utils.isTextOnPage('JVM Heap Usage (Bytes)')
        assert self.ui_utils.isTextOnPage('Non Heap Usage (Bytes)')
        assert self.ui_utils.isTextOnPage('GC Duration (ms)')

        return True

    def validate_messagings_monitoring_utilization(self):
        self.web_session.web_driver.get("{}/middleware_messaging/show_list".format(self.web_session.MIQ_URL))

        self.ui_utils.click_on_row_containing_text('JMS Queue')
        assert self.ui_utils.waitForTextOnPage("Summary", 10)

        self.web_driver.find_element_by_xpath("//*[@title='Monitoring']").click()
        self.ui_utils.sleep(1)
        self.web_driver.find_element_by_id('middleware_messaging_monitoring_choice__middleware_messaging_perf').click()
        assert self.ui_utils.waitForTextOnPage('Options', 30)

        # Validate that graphs are present
        assert self.ui_utils.isTextOnPage('Messages')
        assert self.ui_utils.isTextOnPage('Consumers')

        return True

    def validate_datasources_monitoring_utilization(self):
        self.web_session.web_driver.get("{}/middleware_datasource/show_list".format(self.web_session.MIQ_URL))

        # 'server' will be an EAP Domain server
        self.ui_utils.click_on_row_containing_text('server-one')
        assert self.ui_utils.waitForTextOnPage("Summary", 10)

        self.web_driver.find_element_by_xpath("//*[@title='Monitoring']").click()
        self.ui_utils.sleep(1)
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

