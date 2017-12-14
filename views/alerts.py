from common.ui_utils import ui_utils
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from common.navigate import navigate

'''

Created on December 1st

@author: gbaufake

'''

class alerts:
    web_session = None

    def __init__(self, web_session):
        self.web_session = web_session
        self.web_driver = webdriver
        self.ui_utils = ui_utils(web_session)

    def add_alert(self, alert):
        self.navigate_all_alerts()
        self.ui_utils.sleep(1)

        self.web_session.web_driver.find_element_by_xpath("//div[@id='treeview-alert_tree']/ul/li").click()
        self.ui_utils.sleep(1)

        self.web_session.web_driver.find_element_by_xpath("//button[@title='Configuration']").click()
        self.ui_utils.sleep(5)

        self.web_session.web_driver.find_element_by_xpath("//a[@title='Add a New Alert']").click()
        assert self.ui_utils.waitForTextOnPage("Adding a new Alert", 90)

        self.fill_form(alert)
        self.web_session.web_driver.find_element_by_xpath("//*[@id=\"buttons_on\"]/button[1]").click()
        assert self.ui_utils.waitForTextOnPage('Alert "{}" was added'.format(alert.description), 60)
        self.web_session.logger.info("The alert of category: {} is added successfully.".format(alert.category_description()))

        return True

    def clear_fields(self, alert):
        self.web_session.web_driver.find_element_by_xpath("//input[@id='description']").clear()
        for field in alert.fields_for_ui():
            self.web_session.web_driver.find_element_by_id(field[0]).clear()

    def fill_form(self, alert, new_form=True):
        # Select Middleware
        Select(self.web_session.web_driver.find_element_by_id("miq_alert_db")).select_by_visible_text(
            "Middleware Server")
        self.ui_utils.sleep(2)
        # Category of Alert
        Select(self.web_session.web_driver.find_element_by_id("exp_name")).select_by_value(alert.category_value())

        self.ui_utils.sleep(1)
        # Severity
        Select(self.web_session.web_driver.find_element_by_id("miq_alert_severity")).select_by_visible_text("Info")
        self.ui_utils.sleep(1)

        if new_form:
            # Show in Timeline
            self.web_session.web_driver.find_element_by_id("send_evm_event_cb").click()
            self.ui_utils.sleep(1)


        # Sending Tuple
        for field in alert.fields_for_ui():
            self.web_session.web_driver.find_element_by_id(field[0]).send_keys(str(field[1]))
        self.ui_utils.sleep(1)
        # Notification Frequency
        Select(self.web_session.web_driver.find_element_by_id("repeat_time")).select_by_visible_text("1 Minute")

        if alert.operator() != None:
            Select(self.web_session.web_driver.find_element_by_id("select_mw_operator")).select_by_visible_text(
                alert.operator())
        else:
            self.web_session.logger.info("Nothing to do here")
        self.ui_utils.sleep(1)
        # Description
        self.web_session.web_driver.find_element_by_xpath("//input[@id='description']").send_keys(
            alert.description)
        self.ui_utils.sleep(1)

    def edit_alert(self, alert1, alert2):

        self.navigate_all_alerts()

        self.ui_utils.sleep(1)

        self.ui_utils.get_list_table_as_elements()
        element = self.ui_utils.get_elements_containing_text(alert1.description)
        if element:
            element[0].click()
            assert self.ui_utils.waitForTextOnPage('Alert "{}"'.format(alert1.description), 90)
            self.ui_utils.sleep(1)
            self.web_session.web_driver.find_element_by_xpath("//button[@title='Configuration']").click()
            self.web_session.web_driver.find_element_by_xpath("//a[@id='miq_alert_vmdb_choice__alert_edit']").click()

            assert self.ui_utils.waitForTextOnPage("Editing Alert", 90)
            self.clear_fields(alert2)
            self.fill_form(alert2, new_form=False)
            self.web_session.web_driver.find_element_by_xpath("//button[contains(.,'Save')]").click()
            assert self.ui_utils.waitForTextOnPage('Alert "{}" was saved'.format(alert2.description), 10)
            return True
        else:
            return False

    def remove_alert(self,alert):

        self.navigate_all_alerts()

        self.ui_utils.sleep(1)

        self.ui_utils.get_list_table_as_elements()
        element = self.ui_utils.get_elements_containing_text(alert.description)
        if element:
            element[0].click()
            assert self.ui_utils.waitForTextOnPage('Alert "{}"'.format(alert.description), 90)
            self.ui_utils.sleep(1)
            self.web_session.web_driver.find_element_by_xpath("//button[@title='Configuration']").click()
            self.web_session.web_driver.find_element_by_id("miq_alert_vmdb_choice__alert_delete").click()
            self.ui_utils.accept_alert(20)
            assert self.ui_utils.waitForTextOnPage('Alert "{}": Delete successful'.format(alert.description), 5)
            self.web_session.logger.info(
                "The alert of category: {} is removed successfully.".format(alert.category_description()))

        return True

    def navigate_all_alerts(self):
        navigate(self.web_session).get("{}/miq_policy/explorer".format(self.web_session.MIQ_URL))
        self.ui_utils.sleep(5)
        if not self.web_session.web_driver.find_element_by_xpath("//*[@id='alert_accord']").is_displayed():
            self.web_session.web_driver.find_element_by_xpath("//a[contains(text(),'Alerts')]").click()

    def copy_alert(self,alert, copied_alert):
        self.navigate_all_alerts()

        element = self.ui_utils.get_elements_containing_text(alert.description)
        if element:
            element[0].click()
            self.ui_utils.sleep(1)
            self.web_session.web_driver.find_element_by_xpath("//button[@title='Configuration']").click()
            self.web_session.web_driver.find_element_by_xpath("//a[@id='miq_alert_vmdb_choice__alert_copy']").click()
            self.ui_utils.accept_alert(30)
            self.ui_utils.sleep(5)
            self.web_session.web_driver.find_element_by_xpath("//input[@id='description']").clear()
            self.web_session.web_driver.find_element_by_xpath("//input[@id='description']").send_keys(copied_alert.description)
            self.web_session.web_driver.find_element_by_xpath(".//*[@id='buttons_on']/button[1]").click()
            assert self.ui_utils.waitForTextOnPage('Alert "{}" was added'.format(copied_alert.description), 20)
            self.web_session.logger.info(
                "The alert of category: {} is copied successfully.".format(alert.category_description()))
            return True
        else:
            return False