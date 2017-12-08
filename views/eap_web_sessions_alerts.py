from common.ui_utils import ui_utils
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from common.navigate import navigate

'''

Created on December 1st

@author: gbaufake

'''

class eap_web_session_alerts:
    web_session = None

    def __init__(self, web_session, alert):
        self.web_session = web_session
        self.web_driver = webdriver
        self.alert = alert
        self.ui_utils = ui_utils(web_session)

    def add_alert(self):
        navigate(self.web_session).get("{}/miq_policy/explorer".format(self.web_session.MIQ_URL))

        self.ui_utils.sleep(2)

        if not self.web_session.web_driver.find_element_by_xpath("//*[@id='alert_accord']").is_displayed():
            self.web_session.web_driver.find_element_by_xpath("//a[contains(text(),'Alerts')]").click()


        self.web_session.web_driver.find_element_by_xpath("//div[@id='treeview-alert_tree']/ul/li").click()

        self.ui_utils.sleep(2)


        self.web_session.web_driver.find_element_by_xpath("//button[@title='Configuration']").click()

        self.web_session.web_driver.find_element_by_xpath("//a[@title='Add a New Alert']").click()
        assert self.ui_utils.waitForTextOnPage("Adding a new Alert", 90)

        # Show in Timeline
        self.web_session.web_driver.find_element_by_id("send_evm_event_cb").click()
        self.ui_utils.sleep(1)

        # Select Middleware
        Select(self.web_session.web_driver.find_element_by_id("miq_alert_db")).select_by_visible_text("Middleware Server")
        self.ui_utils.sleep(1)


        # Severity
        Select(self.web_session.web_driver.find_element_by_id("miq_alert_severity")).select_by_visible_text("Info")
        self.ui_utils.sleep(1)


        # Category of Alert
        Select(self.web_session.web_driver.find_element_by_id("exp_name")).select_by_visible_text(self.alert.category)
        self.ui_utils.sleep(1)


        # Description
        self.web_session.web_driver.find_element_by_xpath("//input[@id='description']").send_keys(self.alert.description)

        # Sending Tuple
        for field in self.alert.fields:
            self.web_session.web_driver.find_element_by_id(field[0]).send_keys(field[1])

        self.ui_utils.sleep(1)
        # Notification Frequency
        Select(self.web_session.web_driver.find_element_by_id("repeat_time")).select_by_visible_text("1 Minute")

        if hasattr(self.alert, 'operator'):
            Select(self.web_session.web_driver.find_element_by_id("select_mw_operator")).select_by_visible_text(
                self.alert.operator)
        else:
            self.web_session.logger.info("Nothing to do her")


        self.web_session.web_driver.find_element_by_xpath("//button[contains(.,'Add')]").click()
        assert self.ui_utils.waitForTextOnPage('Alert "{}" was added'.format(self.alert.description), 200)

        return True


    def remove_alert(self):

        navigate(self.web_session).get("{}/miq_policy/explorer".format(self.web_session.MIQ_URL))

        self.ui_utils.sleep(1)

        if not self.web_session.web_driver.find_element_by_xpath("//*[@id='alert_accord']").is_displayed():
            self.web_session.web_driver.find_element_by_xpath("//a[contains(text(),'Alerts')]").click()

        self.web_session.web_driver.find_element_by_xpath("//div[@id='treeview-alert_tree']/ul/li[2]").click()

        self.ui_utils.sleep(2)

        self.web_session.web_driver.find_element_by_xpath("//button[@title='Configuration']").click()

        self.web_session.web_driver.find_element_by_id("miq_alert_vmdb_choice__alert_delete").click()
        self.ui_utils.accept_alert(20)
        assert self.ui_utils.waitForTextOnPage('Alert "{}": Delete successful'.format(self.alert.description), 5)
        self.web_session.logger.info("The alert {} is removed successfully.".format(self.alert.description))



        return True