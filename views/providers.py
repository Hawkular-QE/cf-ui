from common.ui_utils import ui_utils
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from navigation.navigation import NavigationTree
from selenium.webdriver.support import expected_conditions as EC

class providers():
    web_session = None

    def __init__(self, web_session):
        self.web_session = web_session
        self.web_driver = web_session.web_driver

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
        elem_provider = self.web_driver.find_element_by_xpath(
            "//a[contains(@title,'Name: {}')]".format(self.provider_name))

        if ui_utils(self.web_session).isElementPresent(By.XPATH, "//a[contains(@title,'Name: {}')]".format(
                self.provider_name)):
            self.web_session.logger.info("Middleware Provider added successfully.")

        # Navigate to the provider details page and check if the last refresh status is - Success.

        self.web_driver.find_element_by_xpath(
            "//a[@title='{}']".format(self.web_session.HAWKULAR_PROVIDER_NAME)).click()
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
        self.web_driver.find_element_by_xpath("//input[@id='name']").send_keys("Test_Provider")

        self.web_driver.find_element_by_xpath("//input[@id='hostname']").clear()
        self.web_driver.find_element_by_xpath("//input[@id='hostname']").send_keys("Demo.hawkular.org")

        self.web_driver.find_element_by_xpath("//input[@id='port']").clear()
        self.web_driver.find_element_by_xpath("//input[@id='port']").send_keys(8080)

        # Wait till Save button is enabled before click

        WebDriverWait(self.web_driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Save')]")))
        self.web_driver.find_element_by_xpath("//button[contains(.,'Save')]").click()

        assert ui_utils(self.web_session).waitForTextOnPage('Middleware Provider "Test_Provider" was saved', 15)

        # Verify if the provider name, hostname and port number is successfully updated and shown in UI

        assert ui_utils(self.web_session).isElementPresent(By.XPATH, "//td[contains(.,'Test_Provider')]")
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

        # Verify if the provider is deleted from the provider list by refreshing the page.

        count = 0
        while ui_utils(self.web_session).isElementPresent(By.XPATH, "//a[contains(@title,'Name: {}')]".format(
                self.web_session.HAWKULAR_PROVIDER_NAME)) and count < 10:
            self.web_driver.refresh()
            count += 1
        assert WebDriverWait(self, 10).until(lambda s: not ui_utils(self.web_session).isElementPresent(By.XPATH,
                                                                                                       "//a[contains(@title,'Name: {}')]".format(
                                                                                                           self.web_session.HAWKULAR_PROVIDER_NAME)))
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
            "Delete initiated for 1 Middleware Provider from the CFME Database", 15)

        count = 0
        while not ui_utils(self.web_session).isElementPresent(By.XPATH,
                                                              "//span[contains(.,'(Item 0 of 0)')]") and count < 10:
            self.web_driver.refresh()
            count += 1
        assert ui_utils(self.web_session).waitForTextOnPage("No Records Found", 15)
        self.web_session.logger.info("All the middleware providers are deleted successfully.")

    def verify_refresh_status_success(self):

        count = 0
        while ui_utils(self.web_session).isTextOnPage("Never") and count < 10:
            self.web_driver.refresh()
            count += 1

        if ui_utils(self.web_session).isTextOnPage("Success"):
            self.web_session.logger.info("The last refresh status is: Success ")
            return True
        else:
            return False


