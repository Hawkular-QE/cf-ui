from common.ui_utils import ui_utils
from hawkular.hawkular_api import hawkular_api
from common.db import db
import time
import re
from views.servers import servers
from selenium.webdriver.common.by import By

class datasources():
    web_session = None
    datasource_desc = "H2-Test"

    def __init__(self, web_session):
        self.web_session = web_session
        self.web_driver = web_session.web_driver
        self.ui_utils = ui_utils(self.web_session)
        self.hawkular_api = hawkular_api(self.web_session)


    def validate_datasource_list(self):
        self.web_session.web_driver.get("{}/middleware_datasource/show_list".format(self.web_session.MIQ_URL))

        datasource_api = self.hawkular_api.get_hawkular_datasources()
        datasource_ui = self.ui_utils.get_list_table()
        datasource_db = db(self.web_session).get_datasources()
        #assert len(datasource_db) == len(datasource_ui) == len(datasource_api), "Datasource length match"
        assert len(datasource_db) == len(datasource_ui), "Datasource length match"

        for data_ui in datasource_ui:
            datasource_name = data_ui.get('Datasource Name')
            data_api = self.ui_utils.find_row_in_list(datasource_api, 'Name', datasource_name)

            assert data_api, "Datasource Name {} not found".format(datasource_name)
            assert (datasource_name == data_api.get("Name")), \
                "Datasource Name mismatch ui:{}, hawk:{}".format(datasource_name, data_api.get("Name"))
            self.web_session.logger.info(
                "UI Datasource name is: {}, and Hawkular datasource is: {} ".format(datasource_name,
                                                                                    data_api.get("Name")))

        return True

    def validate_datasource_detail(self):
        self.web_session.web_driver.get("{}/middleware_datasource/show_list".format(self.web_session.MIQ_URL))

        datasource_ui = self.ui_utils.get_list_table()
        datasource_api = self.hawkular_api.get_hawkular_datasources()

        for dat in self.ui_utils.get_random_list(datasource_ui, 3):
            datasource_name = dat.get('Datasource Name')
            self.web_session.logger.info("Validate Datasource {}.".format(datasource_name))

            self.web_session.web_driver.get("{}/middleware_datasource/show_list".format(self.web_session.MIQ_URL))
            assert self.ui_utils.waitForTextOnPage("Middleware Datasources", 15)

            self.ui_utils.click_on_row_containing_text(datasource_name)
            self.ui_utils.waitForTextOnPage("Nativeid", 15)
            dat_details_ui = self.ui_utils.get_generic_table_as_dict()
            self.web_session.logger.info("dat_details_ui: {}".format(dat_details_ui))
            dat_details_api = self.ui_utils.find_row_in_list(datasource_api, 'Name', datasource_name)
            self.web_session.logger.info("dat_details_api: {}".format(dat_details_api))

            assert dat_details_ui.get('Name') == dat_details_api.get('Name')

        return True

    def delete_datasource_list_view(self):

        datasource_to_delete = self.datasource_desc
        servers(self.web_session).navigate_to_non_container_eap()
        self.web_session.web_driver.find_element_by_xpath("//td[contains(.,'Middleware Datasources')]").click()
        assert self.ui_utils.waitForTextOnPage('All Middleware Datasources', 15)
        datasources = self.ui_utils.get_list_table_as_elements()
        currrent_datasource_count = len(datasources)

        if not datasources:
            self.web_session.logger.warn("No Datasource found.")
            return True

        for row in datasources:
            datasource = self.ui_utils.find_row_in_element_table_by_text(datasources, datasource_to_delete)
            datasource_name = datasource[2].text
            server = datasource[3].text
            host_name = datasource[4].text

            self.web_session.logger.info("Attempt to delete Dastasource: Name: {}  Server: {}  Host Name: {}".
                                          format(datasource_name, server, host_name))

            self.web_session.web_driver.find_element_by_xpath(
                "//td[contains(text(),'{}')]/preceding-sibling::td/input[@type='checkbox']".format(datasource_name)).click()

            self.ui_utils.web_driver.find_element_by_xpath('.//*[@title="Operations"]').click()
            assert self.ui_utils.waitForElementOnPage(By.ID,
                                            'middleware_datasource_operations_choice__middleware_datasource_remove', 5)
            self.ui_utils.web_driver.find_element_by_id(
                'middleware_datasource_operations_choice__middleware_datasource_remove').click()
            self.ui_utils.accept_alert(5)

            # Hawkular Datasources can not be deleted
            try:
                if not self.ui_utils.waitForTextOnPage('datasources were removed', 5):
                    self.web_session.logger.warn("Datasource Not Removed: Name: {}  Server: {}  Host Name: {}".
                                                  format(datasource_name, server, host_name))
                    # Deselect checkbox
                    datasource[0].click()
                    raise
                break
            except:
                assert self.ui_utils.waitForTextOnPage('Not removed datasources for {} on the provider itself'.
                                                       format(datasource_name), 5)
                datasources.remove(datasource)

        assert self.wait_for_datasource_to_be_deleted(currrent_datasource_count, (60 * 5))

        return True

    def delete_datasource_detail_view(self, list_view=True):

        index = 0
        datasource_to_delete = self.datasource_desc

        self.web_session.web_driver.get("{}/middleware_datasource/show_list".format(self.web_session.MIQ_URL))
        datasources = self.ui_utils.get_list_table_as_elements()
        currrent_datasource_count = len(datasources)

        if not datasources:
            self.web_session.logger.warn("No Datasource found.")
            return True

        for row in datasources:
            datasource = self.ui_utils.find_row_in_element_table_by_text(datasources, datasource_to_delete)
            datasource_name = datasource[2].text
            server = datasource[3].text
            host_name = datasource[4].text

            self.web_session.logger.info("Attempt to delete Dastasource: Name: {}  Server: {}  Host Name: {}".
                                         format(datasource_name, server, host_name))

            # Click on Datasource to get to Detail view

            datasource[2].click()

            # Operations will not be present for a Datasource on a Provider
            try:
                self.ui_utils.web_driver.find_element_by_xpath('.//*[@title="Operations"]').click()
                assert self.ui_utils.waitForElementOnPage(By.ID,
                                        'middleware_datasource_operations_choice__middleware_datasource_remove', 5)
                self.ui_utils.web_driver.find_element_by_id(
                    'middleware_datasource_operations_choice__middleware_datasource_remove').click()
                self.ui_utils.accept_alert(5)

                assert self.ui_utils.waitForTextOnPage('datasources were removed', 5)
                break
            except:
                self.web_session.web_driver.get("{}/middleware_datasource/show_list".format(self.web_session.MIQ_URL))
                datasources = self.ui_utils.get_list_table_as_elements()
                index += 1
                continue

        self.web_session.web_driver.get("{}/middleware_datasource/show_list".format(self.web_session.MIQ_URL))
        assert self.wait_for_datasource_to_be_deleted(currrent_datasource_count, (60 * 5))

        return True

    def wait_for_datasource_to_be_deleted(self, starting_count, time_to_wait):

        servers(self.web_session).navigate_and_refresh_provider()
        servers(self.web_session).navigate_to_non_container_eap()
        self.web_session.web_driver.find_element_by_xpath("//td[contains(.,'Middleware Datasources')]").click()
        assert self.ui_utils.waitForTextOnPage('All Middleware Datasources', 15)

        currentTime = time.time()

        while True:
            if len(self.ui_utils.get_list_table_as_elements()) < starting_count:
                break

            if time.time() - currentTime >= time_to_wait:
                self.web_session.logger.error("Timed out waiting for Datasource to be Deleted in Datasource List.")
                return False

            time.sleep(2)
            self.web_driver.refresh()

        return True
