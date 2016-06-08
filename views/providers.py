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
        self.providerName = self.web_session.HAWKULAR_PROVIDER_NAME
        self.hostName = self.web_session.HAWKULAR_HOSTNAME
        self.port = self.web_session.HAWKULAR_PORT
        self.hawkularUser = self.web_session.HAWKULAR_USERNAME
        self.hawkularPassword = self.web_session.HAWKULAR_PASSWORD

        # Check if the provider already exist. If exist, first delete the provider and then add it.

        if self.does_provider_exist():
            self.web_session.logger.info("Middleware Provider already exist.")
            if delete_if_provider_present:
                self.delete_provider()
            else:
                return
        else:
            self.web_session.logger.info("Adding Middleware Provider to ManageIQ instance")

        elem_config = self.web_driver.find_element_by_xpath("//button[@title='Configuration']")
        elem_config.click()
        assert ui_utils(self.web_session).waitForTextOnPage("Add a New Middleware Provider", 15)
        elem_addNewProvider = self.web_driver.find_element_by_xpath("//a[@title='Add a New Middleware Provider']")
        elem_addNewProvider.click()
        self.web_driver.implicitly_wait(15)
        assert ui_utils(self.web_session).waitForTextOnPage("Confirm Password", 15)

        # Enter the form details and submit to add the provider

        self.web_driver.find_element_by_xpath("//button[@data-id='server_emstype']").click()
        assert ui_utils(self.web_session).waitForTextOnPage("Hawkular", 30)
        self.web_driver.find_element_by_xpath("//span[contains(.,'Hawkular')]").click()
        assert ui_utils(self.web_session).waitForTextOnPage("Hostname or IP address", 30)

        # Enter the name of provider after selecting hawkular type from dropdown to take care of page load issues.

        elem_providerName = self.web_driver.find_element_by_xpath("//input[@id='name']")
        elem_providerName.send_keys(self.providerName)

        elem_providerHostname = self.web_driver.find_element_by_xpath("//input[@id='hostname']")
        elem_providerHostname.send_keys(self.hostName)

        elem_providerPort = self.web_driver.find_element_by_xpath("//input[@id='port']")
        elem_providerPort.send_keys(self.port)
        elem_hawkularUser = self.web_driver.find_element_by_xpath("//input[@id='default_userid']")
        elem_hawkularUser.send_keys(self.hawkularUser)
        elem_hawkularPassword = self.web_driver.find_element_by_xpath("//input[@id='default_password']")
        elem_hawkularPassword.send_keys(self.hawkularPassword)
        elem_hawkularVerifyPassword = self.web_driver.find_element_by_xpath("//input[@id='default_verify']")
        elem_hawkularVerifyPassword.send_keys(self.hawkularPassword)
        self.web_driver.find_element_by_xpath("//button[@alt='Add this Middleware Provider']").click()

        assert ui_utils(self.web_session).waitForTextOnPage(
            'Middleware Providers "{}" was saved'.format(self.providerName), 15)
        elem_provider = self.web_driver.find_element_by_xpath(
            "//a[contains(@title,'Name: {}')]".format(self.providerName))

        if ui_utils(self.web_session).isElementPresent(By.XPATH, "//a[contains(@title,'Name: {}')]".format(
                self.providerName)):
            self.web_session.logger.info("Middleware Provider added successfully.")


    def delete_provider(self):

        NavigationTree(self.web_driver).navigate_to_middleware_providers_view()

        # Delete the provider

        self.web_session.logger.info("Deleting the provider")
        self.web_driver.find_element_by_xpath("//input[contains(@type,'checkbox')]").click()
        elem_config = self.web_driver.find_element_by_xpath("//button[@title='Configuration']")
        elem_config.click()
        elem_deleteProviderLink = self.web_driver.find_element_by_xpath(
            "//a[@title='Remove selected Middleware Providers from the VMDB']")
        elem_deleteProviderLink.click()
        self.web_driver.switch_to_alert().accept()
        assert ui_utils(self.web_session).waitForTextOnPage(
            "Delete initiated for 1 Middleware Provider from the CFME Database", 15)

        # Verify if the provider is deleted from the provider list by refreshing the page.

        self.web_driver.refresh()
        if ui_utils(self.web_session).isElementPresent(By.XPATH, "//a[contains(@title,'Name: {}')]".format(
                self.web_session.HAWKULAR_PROVIDER_NAME)):
            self.web_driver.implicitly_wait(30)
            self.web_driver.refresh()
        assert WebDriverWait(self, 10).until(lambda s: not ui_utils(self.web_session).isElementPresent(By.XPATH,
                                                                                                       "//a[contains(@title,'Name: {}')]".format(
                                                                                                           self.web_session.HAWKULAR_PROVIDER_NAME)))

    def update_provider(self, add_provider=True):
        self.web_session.logger.info("Checking if provider exist and add if it does not.")
        if (add_provider):
            self.add_provider(delete_if_provider_present=False)

        NavigationTree(self.web_driver).navigate_to_middleware_providers_view()
        self.web_driver.find_element_by_xpath("//input[contains(@type,'checkbox')]").click()
        self.web_driver.find_element_by_xpath("//button[@title='Configuration']").click()
        elem_editProviderLink = self.web_driver.find_element_by_xpath(
            "//a[contains(.,'Edit Selected Middleware Provider')]")
        elem_editProviderLink.click()
        assert ui_utils(self.web_session).waitForTextOnPage("Confirm Password", 30)

        self.web_driver.find_element_by_xpath("//input[@id='name']").clear()
        self.web_driver.find_element_by_xpath("//input[@id='name']").send_keys("Test_Provider")

        self.web_driver.find_element_by_xpath("//input[@id='hostname']").clear()
        self.web_driver.find_element_by_xpath("//input[@id='hostname']").send_keys("Demo.hawkular.org")

        self.web_driver.find_element_by_xpath("//input[@id='port']").clear()
        self.web_driver.find_element_by_xpath("//input[@id='port']").send_keys(8080)

        WebDriverWait(self.web_driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, "//button[contains(.,'Save')]")))
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

        WebDriverWait(self.web_driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, "//button[contains(.,'Save')]")))
        self.web_driver.find_element_by_xpath("//button[contains(.,'Save')]").click()
        assert ui_utils(self.web_session).waitForTextOnPage(
            'Middleware Provider "{}" was saved'.format(self.web_session.HAWKULAR_PROVIDER_NAME), 15)

        assert ui_utils(self.web_session).isElementPresent(By.XPATH, "//td[contains(.,'Hawkular-Provider')]")
        assert ui_utils(self.web_session).isElementPresent(By.XPATH, "//td[contains(.,'livingontheedge.hawkular.org')]")
        assert ui_utils(self.web_session).isElementPresent(By.XPATH, "//td[contains(.,'80')]")
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

        # navigate_to_providers (To be replaced with navigation method)

        NavigationTree(self.web_driver).navigate_to_middleware_providers_view()

        # is_provider_present (note: use ui_utils.isTextOnPage OR create new ui_utils.isElementPresent)
        self.existingProviderName = self.web_session.HAWKULAR_PROVIDER_NAME
        if ui_utils(self.web_session).isElementPresent(By.XPATH, "//a[contains(@title,'Name: {}')]".format(
                self.existingProviderName)):
            self.web_session.logger.info("Middleware Provider already exist.")
            return True
        else:
            self.web_session.logger.info("Middleware Provider does not exist.")
            return False
