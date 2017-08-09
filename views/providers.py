from common.ui_utils import ui_utils
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from hawkular.hawkular_api import hawkular_api
from common.view import view
from common.db import db
import time
from common.timeout import timeout

class providers():
    web_session = None
    MIQ_BASE_VERSION = "master"
    ui_utils = None

    def __init__(self, web_session):
        self.web_session = web_session
        self.web_driver = web_session.web_driver
        self.hawkular_api = hawkular_api(self.web_session)
        self.ui_utils = ui_utils(self.web_session)
        self.appliance_version = self.web_session.appliance_version

    def add_provider(self, delete_if_provider_present=True, port=None, validate_provider=True):
        self.provider_name = self.web_session.HAWKULAR_PROVIDER_NAME
        self.host_name = self.web_session.HAWKULAR_HOSTNAME
        self.port = self.web_session.HAWKULAR_PORT if port == None else port
        self.hawkular_user = self.web_session.HAWKULAR_USERNAME
        self.hawkular_password = self.web_session.HAWKULAR_PASSWORD


        # Check if any provider already exist. If exist, first delete all the providers and then add a provider.

        if self.does_provider_exist():
            self.web_session.logger.info("Middleware Provider already exist.")
            if delete_if_provider_present:
                self.delete_provider(delete_all_providers=True)
            else:
                return
        else:
            self.web_session.logger.info("Adding Middleware Provider to ManageIQ instance")

        self.web_session.web_driver.get("{}//ems_middleware/show_list".format(self.web_session.MIQ_URL))
        assert ui_utils(self.web_session).waitForTextOnPage("Middleware Providers", 15)

        self.web_driver.find_element_by_xpath("//button[@title='Configuration']").click()
        self.ui_utils.waitForElementOnPage(By.XPATH, "//a[@title='Add a New Middleware Provider']", 5)
        elem_add_new_provider = self.web_driver.find_element_by_xpath("//a[@title='Add a New Middleware Provider']")
        elem_add_new_provider.click()
        self.web_driver.implicitly_wait(15)
        assert ui_utils(self.web_session).waitForTextOnPage("Add New Middleware Provider", 15)
        ui_utils(self.web_session).sleep(2)

        self.web_session.logger.info("The appliance version in use is: {} ".format(self.web_session.appliance_version))

        self.submit_provider_form_cfme(validate_provider)
        self.verify_add_provider_success()


    def submit_provider_form_cfme(self, validate_provider=True):

        # Enter the form details and submit if the appliance version is CFME Downstream

        self.web_driver.find_element_by_xpath("//button[@data-id='emstype']").click()
        assert ui_utils(self.web_session).waitForTextOnPage("Hawkular", 30)
        self.web_driver.find_element_by_xpath("//span[contains(.,'Hawkular')]").click()
        assert ui_utils(self.web_session).waitForTextOnPage("Hostname", 30)

        self.web_driver.find_element_by_xpath("//input[@id='ems_name']").send_keys(self.provider_name)
        self.web_driver.find_element_by_xpath("//input[@id='default_hostname']").send_keys(self.host_name)
        self.web_driver.find_element_by_xpath("//input[@id='default_api_port']").clear()
        self.web_driver.find_element_by_xpath("//input[@id='default_api_port']").send_keys(self.port)

        self.web_driver.find_element_by_xpath("//button[@data-id='default_security_protocol']").click()
        assert ui_utils(self.web_session).waitForTextOnPage("Non-SSL", 30)
        self.web_driver.find_element_by_xpath("//span[contains(.,'Non-SSL')]").click()

        self.web_driver.find_element_by_xpath("//input[@id='default_userid']").send_keys(self.hawkular_user)
        self.web_driver.find_element_by_xpath("//input[@id='default_password']").send_keys(
            self.hawkular_password)

        if not self.MIQ_BASE_VERSION == self.appliance_version:
            self.web_driver.find_element_by_xpath("//input[@id='default_verify']").send_keys(self.hawkular_password)

        if validate_provider:
            self.validate_provider()
        self.save_provider()

    def delete_provider(self, delete_all_providers=True):

        self.web_session.web_driver.get("{}//ems_middleware/show_list".format(self.web_session.MIQ_URL))
        assert ui_utils(self.web_session).waitForTextOnPage("Middleware Providers", 30)
        view(self.web_session).list_View()
        assert ui_utils(self.web_session).waitForTextOnPage(self.web_session.HAWKULAR_PROVIDER_NAME, 30)
        self.ui_utils.sleep(15)

        # Delete the provider
        if delete_all_providers:
            self.clear_all_providers()
        else:
            self.delete_hawkular_provider()

    def update_provider(self, add_provider=True):
        self.web_session.logger.info("Checking if provider exist and add if it does not.")
        if add_provider:
            self.add_provider(delete_if_provider_present=False)

        self.web_session.web_driver.get("{}//ems_middleware/show_list".format(self.web_session.MIQ_URL))
        assert ui_utils(self.web_session).waitForTextOnPage("Middleware Providers", 30)
        self.web_driver.find_element_by_xpath("//input[contains(@type,'checkbox')]").click()
        self.web_driver.find_element_by_xpath("//button[@title='Configuration']").click()
        self.ui_utils.waitForElementOnPage(By.XPATH, "//a[contains(.,'Edit Selected Middleware Provider')]", 5)
        elem_editprovider_link = self.web_driver.find_element_by_xpath(
            "//a[contains(.,'Edit Selected Middleware Provider')]")
        elem_editprovider_link.click()
        ui_utils(self.web_session).sleep(10)
        assert ui_utils(self.web_session).waitForTextOnPage("Name", 30)

        self.edit_provider_form_cfme_newvalues()
        self.validate_provider()
        self.edit_save_cfme()
        self.verify_edit_provider_success_newvalues()
        self.edit_provider_form_cfme_originalvalues()
        self.validate_provider()
        self.edit_save_cfme()
        self.verify_edit_provider_success_originalvalues()

    def edit_provider_form_cfme_newvalues(self):

        self.web_driver.find_element_by_xpath("//input[@id='ems_name']").clear()
        self.web_driver.find_element_by_xpath("//input[@id='ems_name']").send_keys(self.web_session.PROVIDER)

    def verify_edit_provider_success_newvalues(self):

        # Verify if the provider name, is successfully updated and shown in UI

        assert ui_utils(self.web_session).isElementPresent(By.XPATH, "//td[contains(.,'{}')]".format(self.web_session.PROVIDER))
        self.web_session.logger.info("The middleware provider is edited successfully.")

    def edit_provider_form_cfme_originalvalues(self):

        # Edit and save the name to default value.( This will additionally check edit from the provider details page)

        self.web_session.web_driver.get("{}//ems_middleware/show_list".format(self.web_session.MIQ_URL))
        ui_utils(self.web_session).click_on_row_containing_text(self.web_session.PROVIDER)

        self.web_driver.find_element_by_xpath("//button[@title='Configuration']").click()
        self.ui_utils.waitForElementOnPage(By.XPATH, "//a[@title='Edit this Middleware Provider']", 5)
        self.web_driver.find_element_by_xpath("//a[@title='Edit this Middleware Provider']").click()
        ui_utils(self.web_session).sleep(15)
        assert ui_utils(self.web_session).waitForTextOnPage("Name", 30)

        self.web_driver.find_element_by_xpath("//input[@id='ems_name']").clear()
        self.web_driver.find_element_by_xpath("//input[@id='ems_name']").send_keys(self.web_session.HAWKULAR_PROVIDER_NAME)

    def edit_save_cfme(self):

        # Wait till Save button is enabled before click

        edit_save_cfme = WebDriverWait(self.web_driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Save')]")))
        edit_save_cfme.click()
        assert ui_utils(self.web_session).waitForTextOnPage('saved', 15)

    def verify_edit_provider_success_originalvalues(self):

        assert ui_utils(self.web_session).isElementPresent(By.XPATH, "//td[contains(.,'{}')]".format(
            self.web_session.HAWKULAR_PROVIDER_NAME))
        assert ui_utils(self.web_session).isElementPresent(By.XPATH, "//td[contains(.,'{}')]".format(
            self.web_session.HAWKULAR_HOSTNAME))
        assert ui_utils(self.web_session).isElementPresent(By.XPATH, "//td[contains(.,'{}')]".format(
            self.web_session.HAWKULAR_PORT))
        self.web_session.logger.info("The middleware provider is edited to the original values successfully.")

    def add_provider_if_not_present(self):
        self.web_session.logger.info("Check if provider exist and add if it does not")

        # If provider is not present, add provider

        if self.does_provider_exist():
            self.web_session.logger.info("Middleware Provider already exist.")
        else:
            self.add_provider(delete_if_provider_present=False)

    def does_provider_exist(self):
        self.web_session.logger.info("Checking if provider exists")

        # For performance reasons, check if the provider is present via DB
        providers = db(self.web_session).get_providers()
        provider = ui_utils(self.web_session).find_row_in_list(providers, 'name', self.web_session.HAWKULAR_PROVIDER_NAME)
        if provider:
            return True
        else:
            return False

    def delete_hawkular_provider(self):

        if not self.does_provider_exist():
            self.web_session.logger.warning("Provider {} not present.".format(self.web_session.HAWKULAR_HOSTNAME))
            return True

        self.web_session.web_driver.get("{}//ems_middleware/show_list".format(self.web_session.MIQ_URL))
        assert ui_utils(self.web_session).waitForTextOnPage("Middleware Providers", 30)
        self.web_session.logger.info("Deleting the provider- {}".format(self.web_session.HAWKULAR_HOSTNAME))
        self.web_driver.find_element_by_xpath("//input[contains(@type,'checkbox')]").click()
        self.web_driver.find_element_by_xpath("//button[@title='Configuration']").click()

        if not self.appliance_version == self.MIQ_BASE_VERSION:

            assert self.ui_utils.waitForElementOnPage(By.XPATH,
                                                      "//a[@title='Remove selected Middleware Providers']", 5)
            self.web_driver.find_element_by_xpath(
                "//a[@title='Remove selected Middleware Providers']").click()
        else:

            assert self.ui_utils.waitForElementOnPage(By.XPATH,
                                                      "//a[@id='ems_middleware_vmdb_choice__ems_middleware_delete']", 5)
            self.web_driver.find_element_by_xpath(
                "//a[@id='ems_middleware_vmdb_choice__ems_middleware_delete']").click()

        ui_utils(self.web_session).accept_alert(10)
        assert ui_utils(self.web_session).waitForTextOnPage("Delete initiated", 15)

        # Verify if the provider is deleted from the provider list.

        assert ui_utils(self.web_session).waitForElementOnPage(By.XPATH, "//a[@title='{}']".format(
            self.web_session.HAWKULAR_PROVIDER_NAME), 180, exist=False)
        if not ui_utils(self.web_session).isTextOnPage(self.web_session.HAWKULAR_PROVIDER_NAME):
            self.web_session.logger.info(
                "The provider - {} - is deleted successfully".format(self.web_session.HAWKULAR_HOSTNAME))

    def clear_all_providers(self):
        self.web_session.logger.info("Deleting all the providers from providers list.")

        if not self.appliance_version == self.MIQ_BASE_VERSION:
            self.web_driver.find_element_by_xpath("//input[@id='masterToggle']").click()
            self.web_driver.find_element_by_xpath("//button[@title='Configuration']").click()
            assert self.ui_utils.waitForElementOnPage(By.XPATH,
                                                      "//a[@title='Remove selected Middleware Providers']", 5)
            self.web_driver.find_element_by_xpath(
                "//a[@title='Remove selected Middleware Providers']").click()
        else:
            self.ui_utils.waitForElementOnPage(By.XPATH, "//input[@ng-click='paginationCtrl.onSelectAll({isSelected: isChecked})']", 5)
            self.web_driver.find_element_by_xpath("//input[@ng-click='paginationCtrl.onSelectAll({isSelected: isChecked})']").click()
            self.web_driver.find_element_by_xpath("//button[@title='Configuration']").click()
            assert self.ui_utils.waitForElementOnPage(By.XPATH,
                                                      "//a[@id='ems_middleware_vmdb_choice__ems_middleware_delete']", 5)
            self.web_driver.find_element_by_xpath(
                "//a[@id='ems_middleware_vmdb_choice__ems_middleware_delete']").click()


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

    def refresh_provider(self):
        self.web_driver.find_element_by_xpath("//button[@title='Configuration']").click()
        el = self.web_driver.find_element_by_id('ems_middleware_vmdb_choice__ems_middleware_refresh')
        assert self.ui_utils.wait_until_element_displayed(el, 5)
        el.click()
        ui_utils(self.web_session).accept_alert(10)
        ui_utils(self.web_session).waitForTextOnPage("Refresh Provider initiated", 15)

    def validate_providers_list(self):

        # Test to validate provider list page in UI and validate matching providers hostname, port number

        self.web_session.logger.info("Begin providers list test.")
        self.web_session.web_driver.get("{}//ems_middleware/show_list".format(self.web_session.MIQ_URL))
        providers_ui = self.ui_utils.get_list_table()
        assert len(providers_ui) > 0, "Providers list is empty."

        for prov_ui in providers_ui:

            if prov_ui.get('Name') == self.web_session.HAWKULAR_PROVIDER_NAME:
                assert (prov_ui.get('Hostname') == self.web_session.HAWKULAR_HOSTNAME), "Hostname mismatch"
                assert (prov_ui.get('Port') == self.web_session.HAWKULAR_PORT), "Port Number mismatch"

        return True

    def validate_providers_details(self):

        # Test to validate hawkular provider details like name, hostname, port number
        # and to validate number of middleware servers, deployments and datasources in releationships section.

        self.web_session.logger.info("Begin providers details test.")
        self.web_session.web_driver.get("{}//ems_middleware/show_list".format(self.web_session.MIQ_URL))
        view(self.web_session).list_View()
        providers_ui = self.ui_utils.get_list_table()
        servers_hawk = self.hawkular_api.get_hawkular_servers()
        deployments_hawk = self.hawkular_api.get_hawkular_deployments()
        datasources_hawk = self.hawkular_api.get_hawkular_datasources()

        for prov_ui in providers_ui:
            if prov_ui.get('Name') == self.web_session.HAWKULAR_PROVIDER_NAME:
                ui_utils(self.web_session).click_on_row_containing_text(self.web_session.HAWKULAR_PROVIDER_NAME)

        assert ui_utils(self.web_session).waitForTextOnPage("Status", 15)
        providers_details_ui = ui_utils(self.web_session).get_generic_table_as_dict()

        assert (providers_details_ui.get('Name') == self.web_session.HAWKULAR_PROVIDER_NAME), "Provider name mismatch"
        assert (providers_details_ui.get('Host Name') == self.web_session.HAWKULAR_HOSTNAME), "Hostname mismatch"
        assert (providers_details_ui.get('Port') == self.web_session.HAWKULAR_PORT), "Port Number mismatch"

        assert providers_details_ui.get('Middleware Servers') == str(len(servers_hawk)), "Number of servers mismatch"

        self.web_session.logger.debug("UI Deploys: {}  HW Deploys: {}".format(providers_details_ui.get('Middleware Deployments'), str(len(deployments_hawk))))
        # assert providers_details_ui.get('Middleware Deployments') == str(len(deployments_hawk)), "Number of Deployments mismatch"
        #assert providers_details_ui.get('Middleware Datasources') == str(len(datasources_hawk)), "Number of Datasources mismatch"

        return True

    def recheck_authentication(self):

        # Test for Authentication->Recheck Authentication' on hawkular provider

        self.web_session.logger.info("Begin test for Authentication->Recheck Authentication.")
        self.web_session.web_driver.get("{}//ems_middleware/show_list?type=list".format(self.web_session.MIQ_URL))

        ui_utils(self.web_session).click_on_row_containing_text(self.web_session.HAWKULAR_PROVIDER_NAME)
        self.web_driver.find_element_by_xpath("//h1[contains(.,'Hawkular-Provider (Summary)')]")

        self.web_driver.find_element_by_xpath("//button[@title='Authentication']").click()
        assert self.ui_utils.waitForElementOnPage(By.ID, 'ems_middleware_authentication_choice__ems_middleware_recheck_auth_status', 5)
        self.web_driver.find_element_by_id('ems_middleware_authentication_choice__ems_middleware_recheck_auth_status').click()

        ui_utils(self.web_session).sleep(2)
        assert ui_utils(self.web_session).waitForTextOnPage("Authentication status will be saved and workers will be restarted for the selected Middleware Provider", 15)

        return True

    def verify_add_provider_success(self):

        assert ui_utils(self.web_session).waitForTextOnPage(
            'Middleware Providers "{}" was saved'.format(self.provider_name), 90)

        if ui_utils(self.web_session).isElementPresent(By.XPATH, "//a[contains(@title,'Name: {}')]".format(
                self.provider_name)):
            self.web_session.logger.info("Middleware Provider added successfully.")

        # Navigate to the provider details page and check if the last refresh status is - Success.

        view(self.web_session).list_View()
        assert ui_utils(self.web_session).waitForTextOnPage(self.web_session.HAWKULAR_PROVIDER_NAME, 30)
        ui_utils(self.web_session).click_on_row_containing_text(self.web_session.HAWKULAR_PROVIDER_NAME)

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

    def add_provider_invalid_port(self):

        if self.does_provider_exist():
            self.web_session.logger.info("Middleware Provider exist - Delete the provider.")
            self.delete_provider(delete_all_providers=True)

        try:
            self.add_provider(port="1234")
            raise Exception('Add Provider Unexpectedly passed.')
        except:
            # Expected timeout waiting for form Add button to be clickable, since button should not be clickable.
            pass

        return True;

    def verify_all_providers_deleted(self):
        self.web_session.web_driver.get("{}//ems_middleware/show_list".format(self.web_session.MIQ_URL))
        assert ui_utils(self.web_session).waitForTextOnPage("Middleware Providers", 15)
        while True:
            if self.web_driver.find_element_by_xpath("//strong[contains(.,'No Records Found.')]").is_displayed():
                self.web_session.logger.info("All the middleware providers are deleted successfully.")
                break
            else:
                self.web_driver.refresh()
                ui_utils(self.web_session).sleep(5)
        return True
