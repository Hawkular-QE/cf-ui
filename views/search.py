from common.ui_utils import ui_utils
from common.view import view
from hawkular.hawkular_api import hawkular_api
from views.servers import servers
from views.providers import providers
from selenium.webdriver.common.by import By

class search():
    web_session = None
    web_driver = None
    ui_utils = None
    hawkular_api = None
    db = None

    server_name = "Local"
    deploymentname = "hawkular-alerts.war"
    datasourcename = "ExampleDS"
    jmstopicname = "HawkularAlertData"
    domain_name = "Domain"

    def __init__(self, web_session):
        self.web_session = web_session
        self.web_driver = web_session.web_driver
        self.ui_utils = ui_utils(self.web_session)
        self.hawkular_api = hawkular_api(self.web_session)
        self.provider_name = self.web_session.HAWKULAR_PROVIDER_NAME
        self.hostname = self.web_session.HAWKULAR_HOSTNAME

    def simple_search(self):

        self.simple_search_provider()
        self.simple_search_domain()
        self.simple_search_server()
        self.simple_search_deployments()
        self.simple_search_datasources()
        self.simple_search_messagings()

        return True

    def verify_search_exist(self):

        if (self.web_driver.find_element_by_id("search_text") and self.web_driver.find_element_by_xpath("//button[@id='adv_search']")):
            self.web_session.logger.info("The simple and advanced search exist.")
        else:
            self.web_session.logger.info("The simple and advanced search does not exist.")

    def simple_search_provider(self):

        self.web_session.web_driver.get("{}//ems_middleware/show_list".format(self.web_session.MIQ_URL))
        assert self.ui_utils.waitForTextOnPage("Middleware Providers", 15)
        view(self.web_session).list_View()
        self.verify_search_exist()
        self.web_driver.find_element_by_id("search_text").send_keys(self.provider_name)
        self.web_driver.find_element_by_xpath("//button[@class='btn btn-default']").click()
        assert self.ui_utils.waitForTextOnPage(self.hostname, 15)

    def simple_search_domain(self):

        self.web_session.web_driver.get("{}//middleware_domain/show_list".format(self.web_session.MIQ_URL))
        assert self.ui_utils.waitForTextOnPage("Middleware Domains", 15)
        self.verify_search_exist()
        self.web_driver.find_element_by_id("search_text").send_keys(self.domain_name)
        self.web_driver.find_element_by_xpath("//button[@class='btn btn-default']").click()
        assert self.ui_utils.waitForTextOnPage(self.provider_name, 15)

    def simple_search_server(self):

        self.web_session.web_driver.get("{}//middleware_server/show_list".format(self.web_session.MIQ_URL))
        assert self.ui_utils.waitForTextOnPage("Middleware Servers", 15)
        self.verify_search_exist()

        self.web_driver.find_element_by_id("search_text").send_keys(self.server_name)
        self.web_driver.find_element_by_xpath("//button[@class='btn btn-default']").click()
        assert self.ui_utils.waitForTextOnPage(self.provider_name, 15)

    def simple_search_deployments(self):

        self.web_session.web_driver.get("{}//middleware_deployment/show_list".format(self.web_session.MIQ_URL))
        assert self.ui_utils.waitForTextOnPage("Middleware Deployments", 15)
        self.verify_search_exist()

        self.web_driver.find_element_by_id("search_text").send_keys(self.deploymentname)
        self.web_driver.find_element_by_xpath("//button[@class='btn btn-default']").click()
        assert self.ui_utils.waitForTextOnPage(self.server_name, 15)

    def simple_search_datasources(self):

        self.web_session.web_driver.get("{}//middleware_datasource/show_list".format(self.web_session.MIQ_URL))
        assert self.ui_utils.waitForTextOnPage("Middleware Datasources", 15)
        self.verify_search_exist()

        self.web_driver.find_element_by_id("search_text").send_keys(self.datasourcename)
        self.web_driver.find_element_by_xpath("//button[@class='btn btn-default']").click()
        assert self.ui_utils.waitForTextOnPage(self.server_name, 15)

    def simple_search_messagings(self):

        self.web_session.web_driver.get("{}//middleware_messaging/show_list".format(self.web_session.MIQ_URL))
        assert self.ui_utils.waitForTextOnPage("Middleware Messagings", 15)
        self.verify_search_exist()

        self.web_driver.find_element_by_id("search_text").send_keys(self.jmstopicname)
        self.web_driver.find_element_by_xpath("//button[@class='btn btn-default']").click()
        assert self.ui_utils.waitForTextOnPage(self.server_name, 15)
