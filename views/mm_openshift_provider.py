from common.ui_utils import ui_utils
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from hawkular.hawkular_api import hawkular_api
from common.view import view
from common.db import db
from common.openshift_utils import openshift_utils
import time
from common.timeout import timeout

class mm_openshift_providers():
    web_session = None
    MIQ_BASE_VERSION = "master"
    ui_utils = None

    def __init__(self, web_session):
        self.web_session = web_session
        self.web_driver = web_session.web_driver
        self.ui_utils = ui_utils(self.web_session)
        self.openshift_utils= openshift_utils(self.web_session)

    def add_mm_openshift_provider(self, delete_if_provider_present=True, port=None, validate_provider=True):
        self.provider_name = self.web_session.OPENSHIFT_PROVIDER_NAME
        self.host_name = self.web_session.OPENSHIFT_HOSTNAME
        self.port = self.web_session.OPENSHIFT_PORT if port == None else port
        self.openshift_user = self.web_session.OPENSHIFT_USERNAME
        self.openshift_token= self.openshift_utils.get_token()
        ui_utils(self.web_session).sleep(2)

        # Check if any provider already exist. If exist, first delete all the providers and then add a provider.

        if self.does_provider_exist():
            self.web_session.logger.info("Middleware Provider already exist.")
            if delete_if_provider_present:
                self.delete_provider(delete_all_providers=True)
            else:
                return
        else:
            self.web_session.logger.info("Adding openshift Middleware Provider to ManageIQ instance")

        self.web_session.web_driver.get("{}//ems_container/show_list".format(self.web_session.MIQ_URL))
        assert ui_utils(self.web_session).waitForTextOnPage("Containers Providers", 15)

        self.web_driver.find_element_by_xpath("//button[@title='Configuration']").click()
        self.ui_utils.waitForElementOnPage(By.XPATH,"//a[@title='Add a new Containers Provider']", 5)
        elem_add_new_provider = self.web_driver.find_element_by_xpath("//a[@title='Add a new Containers Provider']")
        elem_add_new_provider.click()
        self.web_driver.implicitly_wait(15)
        assert ui_utils(self.web_session).waitForTextOnPage("Add New Containers Provider", 50)
        ui_utils(self.web_session).sleep(2)

        self.web_session.logger.info("The appliance version in use is: {} ".format(self.web_session.appliance_version))

        self.submit_provider_form_cfme(validate_provider)
        self.verify_add_provider_success()


    def submit_provider_form_cfme(self, validate_provider=True):
        # Enter the form details and submit if the appliance version is CFME Downstream

        self.web_driver.find_element_by_xpath("//input[@id='ems_name']").send_keys(self.provider_name)
        self.web_driver.find_element_by_xpath("//button[contains(.,'<Choose>')]").click()
        assert ui_utils(self.web_session).waitForTextOnPage("OpenShift", 15)
        self.web_driver.find_element_by_xpath("//a[contains(.,'OpenShift')]").click()
        self.web_driver.find_element_by_xpath("//input[@id='default_hostname']").send_keys(self.host_name)

        # self.web_driver.find_element_by_xpath("//input[@id='default_api_port']").send_keys(self.port)

        self.web_driver.find_element_by_xpath("//button[@data-id='default_security_protocol']").click()
        assert ui_utils(self.web_session).waitForTextOnPage("SSL without validation", 15)
        self.web_driver.find_element_by_xpath("//a[contains(.,'SSL without validation')]").click()

        self.web_driver.find_element_by_xpath("//input[@id='default_password']").send_keys(self.openshift_token)


        if validate_provider:
            self.validate_provider()
        self.save_provider()


    def does_provider_exist(self):
        self.web_session.logger.info("Checking if provider exists")

         # For performance reasons, check if the provider is present via DB
        providers = db(self.web_session).get_providers()
        provider = ui_utils(self.web_session).find_row_in_list(providers, 'name', self.web_session.OPENSHIFT_PROVIDER_NAME)
        if provider:
            return True
        else:
            return False


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
        el = self.web_driver.find_element_by_xpath("//a[@id='ems_container_vmdb_choice__ems_container_refresh']")
        assert self.ui_utils.wait_until_element_displayed(el, 5)
        el.click()
        ui_utils(self.web_session).accept_alert(10)
        ui_utils(self.web_session).waitForTextOnPage("Refresh Provider initiated", 15)

    def validate_providers_list(self):

        # Test to validate provider list page in UI and validate matching providers hostname, port number

        self.web_session.logger.info("Begin providers list test.")
        self.web_session.web_driver.get("{}//ems_container/show_list".format(self.web_session.MIQ_URL))
        providers_ui = self.ui_utils.get_list_table()
        assert len(providers_ui) > 0, "Providers list is empty."

        for prov_ui in providers_ui:

            if prov_ui.get('Name') == self.web_session.OPENSHIFT_PROVIDER_NAME:
               assert (prov_ui.get('Hostname') == self.web_session.OPENSHIFT_HOSTNAME), "Hostname mismatch"
               assert (prov_ui.get('Port') == self.web_session.OPENSHIFT_PORT), "Port Number mismatch"

            return True

    def verify_add_provider_success(self):

            assert ui_utils(self.web_session).waitForTextOnPage(
                'Containers Providers "{}" was saved'.format(self.provider_name), 90)

            if ui_utils(self.web_session).isElementPresent(By.XPATH, "//a[contains(@title,'Name: {}')]".format(
                    self.provider_name)):
                self.web_session.logger.info("Container Provider added successfully.")

            # Navigate to the provider details page and check if the last refresh status is - Success.

            view(self.web_session).list_View()
            assert ui_utils(self.web_session).waitForTextOnPage(self.web_session.OPENSHIFT_PROVIDER_NAME, 30)
            ui_utils(self.web_session).click_on_row_containing_text(self.web_session.OPENSHIFT_PROVIDER_NAME)

            assert ui_utils(self.web_session).waitForTextOnPage("Status", 30)

    def validate_provider(self):
        validate = WebDriverWait(self.web_driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Validate')]")))
        validate.click()
        assert ui_utils(self.web_session).waitForTextOnPage('Credential validation was successful', 60)

    def save_provider(self):

        if str(self.web_session.appliance_version) != '5.7*':
            xpath = "//button[contains(text(),'Add')]"
        else:
             xpath = "//button[contains(@ng-click,'addClicked($event, true)')]"

        with timeout(seconds=15, error_message="Timed out waiting for Save."):
            while True:
                WebDriverWait(self.web_driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
                self.web_driver.find_element_by_xpath(xpath).click()
                if (self.ui_utils.isTextOnPage(" was saved")):
                    self.web_session.logger.info("Provider saved.")
                    break;
                else:
                    self.web_session.logger.info("No Provider save message.")

                time.sleep(1)


    def add_provider_invalid_port(self):
        if self.does_provider_exist():
            self.web_session.logger.info("Container Provider exist - Delete the provider.")
            self.delete_provider(delete_all_providers=True)

        try:
            self.add_provider(port="1234")
            raise Exception('Add Provider Unexpectedly passed.')
        except:
            # Expected timeout waiting for form Add button to be clickable, since button should not be clickable.
            pass

        return True;
