from common.ui_utils import ui_utils
from common.navigate import navigate

class policy_profiles():
    web_session = None
    web_driver = None
    ui_utils = None

    def __init__(self, web_session):
        self.web_session = web_session
        self.web_driver = web_session.web_driver
        self.ui_utils = ui_utils(self.web_session)

    def add_middleware_policy_profile(self, policy_name, policy_profile_name, delete_profile=False):
        self.navigate_to_policy_profiles(policy_name=policy_profile_name)

        if delete_profile:
            if self.ui_utils.isTextOnPage(policy_profile_name):
                if not self.delete_policy_profile(policy_profile_name):
                    return False
        else:
            self.web_session.logger.info('Policy Profile "{}" already exists.'.format(policy_profile_name))
            return True

        policy_profile_name = policy_profile_name + " mwmprofile"

        self.web_driver.find_element_by_xpath('//*[@title="Configuration"]').click()
        self.ui_utils.sleep(1)
        self.web_driver.find_element_by_xpath('//*[@title="Add a New Policy Profile"]').click()
        assert self.ui_utils.waitForTextOnPage("Notes", 15)

        self.web_driver.find_element_by_id('description').send_keys(policy_profile_name)
        self.ui_utils.sleep(2)

        # Select the Profile
        try:
            self.web_driver.find_element_by_xpath(
                ".//*[contains(text(), '{}') and not (ancestor::*[contains( @ style, 'display: none')])]".format(policy_name)).click()
        except Exception, e:
            assert False, 'Policy Profile "{}" not found'.format(policy_name)

        self.ui_utils.sleep(1)
        self.web_driver.find_element_by_xpath('//*[@title="Move selected Policies into this Profile"]').click()
        self.ui_utils.sleep(1)

        # Add button
        self.web_driver.find_element_by_xpath('//*[@title="Add"]').click()
        assert self.ui_utils.waitForTextOnPage('Policy Profile "{}" was added'.format(policy_profile_name), 15)

        return True

    def delete_policy_profile(self, policy_profile_name, navigate=True):

        if navigate:
            self.navigate_to_policy_profiles(policy_profile_name)

        policy_profile_name = policy_profile_name + " mwmprofile"

        self.web_driver.find_element_by_xpath('//*[@title="Configuration"]').click()
        self.ui_utils.sleep(1)

        try:
            self.web_driver.find_element_by_xpath('//*[@title="Remove this Policy Profile"]').click()
            self.ui_utils.accept_alert(10)
            assert self.ui_utils.waitForTextOnPage('Policy Profile "{}": Delete successful'.format(policy_profile_name), 10)
        except Exception, e:
            self.web_session.logger.error('Policy "{}" does not exist'.format(policy_profile_name))
            return False, 'Policy Profile "{}" not found'.format(policy_profile_name)

        return True


    def navigate_to_policy_profiles(self, policy_name=None):
        navigate(self.web_session).get("{}/miq_policy/explorer".format(self.web_session.MIQ_URL), wait_for='Policies')

        policy_name = policy_name + " mwmprofile"
        el = self.web_driver.find_element_by_xpath('//*[@title="All Policy Profiles"]')
        if not el.is_displayed():
            self.web_driver.find_element_by_xpath("//a[contains(@href,'#policy_profile_accord')]").click()
            assert self.ui_utils.wait_until_element_displayed(el, 10)

        # Click on the Middleware Policy Profile, if it is present
        if policy_name:
           try:
                el = self.web_driver.find_element_by_xpath(
                   ".//*[contains(text(), '{}') and not (ancestor::*[contains( @ style, 'display: none')])]".format(policy_name))
                el.click()
                assert self.ui_utils.waitForTextOnPage('Policy Profile "{}"'.format(policy_name), 10)
           except Exception, e:
                self.web_session.logger.warning('Element not found for Profile Name "{}"'.format(policy_name))


    def add_policy_profile_to_server(self, policy_profile_name, server_name):
        navigate(self.web_session).get("{}/middleware_server/show_list".format(self.web_session.MIQ_URL),
                                       wait_for=self.web_session.HAWKULAR_PROVIDER_NAME)

        assert server_name, 'No Server Name'

        # Drill into Server details
        self.ui_utils.click_on_row_containing_text(server_name)
        assert self.ui_utils.waitForTextOnPage('Properties', 15)

        # Navigate to Select Policy Profiles
        self.web_driver.find_element_by_xpath('//*[@title="Policy"]').click()
        self.ui_utils.sleep(2)
        self.web_driver.find_element_by_xpath('//*[@title="Manage Policies for this Middleware Server"]').click()
        self.ui_utils.sleep(2)
        assert self.ui_utils.waitForTextOnPage('Select Policy Profiles', 10)

        # Check / Select the Policy Profile if it has not already been selected

        title_els = self.web_driver.find_elements_by_xpath('//*[contains(@title,"profile")]')
        checkbox_els = self.web_driver.find_elements_by_class_name('check-icon')

        assert (len(title_els) == len(checkbox_els))

        for index, el in enumerate(title_els):
            html = el.get_attribute('outerHTML')
            if policy_profile_name in html:
                if 'node-checked' in html:
                    self.web_session.logger.info("Policy Profile \"{}\"on Server \"{}\" already selected".format(policy_profile_name, server_name))
                else:
                    # Check the box
                    checkbox_els[index].click()
                    assert 'node-check-changed' in el.get_attribute('outerHTML'), 'Checkbox for Policy "\{}\" not changed'.format(policy_profile_name)
                    el = self.web_driver.find_element_by_xpath('//*[@title="Save Changes"]')
                    self.ui_utils.wait_until_element_displayed(el, 10)
                    el.click()
                    self.ui_utils.waitForTextOnPage("Product", 15)

                return True

        # Will reach here if the Policy was not found
        self.web_session.logger.warning("Policy Profile \"{}\"on Server \"{}\" was NOT found".format(policy_profile_name, server_name))
        return False