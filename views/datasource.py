from common.ui_utils import ui_utils
from parsing.table import table
from navigation.navigation import NavigationTree
from hawkular.hawkular_api import hawkular_api
from common.db import db

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class datasources():
    web_session = None

    def __init__(self, web_session):
        self.web_session = web_session
        self.web_driver = web_session.web_driver
        self.ui_utils = ui_utils(self.web_session)
        self.hawkular_api = hawkular_api(self.web_session)


    def validate_datasource_list(self):
        nav= NavigationTree(self.web_session)
        nav.navigate_to_middleware_datasources_view()

        haw= hawkular_api(self.web_session)
        tab = table(self.web_session)
        dataDb = db(self.web_session)

        datasource_api = self.hawkular_api.get_hawkular_datasources()
        datasource_ui = table(self.web_session).get_middleware_datasources_table()
        datasource_db = db(self.web_session).get_datasources()
        assert len(datasource_db) == len(datasource_ui) == len(datasource_api), "Datasource length match"

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
        datasource_ui = table(self.web_session).get_middleware_datasources_table()
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
            assert dat_details_ui.get('Nativeid') == dat_details_api.get('Nativeid')

        return True

    def count_datasources_ui(self):
        return len(self.web_session.web_driver.find_elements_by_xpath("//div[@id='list_grid']/table/tbody/tr"))

    def count_datasources_db(self):
        return len(db(self.web_session).get_datasources())


    def validate_delete_datasource_b(self):
        self.web_session.logger.info("Begin undeletable datasource test B")
        driver = self.web_session.web_driver

        nav = NavigationTree(self.web_session).jump_to_middleware_datasources_view()
        number_before = self.count_datasources_ui()
        number_before_db = self.count_datasources_db()
        nav.check_first_datasource()
        nav.select_and_click('Operations', 'Remove')
        alert = driver.switch_to_alert()
        alert.accept()

        # to verify deletion was formally completed
        xpath_flash = "//strong[contains(.,'The selected datasources were removed')]"
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath_flash)))
        flasher = driver.find_element_by_xpath(xpath_flash)
        if flasher:
            print "Flasher is displayed."

        number_after = self.count_datasources_ui()
        number_after_db = self.count_datasources_db()
        assert (number_before == number_after + 1), " Datasource can't be deleted. "
        assert (number_before_db == number_after_db + 1), " Datasource can't be deleted. (according DB) "


    def validate_delete_datasource_a(self):
        self.web_session.logger.info("Begin undeletable datasource test A")
        driver = self.web_session.web_driver
        ds = datasources(self.web_session)
        nav = NavigationTree(self.web_session).jump_to_middleware_datasources_view().to_first_details()
        number_before = ds.count_datasources_ui()
        number_before_db = ds.count_datasources_db()
        nav.select_and_click('Operations', 'Remove')
        alert = driver.switch_to_alert()
        alert.accept()

        # to verify deletion was formally completed
        xpath_flash = "//strong[contains(.,'The selected datasources were removed')]"
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath_flash)))
        flasher = driver.find_element_by_xpath(xpath_flash)
        if flasher:
            print "Flasher is displayed."

        number_after = ds.count_datasources_ui()
        number_after_db = ds.count_datasources_db()
        assert (number_before == number_after + 1), "Datasource can't be deleted."
        assert (number_before_db == number_after_db + 1), "Datasource can't be deleted. (according DB)"