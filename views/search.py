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
    search_provider_name = "Test-SearchProvider"

    def __init__(self, web_session):
        self.web_session = web_session
        self.web_driver = web_session.web_driver
        self.ui_utils = ui_utils(self.web_session)
        self.hawkular_api = hawkular_api(self.web_session)
        self.provider_name = self.web_session.HAWKULAR_PROVIDER_NAME
        self.hostname = self.web_session.HAWKULAR_HOSTNAME

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
        return True

    def simple_search_domain(self):

        self.web_session.web_driver.get("{}//middleware_domain/show_list".format(self.web_session.MIQ_URL))
        assert self.ui_utils.waitForTextOnPage("Middleware Domains", 15)
        self.verify_search_exist()
        self.web_driver.find_element_by_id("search_text").send_keys(self.domain_name)
        self.web_driver.find_element_by_xpath("//button[@class='btn btn-default']").click()
        assert self.ui_utils.waitForTextOnPage(self.provider_name, 15)
        return True

    def simple_search_server(self):

        self.web_session.web_driver.get("{}//middleware_server/show_list".format(self.web_session.MIQ_URL))
        assert self.ui_utils.waitForTextOnPage("Middleware Servers", 15)
        self.verify_search_exist()

        self.web_driver.find_element_by_id("search_text").send_keys(self.server_name)
        self.web_driver.find_element_by_xpath("//button[@class='btn btn-default']").click()
        assert self.ui_utils.waitForTextOnPage(self.provider_name, 15)
        return True

    def simple_search_deployments(self):

        self.web_session.web_driver.get("{}//middleware_deployment/show_list".format(self.web_session.MIQ_URL))
        assert self.ui_utils.waitForTextOnPage("Middleware Deployments", 15)
        self.verify_search_exist()

        self.web_driver.find_element_by_id("search_text").send_keys(self.deploymentname)
        self.web_driver.find_element_by_xpath("//button[@class='btn btn-default']").click()
        assert self.ui_utils.waitForTextOnPage(self.server_name, 15)
        return True

    def simple_search_datasources(self):

        self.web_session.web_driver.get("{}//middleware_datasource/show_list".format(self.web_session.MIQ_URL))
        assert self.ui_utils.waitForTextOnPage("Middleware Datasources", 15)
        self.verify_search_exist()

        self.web_driver.find_element_by_id("search_text").send_keys(self.datasourcename)
        self.web_driver.find_element_by_xpath("//button[@class='btn btn-default']").click()
        assert self.ui_utils.waitForTextOnPage(self.server_name, 15)
        return True

    def simple_search_messagings(self):

        self.web_session.web_driver.get("{}//middleware_messaging/show_list".format(self.web_session.MIQ_URL))
        assert self.ui_utils.waitForTextOnPage("Middleware Messagings", 15)
        self.verify_search_exist()

        self.web_driver.find_element_by_id("search_text").send_keys(self.jmstopicname)
        self.web_driver.find_element_by_xpath("//button[@class='btn btn-default']").click()
        assert self.ui_utils.waitForTextOnPage(self.server_name, 15)
        return True

    def save_advanced_search(self):

        self.web_session.web_driver.get("{}//ems_middleware/show_list".format(self.web_session.MIQ_URL))
        assert self.ui_utils.waitForTextOnPage("Middleware Providers", 15)
        view(self.web_session).list_View()
        self.verify_search_exist()
        self.web_driver.find_element_by_xpath("//button[@id='adv_search']").click()
        assert self.ui_utils.waitForTextOnPage("Advanced Search", 15)
        self.web_driver.find_element_by_xpath("//button[@data-id='chosen_typ']").click()
        assert self.ui_utils.waitForTextOnPage("Field", 15)
        self.web_driver.find_element_by_xpath("//span[contains(.,'Field')]").click()
        self.ui_utils.sleep(10)
        self.web_driver.find_element_by_xpath("//button[@data-id='chosen_field']").click()
        assert self.ui_utils.waitForTextOnPage("Middleware Provider : Name", 15)
        self.web_driver.find_element_by_xpath("//span[contains(.,'Middleware Provider : Name')]").click()
        self.ui_utils.sleep(10)
        el_textbox = self.web_driver.find_element_by_xpath("//input[@id='chosen_value']")
        self.ui_utils.wait_until_element_displayed(el_textbox, 5)
        self.web_driver.find_element_by_xpath("//input[@id='chosen_value']").send_keys(self.provider_name)
        window_before = self.web_driver.window_handles[0]
        #print window_before
        self.web_driver.find_element_by_xpath("//button[@title='Commit expression element changes']").click()
        self.ui_utils.sleep(10)
        self.ui_utils.waitForElementOnPage(By.XPATH, "//h4[@id='adv_search_label']", 5)
        assert self.ui_utils.waitForTextOnPage("Save", 15)

        #To do work on clicking save button inside modal window by switching window
        #self.web_driver.find_element_by_xpath("/html/body/div[3]/div/div/div[4]/div/button[3]").click()

        el_searchname = self.web_driver.find_element_by_xpath("//input[@id='search_name']")
        self.ui_utils.wait_until_element_displayed(el_searchname, 15)
        self.web_driver.find_element_by_xpath("//input[@id='search_name']").send_keys(self.search_provider_name)
        self.web_driver.find_element_by_xpath("//button[@title='Save the current search']").click()
        assert self.ui_utils.waitForTextOnPage("Middleware Provider search '{}' was saved".format(self.search_provider_name), 15)
        self.web_driver.find_element_by_xpath("//button[@title='Apply the current filter']").click()
        self.verify_saved_filter()

        return True

    def verify_saved_filter(self):

        self.web_session.web_driver.get("{}//ems_middleware/show_list".format(self.web_session.MIQ_URL))
        assert self.ui_utils.waitForTextOnPage("Middleware Providers", 15)
        self.web_driver.find_element_by_xpath("//a[contains(.,'My Filters')]")
        assert self.ui_utils.waitForTextOnPage(self.search_provider_name, 15)

        return True

    def apply_advanced_search(self):
        self.web_session.web_driver.get("{}//ems_middleware/show_list".format(self.web_session.MIQ_URL))
        assert self.ui_utils.waitForTextOnPage("Middleware Providers", 15)
        if self.web_driver.find_element_by_xpath("//a[contains(.,'My Filters')]"):
            self.delete_saved_search()
            self.save_advanced_search()
        else:
            self.save_advanced_search()
            self.web_driver.find_element_by_xpath("//button[@id='adv_search']").click()
            assert self.ui_utils.waitForTextOnPage("Advanced Search", 15)
            self.web_driver.find_element_by_xpath("//a[@title='Apply this filter']").click()
            assert self.web_driver.find_element_by_xpath("//a[contains(@href,'clear')]")
            assert self.ui_utils.waitForTextOnPage(self.provider_name, 15)

    def delete_saved_search(self):
        self.web_session.web_driver.get("{}//ems_middleware/show_list".format(self.web_session.MIQ_URL))
        assert self.ui_utils.waitForTextOnPage("Middleware Providers", 15)
        self.web_driver.find_element_by_xpath("//a[contains(.,'My Filters')]")
        self.ui_utils.waitForTextOnPage(self.search_provider_name, 15).click()
        self.web_driver.find_element_by_xpath("//button[@id='adv_search']").click()
        assert self.ui_utils.waitForTextOnPage("Advanced Search", 15)
        self.web_driver.find_element_by_xpath("//a[@class='btn btn-danger']").click()
        ui_utils(self.web_session).accept_alert(10)
        assert self.ui_utils.waitForTextOnPage("Delete successful", 15)
        self.web_driver.find_element_by_xpath("//button[@class='close']")

        return True





