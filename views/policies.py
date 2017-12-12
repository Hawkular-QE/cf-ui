from common.ui_utils import ui_utils
from common.navigate import navigate
from common.db import db

class policies():
    web_session = None
    web_driver = None
    ui_utils = None

    EVENT_TYPES = ('deployments', 'datasources', 'jdbc')

    def __init__(self, web_session):
        self.web_session = web_session
        self.web_driver = web_session.web_driver
        self.ui_utils = ui_utils(self.web_session)

    def add_middleware_control_policy(self, policy_name, product_name, delete_policy=False, assignment_events=None):
        self.web_session.logger.info('Add Policy: "{}", Product Name: "{}"'.format(policy_name, product_name))

        if db(self.web_session).is_policy_present(policy_name):
            if delete_policy:
                if not self.delete_middleware_control_policy(policy_name):
                    return False
            else:
                self.web_session.logger.info('Policy "{}" already exists.'.format(policy_name))
                return True

        self.navigate_to_middleware_server_control_policies()

        # Add the policy

        self.web_driver.find_element_by_xpath('//*[@title="Configuration"]').click()
        self.ui_utils.sleep(2)
        el = self.web_driver.find_element_by_xpath('//*[@title="Add a New Middleware Server Control Policy"]')
        #self.ui_utils.wait_until_element_displayed(mw_el, 10)
        el.click()
        assert self.ui_utils.waitForTextOnPage("Notes", 15)

        # Fill out form
        self.web_driver.find_element_by_id("description").send_keys(policy_name)
        self.web_driver.find_element_by_xpath("//span[contains(.,'Choose')]").click()
        el = self.web_driver.find_element_by_xpath("//span[contains(.,'Field')]")
        assert self.ui_utils.wait_until_element_displayed(el, 10)
        el.click()
        self.ui_utils.sleep(2)
        self.web_driver.find_elements_by_xpath(".//*[contains(text(), 'Choose') and not (ancestor::*[contains( @ style, 'display: none')])]")[3].click()

        el = self.web_driver.find_element_by_xpath("//*[contains(text(),'Middleware Server : Product')]")
        self.ui_utils.wait_until_element_displayed(el, 10)
        el.click()
        self.ui_utils.sleep(2)
        el = self.web_driver.find_element_by_xpath('//*[@id="exp_atom_editor_div"]/fieldset/div[4]/button/span[1]')
        assert self.ui_utils.wait_until_element_displayed(el, 10)
        el.click()
        el = self.web_driver.find_element_by_xpath("//*[contains(text(),'INCLUDES')]")
        assert self.ui_utils.wait_until_element_displayed(el, 10)
        el.click()
        self.ui_utils.sleep(2)
        el = self.web_driver.find_element_by_id('chosen_value')
        assert self.ui_utils.wait_until_element_displayed(el, 10)
        el.send_keys(product_name)

        # Click on Check box
        el = self.web_driver.find_element_by_class_name('fa-check').click()
        assert self.ui_utils.waitForTextOnPage('Middleware Server : Product INCLUDES "{}"'.format(product_name), 10)

        # Add Policy
        self.web_driver.find_element_by_xpath('//*[@title="Add"]').click()
        assert self.ui_utils.waitForTextOnPage('Policy "{}" was added'.format(policy_name), 10)

        # Assign Policy Events
        if assignment_events:
            self.assign_middleware_policy_events(policy_name, assignment_events)

        return True

    def delete_middleware_control_policy(self, policy_name, navigate=True):
        self.web_session.logger.info('Delete Policy: "{}"'.format(policy_name))

        if not db(self.web_session).is_policy_present(policy_name):
            self.web_session.logger.warning('Policy "{}" does not exists.'.format(policy_name))
            return False

        if navigate:
            self.navigate_to_middleware_server_control_policies(policy_name=policy_name)

        self.web_driver.find_element_by_xpath('//*[@title="Configuration"]').click()
        self.ui_utils.sleep(1)
        try:
            self.web_driver.find_element_by_xpath('//*[@title="Delete this Middleware Server Policy"]').click()
            self.ui_utils.accept_alert(10)
        except Exception, e:
            try:
                self.web_driver.find_element_by_xpath(
                    '//*[@title="Policies that belong to Profiles can not be deleted"]')
                self.web_session.logger.error('Policy "{}" - Policies that belong to Profiles can not be deleted'.format(policy_name))
                return False
            except Exception, e:
                assert False, 'Policy "{}" not found'.format(policy_name)

        assert self.ui_utils.waitForTextOnPage('Policy "{}": Delete successful'.format(policy_name), 10)

        return True

    def assign_middleware_policy_events(self, policy_name, event_type):
        self.web_session.logger.info('Assign Policy Events: "{}", Policy Name: "{}"'.format(event_type, policy_name))

        assert event_type in self.EVENT_TYPES, 'Unsupposrted event type "{}". Valid Event types: {}'\
            .format(event_type, self.EVENT_TYPES)

        self.navigate_to_middleware_server_control_policies(policy_name=policy_name)

        self.web_driver.find_element_by_xpath('//*[@title="Configuration"]').click()
        self.ui_utils.sleep(2)
        self.web_driver.find_element_by_xpath('//*[@title="Edit this Policy\'s Event assignments"]').click()
        self.ui_utils.waitForTextOnPage('"{}" Event Assignments'.format(policy_name), 10)

        els = self.web_driver.find_elements_by_xpath(
            ".//*[contains(text(), 'No') and not (ancestor::*[contains( @ style, 'display: none')])]")

        if event_type == "deployments":
            self.__assign_middleware_policy_deployment_events__(policy_name, els)
        elif event_type == "datasources":
            self.__assign_middleware_policy_datasource_events__(policy_name, els)
        elif event_type == 'jdbc':
            self.__assign_middleware_policy_jdbc_events__(policy_name, els)

        # Save the Assignments
        el = self.web_driver.find_element_by_xpath('//*[@title="Save Changes"]')
        assert self.ui_utils.wait_until_element_displayed(el, 10)
        el.click()
        assert self.ui_utils.waitForTextOnPage('Policy "{}" was saved'.format(policy_name), 15)

    def __assign_middleware_policy_deployment_events__(self, policy_name, els):
        assert self.ui_utils.isTextOnPage('"{}" Event Assignments'.format(policy_name))

        # EAP Application/Deployments
        els[84].click()
        els[85].click()
        els[86].click()
        els[87].click()

    def __assign_middleware_policy_datasource_events__(self, policy_name, els):
        assert self.ui_utils.isTextOnPage('"{}" Event Assignments'.format(policy_name))

        # EAP Datasource
        els[88].click()
        els[89].click()
        els[90].click()
        els[91].click()

    def __assign_middleware_policy_jdbc_events__(self, policy_name, els):
        assert self.ui_utils.isTextOnPage('"{}" Event Assignments'.format(policy_name))

        # EAP JDBC
        els[92].click()
        els[93].click()
        els[94].click()
        els[95].click()

    def navigate_to_middleware_server_control_policies(self, policy_name=None):
        navigate(self.web_session).get("{}/miq_policy/explorer".format(self.web_session.MIQ_URL), wait_for='Policies')

        all_policies_el = self.web_driver.find_element_by_xpath("//a[contains(@href,'#policy_accord')]")
        mw_el = self.web_driver.find_element_by_xpath('//*[@title="Middleware Server Control Policies"]')

        if not mw_el.is_displayed():
            all_policies_el.click()
            assert self.ui_utils.wait_until_element_displayed(mw_el, 10)

        mw_el.click()
        assert self.ui_utils.waitForTextOnPage("All Middleware Server", 10)

        # Click on the Middleware Policy, if it is present
        if policy_name:
            try:
                el = self.web_driver.find_element_by_xpath(
                ".//*[contains(text(), '{}') and not (ancestor::*[contains( @ style, 'display: none')])]".format(policy_name))
                el.click()
                assert self.ui_utils.waitForTextOnPage('Middleware Server Control Policy "{}"'.format(policy_name), 10)
            except Exception, e:
                assert False, 'Element not found for Profile Name "{}"'.format(policy_name)

