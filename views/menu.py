from common.ui_utils import ui_utils
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from hawkular.hawkular_api import hawkular_api
#from selenium.common.exceptions import TimeoutException
#from selenium.common.exceptions import ElementNotVisibleException

class menu():
    web_session = None
    MIQ_BASE_VERSION = "master"
    ui_utils = None
    web_driver = None

    def __init__(self, web_session):
        self.web_session = web_session
        self.web_driver = web_session.web_driver
        self.hawkular_api = hawkular_api(self.web_session)
        self.ui_utils = ui_utils(self.web_session)

    def validate_all_middleware_summary_and_relationships(self):
        self.navigate_to_middleware() # ems_middleware
        self.navigate_to_middleware("middleware_domain", "Name")
        self.navigate_to_middleware("middleware_server", "Feed")
        self.navigate_to_middleware("middleware_deployment", "Deployment Name")
        self.navigate_to_middleware("middleware_datasource", "Datasource Name")
        self.navigate_to_middleware("middleware_messaging", "Messaging Name")

    def navigate_to_middleware(self, where="ems_middleware", waitForText="Hostname"):
        if not self.redirect_and_wait_for_change("{}//{}/show_list?type=list".format(self.web_session.MIQ_URL, where), waitForText):
            return
        self.validate_rows(where, waitForText, 2)

    def redirect_and_wait_for_change(self, where, waitForText=""):
        self.web_session.web_driver.get(where)
        if not self.ui_utils.waitForTextOnPage(waitForText, 15):
            if (self.ui_utils.waitForTextOnPage("No Records Found", 15)):
                self.web_session.logger.info("No recrods at {} - skipping validation".format(self.web_driver.current_url))
                return False
        assert self.ui_utils.waitForTextOnPage(waitForText, 15)
        return True

    # validate each row in MW menu view, count=0 for all rows, otherwise 'count' used for random limit
    def validate_rows(self, where, waitForText="", count=3):
        self.ui_utils.waitForTextOnPage(waitForText, 15)
        self.ui_utils.waitForElementOnPage(By.XPATH,"//th[contains(.,'"+waitForText+"')]/../../..//tbody/tr",15)
        rows_count = len(self.ui_utils.get_list_table_as_elements()) if count == 0 else count
        index = 0
        while(index < rows_count):
            table = self.ui_utils.get_list_table_as_elements() if count == 0 else self.ui_utils.get_random_list(self.ui_utils.get_list_table_as_elements(), count)
            self.web_session.logger.info("At: {} Current row index: {}".format(self.web_driver.current_url, str(index)))
            # in case there is not that many lines set max rows (rows_count) to new limit and update index
            if index >= table.__len__():
                rows_count = table.__len__()
                index = rows_count - 1
                if index < 0:
                    self.web_session.logger.info(
                        "Not validating anything for URL: {}".format(self.web_driver.current_url))
                    break

            row = table[index]
            # because row[2] is usually td with (mostly or sufficiently unique) text so together with h1 it should be enough to validate same page
            # todo add current and previous url check
            current_url = self.web_driver.current_url
            row[2].click()

            self.validate_summary_button()
            self.validate_relationships_buttons()
            self.validate_relationships_buttons(disabled=True)

            self.redirect_and_wait_for_change(current_url, waitForText)

            index=index+1

    # disabled - for disabled buttons do not redirect
    # otherwise iterate over relationships items ( click on item, check that redirect happen, go back )
    def validate_relationships_buttons(self, disabled = False):
        if disabled == False:
            relationships_rows_len = len(self.web_driver.find_elements_by_xpath(
                "//*[@id='listnav_div']//a[contains(.,'Relationships')]/../../..//li[not(contains(@class,'disabled'))]/a[not(contains(.,'Relationships'))]"))
        else:
            relationships_rows_len = len(self.web_driver.find_elements_by_xpath(
                "//*[@id='listnav_div']//a[contains(.,'Relationships')]/../../..//li[contains(@class,'disabled')]/a[not(contains(.,'Relationships'))]"))
        index = 1 # 0 is empty
        # for row in relationships_rows:
        while index <= relationships_rows_len:
            self.ui_utils.waitForElementOnPage(By.XPATH, "//h1", 15)
            current_H1_text = self.web_driver.find_element_by_xpath("//h1").text
            current_url = self.web_driver.current_url
            self.web_session.logger.info("At {} H1: {}".format(current_url, current_H1_text))
            if disabled == False:
                xpath_collapsing = "(//*[@id='listnav_div']//*[contains(@id,'middleware_deployment_rel') and not(contains(@class,'collapsing')) ]" \
                        "/..//li[not(contains(@class,'disabled'))]//a[not(contains(.,'Relationships'))])[" + str(index) + "]"
                xpath_to_click = "(//*[@id='listnav_div']//a[contains(.,'Relationships')]/../../..//li[not(contains(@class,'disabled'))]" \
                        "//a[not(contains(.,'Relationships'))])[" + str(index) + "]"

            else:
                xpath_collapsing = "(//*[@id='listnav_div']//*[contains(@id,'middleware_deployment_rel') and contains(@class,'collapsing')]" \
                        "/..//li[not(contains(@class,'disabled'))]//a[not(contains(.,'Relationships'))])[" + str(index) + "]"

                xpath_to_click = "(//*[@id='listnav_div']//a[contains(.,'Relationships')]/../../..//li[contains(@class,'disabled')]" \
                        "//a[not(contains(.,'Relationships'))])[" + str(index) + "]"
            # elements not element, it was not recognizing just one element idk why

            # for a certain time there might be element with this xpath while the 'collapsing' class exist while animating
            self.ui_utils.waitForElementOnPage(By.XPATH,xpath_collapsing, 5, show_as_error=False)
            self.ui_utils.waitForElementOnPage(By.XPATH,xpath_collapsing, 5, False, show_as_error=False)

            self.open_links_href(xpath=xpath_to_click)

            if disabled == False:
                # todo check status code and errors on page and in logs
                self.ui_utils.waitForElementOnPage(By.XPATH, "//h1", 15)
                self.web_session.logger.info("At {} H1: {}".format(current_url,
                    self.web_driver.find_element_by_xpath("//h1").text))
                # the current details page should contain different h1 then the previous detail page
                assert self.ui_utils.waitForElementOnPage(By.XPATH, "//h1[not(contains(.,'{}'))]".format(current_H1_text), 15)
                self.redirect_and_wait_for_change(current_url)

            # this will fail in case that h1 is still same, g.e. its still same list page, but for this is meant Summary and not Relationships
            self.ui_utils.waitForElementOnPage(
                By.XPATH, "//h1[contains(.,'{}')]".format(current_H1_text), 15)
            index = index + 1

    def validate_summary_button(self):
        self.ui_utils.waitForElementOnPage(By.XPATH,  "//h1", 15)
        current_H1_text =  self.web_driver.find_element_by_xpath("//h1").text

        self.open_links_href(xpath="//a[contains(.,'Summary')]")

        # previous h1 must match current h1 because it is the same page
        self.ui_utils.waitForElementOnPage(By.XPATH,  "//h1[contains(.,'{}')]".format(current_H1_text), 15)

    def open_links_href(self,xpath, seconds=15):
        self.ui_utils.waitForElementOnPage(By.XPATH, xpath, 15)
        maybe_present_elem_row = self.web_driver.find_element_by_xpath(xpath)
        self.redirect_and_wait_for_change(where=maybe_present_elem_row.get_attribute("href"))
