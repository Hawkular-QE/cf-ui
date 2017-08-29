from common.ui_utils import ui_utils
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from hawkular.hawkular_api import hawkular_api
from common.view import view
from common.db import db
import time
from common.timeout import timeout

class provider_base(object):
    web_session = None
    MIQ_BASE_VERSION = "master"
    ui_utils = None
    provider_type = None
    provider_url_part = None  # default

    summary_xpath = "//button[@id='view_summary']"

    def __init__(self, web_session, provider_name=None, provider_type = "middleware", provider_type_name = "Middleware", provider_url_part = "ems_middleware", provider_db_name="Hawkular", provider_known_name="Hawkular"):
        self.web_session = web_session
        self.web_driver = web_session.web_driver
        self.hawkular_api = hawkular_api(self.web_session)
        self.ui_utils = ui_utils(self.web_session)
        # Name as it shows in UI and DB, should be unique
        self.provider_name = provider_name
        # Type of provider - middleware/infrastructure/openshift
        self.provider_type = provider_type
        # used by waitForTextOnPage
        self.provider_type_name = provider_type_name
        # used by self.web_session.web_driver.get("{}//{}/show_list".format(self.web_session.MIQ_URL,self.provider_url_part))
        self.provider_url_part = provider_url_part
        # used by common/db.py
        self.provider_type_db_name = provider_db_name

    def add_provider(self, delete_if_provider_present=True, port=None, validate_provider=True):

        self.appliance_version = self.web_session.appliance_version

        # Check if any provider already exist. If exist, first delete all the providers and then add a provider.

        if self.does_provider_exist():
            self.web_session.logger.info("{} Provider already exist.".format(self.provider_type_name))
            if delete_if_provider_present:
                self.delete_provider(delete_all_providers=True)
            else:
                return
        else:
            self.web_session.logger.info("Adding {} Provider to ManageIQ instance".format(self.provider_type_name))

        self.web_session.web_driver.get("{}//{}/show_list".format(self.web_session.MIQ_URL,self.provider_url_part))
        assert ui_utils(self.web_session).waitForTextOnPage("{} Providers".format(self.provider_type_name), 15)

        self.web_driver.find_element_by_xpath("//button[@title='Configuration']").click()
        self.ui_utils.waitForElementOnPage(By.XPATH, "//a[@title='Add a New {} Provider']".format(self.provider_type_name), 5)
        elem_add_new_provider = self.web_driver.find_element_by_xpath("//a[@title='Add a New {} Provider']".format(self.provider_type_name))
        elem_add_new_provider.click()
        self.web_driver.implicitly_wait(15)
        assert ui_utils(self.web_session).waitForTextOnPage("Add New {} Provider".format(self.provider_type_name), 15)
        ui_utils(self.web_session).sleep(2)

        self.web_session.logger.info("The appliance version in use is: {} ".format(self.web_session.appliance_version))

        self.submit_provider_form_cfme(validate_provider)

        self.verify_add_provider_success()


    def submit_provider_form_cfme(self):
        # override me

        #if validate_provider:
        #    self.validate_provider()
        #self.save_provider()

        return

    def delete_provider(self, delete_all_providers=True):

        self.web_session.web_driver.get("{}//{}/show_list".format(self.web_session.MIQ_URL,self.provider_url_part))
        assert ui_utils(self.web_session).waitForTextOnPage("{} Providers".format(self.provider_type_name), 30)
        #self.ui_utils.sleep(15)

        # Delete the provider
        if delete_all_providers:
            self.clear_all_providers()
        else:
            self.delete_single_provider()

    def update_provider(self, add_provider=True):
        self.web_session.logger.info("Checking if provider exist and add if it does not.")
        if add_provider:
            self.add_provider(delete_if_provider_present=False)

        self.web_session.web_driver.get("{}//{}/show_list".format(self.web_session.MIQ_URL,self.provider_url_part))
        assert ui_utils(self.web_session).waitForTextOnPage("{} Providers".format(self.provider_type_name), 30)
        self.web_driver.find_element_by_xpath("//input[contains(@type,'checkbox')]").click()
        self.web_driver.find_element_by_xpath("//button[@title='Configuration']").click()
        self.ui_utils.waitForElementOnPage(By.XPATH, "//a[contains(.,'Edit Selected {} Provider')]".format(self.provider_type_name), 5)
        elem_editprovider_link = self.web_driver.find_element_by_xpath(
            "//a[contains(.,'Edit Selected {} Provider')]".format(self.provider_type_name))
        elem_editprovider_link.click()
        # continue with inheritance

    def edit_save_cfme(self):
        # Wait till Save button is enabled before click
        edit_save_cfme = WebDriverWait(self.web_driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Save')]")))
        edit_save_cfme.click()
        assert ui_utils(self.web_session).waitForTextOnPage('saved', 15)

    def add_provider_if_not_present(self):
        self.web_session.logger.info("Check if provider exist and add if it does not")
        # If provider is not present, add provider
        if self.does_provider_exist():
            self.web_session.logger.info("{} Provider already exist.".format(self.provider_type_name))
        else:
            self.add_provider(delete_if_provider_present=False)

    def does_provider_exist(self):
        self.web_session.logger.info("Checking if provider exists")

        # For performance reasons, check if the provider is present via DB
        providers = db(self.web_session).get_providers(type=self.provider_type_db_name)
        provider = ui_utils(self.web_session).find_row_in_list(providers, 'name', self.provider_name)
        if provider:
            return True
        else:
            return False

    def delete_single_provider(self):

        if not self.does_provider_exist():
            self.web_session.logger.warning("Provider {} not present.".format(self.provider_name))
            return True

        self.web_session.web_driver.get("{}//{}/show_list".format(self.web_session.MIQ_URL,self.provider_url_part))
        assert ui_utils(self.web_session).waitForTextOnPage("{} Providers".format(self.provider_type_name), 30)
        self.web_session.logger.info("Deleting the provider- {}".format(self.provider_name))
        self.web_driver.find_element_by_xpath("//input[contains(@type,'checkbox')]").click()
        self.web_driver.find_element_by_xpath("//button[@title='Configuration']").click()
        assert self.ui_utils.waitForElementOnPage(By.XPATH,
                                                  "//a[@title='Remove selected {} Providers']".format(self.provider_type_name), 5)
        self.web_driver.find_element_by_xpath(
            "//a[@title='Remove selected {} Providers']".format(self.provider_type_name)).click()
        ui_utils(self.web_session).accept_alert(10)
        assert ui_utils(self.web_session).waitForTextOnPage("Delete initiated", 15)

        # Verify if the provider is deleted from the provider list.

        assert ui_utils(self.web_session).waitForElementOnPage(By.XPATH, "//a[@title='{}']".format(
            self.provider_name), 180, exist=False)
        if not ui_utils(self.web_session).isTextOnPage(self.provider_name):
            self.web_session.logger.info(
                "The provider - {} - is deleted successfully".format(self.provider_name))

    def clear_all_providers(self):
        self.web_session.logger.info("Deleting all the providers from providers list.")
        view(self.web_session).list_View()

        if not self.appliance_version == self.MIQ_BASE_VERSION:
            self.web_driver.find_element_by_xpath("//input[@id='masterToggle']").click()
        else:
            self.ui_utils.waitForElementOnPage(By.XPATH, "//input[@ng-click='tableCtrl.onCheckAll(isChecked)']", 5)
            self.web_driver.find_element_by_xpath("//input[@ng-click='tableCtrl.onCheckAll(isChecked)']").click()

        self.web_driver.find_element_by_xpath("//button[@title='Configuration']").click()
        assert self.ui_utils.waitForElementOnPage(By.XPATH,
                                         "//a[@title='Remove selected {} Providers']".format(self.provider_type_name), 5)
        self.web_driver.find_element_by_xpath(
            "//a[@title='Remove selected {} Providers']".format(self.provider_type_name)).click()
        ui_utils(self.web_session).accept_alert(10)
        assert ui_utils(self.web_session).waitForTextOnPage(
            "Delete initiated", 15)

        self.verify_all_providers_deleted()

    def verify_refresh_status_success(self):

        refresh_value_success = "Success"

        self.refresh_provider()

        # Refresh the page till till the table value for Last Refresh shows the value - Success

        assert self.wait_for_provider_refresh_status(refresh_value_success, 600)
        provider_details = ui_utils(self.web_session).get_generic_table_as_dict()

        # Verify if the 'Last Refresh' value from table contains 'Success:
        refresh_status = provider_details.get("Last Refresh")

        if str(refresh_status).__contains__(refresh_value_success):
            self.web_session.logger.info("The Last refresh status is - " + refresh_status)
            return True
        else:
            return False

    refresh_provider_id = "ems_middleware_vmdb_choice__ems_middleware_refresh"

    def refresh_provider(self):
        self.web_driver.find_element_by_xpath("//button[@title='Configuration']").click()
        el = self.web_driver.find_element_by_id(self.refresh_provider_id)
        assert self.ui_utils.wait_until_element_displayed(el, 5)
        el.click()
        ui_utils(self.web_session).accept_alert(10)
        ui_utils(self.web_session).waitForTextOnPage("Refresh Provider initiated", 15)

    def validate_providers_list(self):

        # Test to validate provider list page in UI and validate matching providers hostname, port number

        self.web_session.logger.info("Begin providers list test.")
        self.web_session.web_driver.get("{}//{}/show_list".format(self.web_session.MIQ_URL,self.provider_url_part))
        providers_ui = self.ui_utils.get_list_table()
        assert len(providers_ui) > 0, "Providers list is empty."

        for prov_ui in providers_ui:
            if prov_ui.get('Name') == self.provider_name:
                self.validate_providers_list_asserts(prov_ui)

        return True

    def validate_providers_list_asserts(self, prov_ui):
        # override
        # assert (prov_ui.get('Hostname') == self.web_session.HAWKULAR_HOSTNAME), "Hostname mismatch"
        # assert (prov_ui.get('Port') == self.web_session.HAWKULAR_PORT), "Port Number mismatch"
        return

    def validate_providers_details(self):

        # Test to validate ??? provider details like name, hostname, port number
        # and to validate number of middleware servers, deployments and datasources in releationships section.

        self.web_session.logger.info("Begin providers details test.")
        self.web_session.web_driver.get("{}//{}/show_list".format(self.web_session.MIQ_URL,self.provider_url_part))
        view(self.web_session).list_View()
        providers_ui = self.ui_utils.get_list_table()

        for prov_ui in providers_ui:
            if prov_ui.get('Name') == self.provider_name:
                ui_utils(self.web_session).click_on_row_containing_text(self.provider_name)

        assert ui_utils(self.web_session).waitForTextOnPage("Status", 15)
        providers_details_ui = ui_utils(self.web_session).get_generic_table_as_dict()

        return True

    #override
    recheck_auth_id="ems_middleware_authentication_choice__ems_middleware_recheck_auth_status"

    def recheck_authentication(self):
        # Test for Authentication->Recheck Authentication' on ??? provider

        self.web_session.logger.info("Begin test for Authentication->Recheck Authentication.")
        self.web_session.web_driver.get("{}//{}/show_list?type=list".format(self.web_session.MIQ_URL,self.provider_url_part))

        ui_utils(self.web_session).click_on_row_containing_text(self.provider_name)
        self.web_driver.find_element_by_xpath("//h1[contains(.,'{}-Provider (Summary)')]".format(self.provider_type_name))

        self.web_driver.find_element_by_xpath("//button[@title='Authentication']").click()
        assert self.ui_utils.waitForElementOnPage(By.ID, self.recheck_auth_id, 5)
        self.web_driver.find_element_by_id(self.recheck_auth_id).click()

        ui_utils(self.web_session).sleep(2)
        assert ui_utils(self.web_session).waitForTextOnPage("Authentication status will be saved and workers will be restarted for the selected {} Provider".format(self.provider_type_name), 15)

        return True

    def verify_add_provider_success(self):

        assert ui_utils(self.web_session).waitForTextOnPage(
            '{} Providers "{}" was saved'.format(self.provider_type_name ,self.provider_name), 90)

        if ui_utils(self.web_session).isElementPresent(By.XPATH, "//a[contains(@title,'Name: {}')]".format(
                self.provider_name)):
            self.web_session.logger.info("{} Provider added successfully.".format(self.provider_type_name))

        # Navigate to the provider details page and check if the last refresh status is - Success.

        view(self.web_session).list_View()
        assert ui_utils(self.web_session).waitForTextOnPage(self.provider_name, 30)
        ui_utils(self.web_session).click_on_row_containing_text(self.provider_name)

        assert ui_utils(self.web_session).waitForTextOnPage("Status", 30)

        assert self.verify_refresh_status_success(), "The last refresh status is not - Success"

    def validate_provider(self):
        validate = WebDriverWait(self.web_driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, "//button[@title='Validate the credentials by logging into the Server']")))
        validate.click()
        assert ui_utils(self.web_session).waitForTextOnPage('Credential validation was successful', 60)

    def save_provider(self):

        if str(self.web_session.appliance_version) != '5.7*':
            xpath = "//button[contains(text(),'Add')]"
        else:
            xpath = "//button[contains(@ng-click,'addClicked($event, true)')]"

        with timeout(seconds=15, error_message="Timed out waiting for Save."):
            while True:
                WebDriverWait(self.web_driver, 10).until(EC.element_to_be_clickable(
                    (By.XPATH, xpath)))
                self.web_driver.find_element_by_xpath(xpath).click()
                if (self.ui_utils.isTextOnPage(" was saved")):
                    self.web_session.logger.info("Provider saved.")
                    break;
                else:
                    self.web_session.logger.info("No Provider save message.")

                time.sleep(1)

    def wait_for_provider_refresh_status(self, expected_status, waitTime):
        currentTime = time.time()

        while True:
            last_refresh = self.ui_utils.get_generic_table_as_dict().get('Last Refresh')

            if expected_status in last_refresh:
                self.web_session.logger.info("Provider Last Refresh Status found: {}".format(last_refresh))
                return True

            if 'Error' in last_refresh and 'Success' in expected_status:
                self.web_session.logger.error("Provider Last Refresh Status contains Error: {}   but expected: {}".
                                              format(last_refresh, expected_status))
                return False

            if time.time() - currentTime >= waitTime:
                self.web_session.logger.error("Timed out waiting for provider Refresh Status: {}   Actual Status: {}".
                                              format(expected_status, last_refresh))
                return False
            else:
                self.web_driver.refresh()
                time.sleep(1)

        return True

    def verify_all_providers_deleted(self):
        self.web_session.web_driver.get("{}//{}/show_list".format(self.web_session.MIQ_URL,self.provider_url_part))
        assert ui_utils(self.web_session).waitForTextOnPage("{} Providers".format(self.provider_type_name), 15)
        while True:
            if self.web_driver.find_element_by_xpath("//strong[contains(.,'No Records Found.')]").is_displayed():
                self.web_session.logger.info("All the {} providers are deleted successfully.".format(self.provider_type_name))
                break
            else:
                self.web_driver.refresh()
                ui_utils(self.web_session).sleep(5)
        return True
