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
            self.web_session.logger.info("Openshift Provider already exist.")
            return

        self.web_session.logger.info("Adding openshift Provider to ManageIQ instance")

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

        if db(self.web_session).is_container_provider_present(self.provider_name):
            self.web_session.logger.info("Container Provider already exist.")
            return True
        else:
            self.web_session.logger.info("Adding Container Provider to ManageIQ instance")
            return False

    def delete_provider(self, delete_all_providers=True):

        self.web_session.web_driver.get("{}//ems_container/show_list".format(self.web_session.MIQ_URL))
        assert ui_utils(self.web_session).waitForTextOnPage("Containers Providers", 30)
        # self.ui_utils.sleep(15)

        # Delete the provider
        if delete_all_providers:
            self.clear_all_providers()
        else:
            self.delete_hawkular_provider()


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


