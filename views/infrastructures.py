from common.ui_utils import ui_utils
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from common.db import db
from views.provider_base import provider_base
import common.view as view

class infrastructures(provider_base):

    def __init__(self, web_session, provider_type = "infrastructure", provider_type_name = "Infrastructure", provider_url_part = "ems_infra", provider_db_name="Infra"):
        super(infrastructures, self).__init__(web_session, provider_type=provider_type, provider_type_name=provider_type_name, provider_url_part=provider_url_part, provider_db_name=provider_db_name)

    def add_provider(self, delete_if_provider_present=True, validate_provider=True):
        # here pass parameters that are needed at add provider view
        self.provider_name = self.web_session.INFRA_PROVIDER_NAME
        # pass to this class instance default endpoint creds
        self.infra_default_host_name = self.web_session.INFRA_DEFAULT_HOSTNAME
        self.infra_default_port = self.web_session.INFRA_DEFAULT_PORT
        self.infra_default_user = self.web_session.INFRA_DEFAULT_USERNAME
        self.infra_default_password = self.web_session.INFRA_DEFAULT_PASSWORD

        # pass to this class instance c&u endpoint creds
        self.infra_metrics_host_name = self.web_session.INFRA_METRICS_HOSTNAME
        self.infra_metrics_port = self.web_session.INFRA_METRICS_PORT
        self.infra_metrics_user = self.web_session.INFRA_METRICS_USERNAME
        self.infra_metrics_password = self.web_session.INFRA_METRICS_PASSWORD

        # call the rest in parent method
        super(infrastructures, self).add_provider(delete_if_provider_present, validate_provider)

    def submit_provider_form_cfme(self, validate_provider=True):
        # Enter the form details and submit if the appliance version is CFME Downstream

        self.web_driver.find_element_by_xpath("//button[@data-id='emstype']").click()
        assert ui_utils(self.web_session).waitForTextOnPage("Red Hat Virtualization", 30)
        self.web_driver.find_element_by_xpath("//span[contains(.,'Red Hat Virtualization')]").click()
        assert ui_utils(self.web_session).waitForTextOnPage("Red Hat Virtualization", 30)

        self.web_driver.find_element_by_xpath("//input[@id='ems_name']").send_keys(self.provider_name)
        self.web_driver.find_element_by_xpath("//input[@id='default_hostname']").send_keys(self.infra_default_host_name)
        self.web_driver.find_element_by_xpath("//input[@id='default_api_port']").clear()
        self.web_driver.find_element_by_xpath("//input[@id='default_api_port']").send_keys(self.infra_default_port)

        # disable Verify TLS Certificate - default Yes
        self.web_driver.find_element_by_xpath("//div/div/input[@id='default_tls_verify']/../..").click()
        assert ui_utils(self.web_session).waitForElementOnPage(By.XPATH, "//input[@id='default_tls_verify' and contains(@class,'ng-empty')]", 30)

        self.web_driver.find_element_by_xpath(
            """//*[contains(@ng-show,"emsCommonModel.emstype != 'azure'")]//input[@id='default_userid']"""
        ).send_keys(self.infra_default_user)
        self.web_driver.find_element_by_xpath(
            """//*[contains(@ng-show,"emsCommonModel.emstype != 'azure'")]//input[@id='default_password']"""
            ).send_keys(
            self.infra_default_password)

        if not self.MIQ_BASE_VERSION == self.appliance_version:
            self.web_driver.find_element_by_xpath(
                """//*[contains(@ng-show,"emsCommonModel.emstype != 'azure'")]//input[@id='default_verify']"""
            ).send_keys(self.infra_default_password)

        if validate_provider:
            self.validate_provider()

        # add c&u db endpoint - metrics
        self.web_driver.find_element_by_xpath("id('metrics_tab')").click()
        assert ui_utils(self.web_session).waitForElementOnPage(By.XPATH, "//input[@id='metrics_hostname']", 30)

        self.web_driver.find_element_by_xpath("//input[@id='metrics_hostname']").send_keys(self.infra_metrics_host_name)
        self.web_driver.find_element_by_xpath("//input[@id='metrics_api_port']").clear()
        self.web_driver.find_element_by_xpath("//input[@id='metrics_api_port']").send_keys(self.infra_metrics_port)

        self.web_driver.find_element_by_xpath(
            """//*[contains(@ng-show,"emsCommonModel.emstype != 'azure'")]//input[@id='metrics_userid']"""
        ).send_keys(self.infra_metrics_user)
        self.web_driver.find_element_by_xpath(
            """//*[contains(@ng-show,"emsCommonModel.emstype != 'azure'")]//input[@id='metrics_password']"""
        ).send_keys(
            self.infra_metrics_password)

        if not self.MIQ_BASE_VERSION == self.appliance_version:
            self.web_driver.find_element_by_xpath(
                """//*[contains(@ng-show,"emsCommonModel.emstype != 'azure'")]//input[@id='metrics_verify']"""
            ).send_keys(self.infra_metrics_password)

        if validate_provider:
            self.validate_provider(endpoint="metrics")

        self.save_provider()

    def update_provider(self, add_provider=True):
        super(infrastructures, self).update_provider(add_provider)

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

    name_suffix = "-s"

    def edit_provider_form_cfme_newvalues(self):

        self.web_driver.find_element_by_xpath("//input[@id='ems_name']").clear()
        self.web_driver.find_element_by_xpath("//input[@id='ems_name']").send_keys(self.provider_name + self.name_suffix)

    def verify_edit_provider_success_newvalues(self):

        # Verify if the provider name, is successfully updated and shown in UI
        view.view(self.web_session).list_View()
        assert ui_utils(self.web_session).isElementPresent(By.XPATH, "//td[contains(.,'{}')]".format(self.provider_name + self.name_suffix))
        self.web_session.logger.info("The middleware provider is edited successfully.")

    def edit_provider_form_cfme_originalvalues(self):

        # Edit and save the name to default value.( This will additionally check edit from the provider details page)

        self.web_session.web_driver.get("{}//ems_infra/show_list?type=list".format(self.web_session.MIQ_URL))
        ui_utils(self.web_session).click_on_row_containing_text(self.provider_name + self.name_suffix)

        self.web_driver.find_element_by_xpath("//button[@title='Configuration']").click()
        self.ui_utils.waitForElementOnPage(By.XPATH, "//a[@title='Edit this {} Provider']".format(self.provider_type_name), 5)
        self.web_driver.find_element_by_xpath("//a[@title='Edit this {} Provider']".format(self.provider_type_name)).click()
        ui_utils(self.web_session).sleep(15)
        assert ui_utils(self.web_session).waitForTextOnPage("Name", 30)

        self.web_driver.find_element_by_xpath("//input[@id='ems_name']").clear()
        self.web_driver.find_element_by_xpath("//input[@id='ems_name']").send_keys(self.provider_name)

    def verify_edit_provider_success_originalvalues(self):
        ui_utils(self.web_session).waitForElementOnPage(By.XPATH, self.summary_xpath, 30)
        self.web_driver.find_element_by_xpath(self.summary_xpath).click()
        assert ui_utils(self.web_session).isElementPresent(By.XPATH, "//*[contains(.,'{}')]".format(
            self.provider_name))
        self.web_session.logger.info("The infrastructure provider is edited to the original values successfully.")

    def verify_refresh_status_success(self):
        refresh_value_success = "Success"

        self.refresh_provider()

        # Refresh the page till till the table value for Last Refresh shows the value - Success
        ui_utils(self.web_session).waitForElementOnPage(By.XPATH, self.summary_xpath, 30)
        self.web_driver.find_element_by_xpath(self.summary_xpath).click()

        assert self.wait_for_provider_refresh_status(refresh_value_success, 600)
        provider_details = ui_utils(self.web_session).get_generic_table_as_dict()

        # Verify if the 'Last Refresh' value from table contains 'Success:
        refresh_status = provider_details.get("Last Refresh")

        if str(refresh_status).__contains__(refresh_value_success):
            self.web_session.logger.info("The Last refresh status is - " + refresh_status)
            return True
        else:
            return False

    refresh_provider_id = "ems_infra_vmdb_choice__ems_infra_refresh"

    def validate_providers_list_asserts(self, prov_ui):
        # override
        assert (prov_ui.get('Hostname') == self.infra_default_host_name), "Hostname mismatch"
        return

    recheck_auth_id="ems_infra_authentication_choice__ems_infra_recheck_auth_status"

    def validate_provider(self, endpoint="default"):
        # overriden because 2 endpoints
        validate = WebDriverWait(self.web_driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, """//*[contains(@ng-show,"emsCommonModel.emstype != 'azure'")]//div[@id='"""+endpoint+"""']//button[@title='Validate the credentials by logging into the Server']""")))
        validate.click()
        assert ui_utils(self.web_session).waitForTextOnPage('Credential validation was successful', 60)

    def navigate_to_vm_view(self):
        # navigate to VM
        providers = db(self.web_session).get_providers("InfraManager")
        provider = ui_utils(self.web_session).find_row_in_list(providers, 'name', self.provider_name)

        if provider:
            self.web_session.web_driver.get("{}//ems_infra/{}?display=vms&type=list".format(self.web_session.MIQ_URL, str(provider[0])))
            # click the vm by its name INFRA_TEST_VM_NAME
            ui_utils(self.web_session).click_on_row_containing_text(self.web_session.INFRA_TEST_VM_NAME)
            return True
        else:
            return False
