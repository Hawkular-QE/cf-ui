from common.ui_utils import ui_utils
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from navigation.navigation import NavigationTree
from selenium.webdriver.support import expected_conditions as EC
from parsing.table import table
from hawkular.hawkular_api import hawkular_api
from common.view import view
from common.db import db

class providers():
    web_session = None

    def __init__(self, web_session):
        self.web_session = web_session
        self.web_driver = web_session.web_driver
        self.hawkular_api = hawkular_api(self.web_session)

    def add_provider(self, delete_if_provider_present=True):
        self.provider_name = self.web_session.HAWKULAR_PROVIDER_NAME
        self.host_name = self.web_session.HAWKULAR_HOSTNAME
        self.port = self.web_session.HAWKULAR_PORT
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

        NavigationTree(self.web_session).navigate_to_middleware_providers_view()

        elem_config = self.web_driver.find_element_by_xpath("//button[@title='Configuration']")
        elem_config.click()
        assert ui_utils(self.web_session).waitForTextOnPage("Add a New Middleware Provider", 15)
        elem_add_new_provider = self.web_driver.find_element_by_xpath("//a[@title='Add a New Middleware Provider']")
        elem_add_new_provider.click()
        self.web_driver.implicitly_wait(15)
        assert ui_utils(self.web_session).waitForTextOnPage("Confirm Password", 15)

        # Enter the form details and submit to add the provider

        self.web_driver.find_element_by_xpath("//button[@data-id='server_emstype']").click()
        assert ui_utils(self.web_session).waitForTextOnPage("Hawkular", 30)
        self.web_driver.find_element_by_xpath("//span[contains(.,'Hawkular')]").click()
        assert ui_utils(self.web_session).waitForTextOnPage("Hostname or IP address", 30)

        # Enter the name of provider after selecting hawkular type from dropdown to take care of page load issues.

        elem_provider_name = self.web_driver.find_element_by_xpath("//input[@id='name']")
        elem_provider_name.send_keys(self.provider_name)

        elem_provider_hostname = self.web_driver.find_element_by_xpath("//input[@id='hostname']")
        elem_provider_hostname.send_keys(self.host_name)

        elem_provider_port = self.web_driver.find_element_by_xpath("//input[@id='port']")
        elem_provider_port.send_keys(self.port)
        elem_hawkular_user = self.web_driver.find_element_by_xpath("//input[@id='default_userid']")
        elem_hawkular_user.send_keys(self.hawkular_user)
        elem_hawkular_password = self.web_driver.find_element_by_xpath("//input[@id='default_password']")
        elem_hawkular_password.send_keys(self.hawkular_password)
        elem_hawkularVerify_password = self.web_driver.find_element_by_xpath("//input[@id='default_verify']")
        elem_hawkularVerify_password.send_keys(self.hawkular_password)
        self.web_driver.find_element_by_xpath("//button[@alt='Add this Middleware Provider']").click()

        assert ui_utils(self.web_session).waitForTextOnPage(
            'Middleware Providers "{}" was saved'.format(self.provider_name), 15)
        
        if ui_utils(self.web_session).isElementPresent(By.XPATH, "//a[contains(@title,'Name: {}')]".format(
                self.provider_name)):
            self.web_session.logger.info("Middleware Provider added successfully.")

        # Navigate to the provider details page and check if the last refresh status is - Success.

        view(self.web_session).list_View()
        assert ui_utils(self.web_session).waitForTextOnPage(self.web_session.HAWKULAR_PROVIDER_NAME, 15)
        ui_utils(self.web_session).click_on_row_containing_text(self.web_session.HAWKULAR_PROVIDER_NAME)

        assert ui_utils(self.web_session).waitForTextOnPage("Status", 15)

        assert self.verify_refresh_status_success(), "The last refresh status is not - Success"

    def delete_provider(self, delete_all_providers=True):
        NavigationTree(self.web_session).navigate_to_middleware_providers_view()
        assert ui_utils(self.web_session).waitForTextOnPage("Middleware Providers", 30)

        # Delete the provider
        if delete_all_providers:
            self.clear_all_providers()
        else:
            self.delete_hawkular_provider()

    def update_provider(self, add_provider=True):
        self.web_session.logger.info("Checking if provider exist and add if it does not.")
        if add_provider:
            self.add_provider(delete_if_provider_present=False)

        NavigationTree(self.web_session).navigate_to_middleware_providers_view()
        assert ui_utils(self.web_session).waitForTextOnPage("Middleware Providers", 30)
        self.web_driver.find_element_by_xpath("//input[contains(@type,'checkbox')]").click()
        self.web_driver.find_element_by_xpath("//button[@title='Configuration']").click()
        elem_editprovider_link = self.web_driver.find_element_by_xpath(
            "//a[contains(.,'Edit Selected Middleware Provider')]")
        elem_editprovider_link.click()
        assert ui_utils(self.web_session).waitForTextOnPage("Confirm Password", 30)

        self.web_driver.find_element_by_xpath("//input[@id='name']").clear()
        self.web_driver.find_element_by_xpath("//input[@id='name']").send_keys(self.web_session.PROVIDER)

        self.web_driver.find_element_by_xpath("//input[@id='hostname']").clear()
        self.web_driver.find_element_by_xpath("//input[@id='hostname']").send_keys("Demo.hawkular.org")

        self.web_driver.find_element_by_xpath("//input[@id='port']").clear()
        self.web_driver.find_element_by_xpath("//input[@id='port']").send_keys(8080)

        # Wait till Save button is enabled before click

        WebDriverWait(self.web_driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Save')]")))
        self.web_driver.find_element_by_xpath("//button[contains(.,'Save')]").click()

        assert ui_utils(self.web_session).waitForTextOnPage('Middleware Provider "{}" was saved'.format(self.web_session.PROVIDER), 15)

        # Verify if the provider name, hostname and port number is successfully updated and shown in UI

        assert ui_utils(self.web_session).isElementPresent(By.XPATH, "//td[contains(.,'{}')]".format(self.web_session.PROVIDER))
        assert ui_utils(self.web_session).isElementPresent(By.XPATH, "//td[contains(text(),'Demo')]")
        assert ui_utils(self.web_session).isElementPresent(By.XPATH, "//td[contains(.,'8080')]")
        self.web_session.logger.info("The middleware provider is edited successfully.")

        # Edit and save the name, port and number to default value.( This will additionally check edit from the provider details page)

        self.web_driver.find_element_by_xpath("//button[@title='Configuration']").click()
        self.web_driver.find_element_by_xpath("//a[@title='Edit this Middleware Provider']").click()
        assert ui_utils(self.web_session).waitForTextOnPage("Basic Information", 30)

        self.web_driver.find_element_by_xpath("//input[@id='name']").clear()
        self.web_driver.find_element_by_xpath("//input[@id='name']").send_keys(self.web_session.HAWKULAR_PROVIDER_NAME)

        self.web_driver.find_element_by_xpath("//input[@id='hostname']").clear()
        self.web_driver.find_element_by_xpath("//input[@id='hostname']").send_keys(self.web_session.HAWKULAR_HOSTNAME)

        self.web_driver.find_element_by_xpath("//input[@id='port']").clear()
        self.web_driver.find_element_by_xpath("//input[@id='port']").send_keys(self.web_session.HAWKULAR_PORT)

        # Wait till Save button is enabled before click

        WebDriverWait(self.web_driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Save')]")))
        self.web_driver.find_element_by_xpath("//button[contains(.,'Save')]").click()
        assert ui_utils(self.web_session).waitForTextOnPage(
            'Middleware Provider "{}" was saved'.format(self.web_session.HAWKULAR_PROVIDER_NAME), 15)

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

        # navigate_to_providers

        NavigationTree(self.web_session).navigate_to_middleware_providers_view()

        if ui_utils(self.web_session).isElementPresent(By.XPATH, "//span[contains(.,'(Item 0 of 0)')]"):
            self.web_session.logger.info("Middleware Provider does not exist.")
            return False
        else:
            self.web_session.logger.info("Middleware Provider already exist.")
            return True


    def delete_hawkular_provider(self):
        NavigationTree(self.web_session).navigate_to_middleware_providers_view()
        assert ui_utils(self.web_session).waitForTextOnPage("Middleware Providers", 30)
        self.web_session.logger.info("Deleting the provider- {}".format(self.web_session.HAWKULAR_HOSTNAME))
        self.web_driver.find_element_by_xpath("//input[contains(@type,'checkbox')]").click()
        self.web_driver.find_element_by_xpath("//button[@title='Configuration']").click()
        self.web_driver.find_element_by_xpath(
            "//a[@title='Remove selected Middleware Providers from the VMDB']").click()
        self.web_driver.switch_to_alert().accept()
        assert ui_utils(self.web_session).waitForTextOnPage("Delete initiated", 15)

        # Verify if the provider is deleted from the provider list.

        assert ui_utils(self.web_session).waitForElementOnPage(By.XPATH, "//a[@title='{}']".format(
            self.web_session.HAWKULAR_PROVIDER_NAME), 120, exist=False)
        if not ui_utils(self.web_session).isTextOnPage(self.web_session.HAWKULAR_PROVIDER_NAME):
            self.web_session.logger.info(
                "The provider - {} - is deleted successfully".format(self.web_session.HAWKULAR_HOSTNAME))

    def clear_all_providers(self):
        self.web_session.logger.info("Deleting all the providers from providers list.")
        self.web_driver.find_element_by_xpath("//input[@id='masterToggle']").click()
        self.web_driver.find_element_by_xpath("//button[@title='Configuration']").click()
        self.web_driver.find_element_by_xpath(
            "//a[@title='Remove selected Middleware Providers from the VMDB']").click()
        self.web_driver.switch_to_alert().accept()
        assert ui_utils(self.web_session).waitForTextOnPage(
            "Delete initiated", 15)

        assert ui_utils(self.web_session).refresh_until_text_appears("No Records Found", 300)
        self.web_session.logger.info("All the middleware providers are deleted successfully.")

    def verify_refresh_status_success(self):

        refresh_value_success = "Success"

        self.refresh_provider()

        # Refresh the page till till the table value for Last Refresh shows the value - Success

        assert ui_utils(self.web_session).refresh_until_text_appears(refresh_value_success, 300)
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
        self.web_driver.find_element_by_id('ems_middleware_vmdb_choice__ems_middleware_refresh').click()
        self.web_driver.switch_to_alert().accept()
        ui_utils(self.web_session).waitForTextOnPage("Refresh Provider initiated", 15)

    def validate_providers_list(self):

        # Test to validate provider list page in UI and validate matching providers hostname, port number

        self.web_session.logger.info("Begin providers list test.")
        NavigationTree(self.web_session).navigate_to_middleware_providers_view()
        providers_ui = table(self.web_session).get_middleware_providers_table()

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
        NavigationTree(self.web_session).navigate_to_middleware_providers_view()
        providers_ui = table(self.web_session).get_middleware_providers_table()
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
        assert providers_details_ui.get('Middleware Datasources') == str(len(datasources_hawk)), "Number of Datasources mismatch"

        return True

    def recheck_authentication(self):

        # Test for Authentication->Recheck Authentication' on hawkular provider

        self.web_session.logger.info("Begin test for Authentication->Recheck Authentication.")
        NavigationTree(self.web_session).navigate_to_middleware_providers_view()
        ui_utils(self.web_session).click_on_row_containing_text(self.web_session.HAWKULAR_PROVIDER_NAME)

        self.web_driver.find_element_by_id('ems_middleware_authentication_choice').click()
        self.web_driver.find_element_by_id('ems_middleware_authentication_choice__ems_middleware_recheck_auth_status').click()

        ui_utils(self.web_session).sleep(2)
        assert ui_utils(self.web_session).waitForTextOnPage("Authentication status will be saved and workers will be restarted for this Middleware Provider", 15)
        return True


    def add_wrong_provider_double_host(self):
        self.provider_name = self.web_session.HAWKULAR_PROVIDER_NAME
        self.host_name = self.web_session.HAWKULAR_HOSTNAME
        self.port = self.web_session.HAWKULAR_PORT
        self.hawkular_user = self.web_session.HAWKULAR_USERNAME
        self.hawkular_password = self.web_session.HAWKULAR_PASSWORD

        NavigationTree(self.web_session).jump_to_middleware_providers_view().select_and_click('Configuration', 'Add a New Middleware Provider')
        self.web_driver.implicitly_wait(5)

        self.web_driver.find_element_by_xpath("//button[@data-id='server_emstype']").click()
        assert ui_utils(self.web_session).waitForTextOnPage("Hawkular", 30)
        self.web_driver.find_element_by_xpath("//span[contains(.,'Hawkular')]").click()
        assert ui_utils(self.web_session).waitForTextOnPage("Hostname or IP address", 30)

        # Enter the name of provider after selecting hawkular type from dropdown to take care of page load issues.

        elem_provider_name = self.web_driver.find_element_by_xpath("//input[@id='name']")
        elem_provider_name.send_keys(self.provider_name)

        elem_provider_hostname = self.web_driver.find_element_by_xpath("//input[@id='hostname']")
        elem_provider_hostname.send_keys(self.host_name)

        elem_provider_port = self.web_driver.find_element_by_xpath("//input[@id='port']")
        elem_provider_port.send_keys(self.port)
        elem_hawkular_user = self.web_driver.find_element_by_xpath("//input[@id='default_userid']")
        elem_hawkular_user.send_keys(self.hawkular_user)
        elem_hawkular_password = self.web_driver.find_element_by_xpath("//input[@id='default_password']")
        elem_hawkular_password.send_keys(self.hawkular_password)
        elem_hawkularVerify_password = self.web_driver.find_element_by_xpath("//input[@id='default_verify']")
        elem_hawkularVerify_password.send_keys(self.hawkular_password)
        self.web_driver.find_element_by_xpath("//button[@alt='Add this Middleware Provider']").click()

        if self.web_driver.find_element_by_xpath("//strong[contains(.,'Host Name has already been taken')]"):
            raise ValueError("Exception: provider already exists!")

    def add_wrong_provider_missed_type(self):
        self.provider_name = self.web_session.HAWKULAR_PROVIDER_NAME
        self.host_name = self.web_session.HAWKULAR_HOSTNAME
        self.port = self.web_session.HAWKULAR_PORT
        self.hawkular_user = self.web_session.HAWKULAR_USERNAME
        self.hawkular_password = self.web_session.HAWKULAR_PASSWORD

        NavigationTree(self.web_session).jump_to_middleware_providers_view().select_and_click('Configuration', 'Add a New Middleware Provider')
        self.web_driver.implicitly_wait(5)

        elem_provider_name = self.web_driver.find_element_by_xpath("//input[@id='name']")
        elem_provider_name.send_keys(self.provider_name)

        elem_hawkular_user = self.web_driver.find_element_by_xpath("//input[@id='default_userid']")
        elem_hawkular_user.send_keys(self.hawkular_user)
        elem_hawkular_password = self.web_driver.find_element_by_xpath("//input[@id='default_password']")
        elem_hawkular_password.send_keys(self.hawkular_password)
        elem_hawkularVerify_password = self.web_driver.find_element_by_xpath("//input[@id='default_verify']")
        elem_hawkularVerify_password.send_keys(self.hawkular_password)
        self.web_driver.find_element_by_xpath("//button[@alt='Add this Middleware Provider']").click()
        if self.web_driver.find_element_by_xpath("//strong[contains(.,'Type is required')]"):
            raise ValueError("Exception: Type of provider should be choosen!")



    def add_wrong_provider_missed_everything(self):
        self.provider_name = self.web_session.HAWKULAR_PROVIDER_NAME
        self.host_name = self.web_session.HAWKULAR_HOSTNAME
        self.port = self.web_session.HAWKULAR_PORT
        self.hawkular_user = self.web_session.HAWKULAR_USERNAME
        self.hawkular_password = self.web_session.HAWKULAR_PASSWORD

        NavigationTree(self.web_session).jump_to_middleware_providers_view().select_and_click('Configuration', 'Add a New Middleware Provider')
        self.web_driver.implicitly_wait(5)
        self.web_driver.find_element_by_xpath("//button[@alt='Add this Middleware Provider']").click()

        if self.web_driver.find_element_by_xpath("//strong[contains(.,'Type is required')]"):
            raise ValueError("Exception: Type of provider should be choosen!")



    def add_wrong_provider(self):
        self.web_session.logger.info("Wrong attempt to add Middleware Provider.")
        self.provider_name = self.web_session.HAWKULAR_PROVIDER_NAME
        self.host_name = self.web_session.HAWKULAR_HOSTNAME

        self.port = self.web_session.HAWKULAR_PORT + '100'
        print "Actual port number=", self.port

        self.hawkular_user = self.web_session.HAWKULAR_USERNAME
        self.hawkular_password = self.web_session.HAWKULAR_PASSWORD

        NavigationTree(self.web_session).jump_to_middleware_providers_view().select_and_click('Configuration', 'Add a New Middleware Provider')
        self.web_driver.implicitly_wait(5)

        # Enter the form details and submit to add the provider

        self.web_driver.find_element_by_xpath("//button[@data-id='server_emstype']").click()
        assert ui_utils(self.web_session).waitForTextOnPage("Hawkular", 30)
        self.web_driver.find_element_by_xpath("//span[contains(.,'Hawkular')]").click()
        assert ui_utils(self.web_session).waitForTextOnPage("Hostname or IP address", 30)

        # Enter the name of provider after selecting hawkular type from dropdown to take care of page load issues.

        elem_provider_name = self.web_driver.find_element_by_xpath("//input[@id='name']")
        elem_provider_name.send_keys(self.provider_name)

        elem_provider_hostname = self.web_driver.find_element_by_xpath("//input[@id='hostname']")
        elem_provider_hostname.send_keys(self.host_name)

        elem_provider_port = self.web_driver.find_element_by_xpath("//input[@id='port']")
        elem_provider_port.send_keys(self.port)
        elem_hawkular_user = self.web_driver.find_element_by_xpath("//input[@id='default_userid']")
        elem_hawkular_user.send_keys(self.hawkular_user)
        elem_hawkular_password = self.web_driver.find_element_by_xpath("//input[@id='default_password']")
        elem_hawkular_password.send_keys(self.hawkular_password)
        elem_hawkularVerify_password = self.web_driver.find_element_by_xpath("//input[@id='default_verify']")
        elem_hawkularVerify_password.send_keys(self.hawkular_password)
        self.web_driver.find_element_by_xpath("//button[@alt='Add this Middleware Provider']").click()

        assert ui_utils(self.web_session).waitForTextOnPage(
            'Middleware Providers "{}" was saved'.format(self.provider_name), 15)

        if ui_utils(self.web_session).isElementPresent(By.XPATH, "//a[contains(@title,'Name: {}')]".format(
                self.provider_name)):
            self.web_session.logger.info("Middleware Provider added successfully.")

        # Navigate to the provider details page and check if the last refresh status is - Success.

        view(self.web_session).list_View()
        assert ui_utils(self.web_session).waitForTextOnPage(self.web_session.HAWKULAR_PROVIDER_NAME, 15)
        ui_utils(self.web_session).click_on_row_containing_text(self.web_session.HAWKULAR_PROVIDER_NAME)

        assert ui_utils(self.web_session).waitForTextOnPage("Status", 15)

        assert self.verify_refresh_status_success(), "The last refresh status is not - Success"


