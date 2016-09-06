from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from navigation.navigation import NavigationTree

from time import sleep


class tags():

    web_driver = None
    web_session = None
    nav = None

    def __init__(self, _web_session):
        self.web_session = _web_session
        self.web_driver = _web_session.web_driver
        self.nav = NavigationTree(self.web_session)

    def waiting_ability(self, xpath, seconds):
        try:
            WebDriverWait(self.web_driver, seconds).until(
                EC.element_to_be_clickable((By.XPATH, xpath)))
        except:
            self.web_session.logger.info(" Given object is not clickable. (waiting_clickability)")
            self.waiting_ability(xpath, seconds - 1)


    def button_click(self, xpath, seconds):
        driver = self.web_driver
        self.web_session.logger.info(" Exact XPath: {}".format(xpath))
        self.waiting_ability(xpath, seconds)
        try:
            driver.find_element_by_xpath(xpath).click()
        except:
            self.button_click(xpath, seconds-1 )


    def click_option(self, option_name, xpath):
        for option in self.web_driver.find_elements_by_xpath( xpath ):
            if option_name in option.text:
                print "Click on option : ", option.text
                option.click()
                break


    def set_tag(self, tag_name, tag_value):
        driver = self.web_session.web_driver
        logger = self.web_session.logger

        #if navigation:
        #    NavigationTree(self.web_session).jump_to_middleware_servers_view().to_first_details().select_and_click('Policy', 'Edit Tags')

        if tag_value in self.ui_tags()[tag_name]:
            print "Already added (set_tag: ", tag_name, "::", tag_value, ")"
            return self

        column_xpath = "//button[@data-toggle='dropdown'][@data-id='{}']"
        option_xpath = "//select[@id='{}']/../div[contains(@class, 'btn-group')]/div/ul/li/a"
        xpath_save = "//button[contains(@title,'Save Changes')]"

        tag_button = column_xpath.format("tag_cat")
        self.button_click(tag_button, 7)

        option_button = option_xpath.format("tag_cat")
        self.click_option(tag_name, option_button)

        value_button = column_xpath.format("tag_add")
        self.button_click(value_button, 7)

        value_option = option_xpath.format("tag_add")
        self.click_option(tag_value, value_option)

        save_click = driver.find_element_by_xpath(xpath_save)
        WebDriverWait(self.web_driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, xpath_save))
            )
        save_click.click()

        flash_caption = "id('flash_text_div')/div/strong[contains(.,'Tag edits were successfully saved')]"
        WebDriverWait(self.web_driver, 7).until(
            EC.visibility_of_element_located((By.XPATH, flash_caption))
            )

        import re
        src = self.web_driver.page_source
        text_to_search = r'Tag edits were successfully saved'
        text_found = re.search(text_to_search, src)
        assert(text_found != None), "Not Found."

        return self


    def count_tags_on_page(self):
        WebDriverWait(self.web_driver, 7).until(EC.visibility_of_any_elements_located((By.XPATH, "id('main_div')/div[@id='tab_div']/h3[contains(.,'Tag Assignment')]")))
        xpath = './/table/tbody/tr[contains(@id, "_tr")]'
        num_tags = len( self.web_driver.find_elements_by_xpath(xpath) )
        #print "Numbers of tags: ", num_tags
        return num_tags


    def ui_tags(self):
        xpath = "//table/tbody/tr[contains(@id,'_tr')]/td[not(contains(@title,'Click'))]"
        driver = self.web_driver
        sleep(3)

        collected_tags = driver.find_elements_by_xpath(xpath)
        num = len(collected_tags)
        tags = [ tag.text for tag in collected_tags ]

        from collections import defaultdict
        tag_dict = defaultdict(list)

        for zz in zip(*[iter(tags)] * 2):
            #print zz[0], " -> ", zz[1]
            key = zz[0].encode('ascii', 'ignore')
            val = zz[1].encode('ascii', 'ignore')
            tag_dict[key].append( val )
        return tag_dict

    def _set_tags(self, tags):
        for category in tags.keys():
            for value in tags[category]:
                self.set_tag(category, value)

    def drop_tag(self, tag_name, tag_value):
        driver = self.web_driver
        print "Current page: ", driver.current_url

        if self.count_tags_on_page() == 0 or tag_value not in self.ui_tags()[tag_name]:
            print "Nothing to delete."
            return self

        magic_xpath = "//td[contains(., '{}')]/../td[contains(., '{}')]/../td[contains(@title, 'to remove this assignment')]".format(tag_name, tag_value)
        magic_button = None
        try:
            magic_button = driver.find_element_by_xpath(magic_xpath)
        except:
            raise ValueError("These tag name or tag value not present on page: {} | {}".format(tag_name, tag_value))

        magic_button.click()

        xpath_save = "//div[@id='buttons_on']/button[@title='Save Changes']"
        WebDriverWait(self.web_driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, xpath_save))
            )
        save_button = driver.find_element_by_xpath(xpath_save)
        save_button.click()
        return self

    def drop_first_tag(self):
        driver = self.web_driver
        self.web_session.logger.info(" --| drop first tag")
        magic_xpath = "(//td[@title='Click to remove this assignment'])[1]"

        """
        if self.count_tags_on_page() == 0:
            print "Nothing to delete."
            return self
        """

        WebDriverWait(self.web_driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, magic_xpath))
        )
        tag_list = driver.find_elements_by_xpath(magic_xpath)

        #for x in tag_list:
        x_button = driver.find_element_by_xpath(magic_xpath)
        WebDriverWait(self.web_driver, 7).until(EC.element_to_be_clickable((By.XPATH, magic_xpath)))
        x_button.click()

        xpath_save = "//button[contains(@title,'Save Changes')]"
        save_button = driver.find_element_by_xpath(xpath_save)
        WebDriverWait(self.web_driver, 7).until(EC.element_to_be_clickable((By.XPATH, xpath_save)))
        save_button.click()

        flash_caption = "id('flash_text_div')/div/strong[contains(.,'Tag edits were successfully saved')]"
        WebDriverWait(self.web_driver, 7).until(
            EC.visibility_of_element_located((By.XPATH, flash_caption))
        )

        import re
        src = self.web_driver.page_source
        text_to_search = r'Tag edits were successfully saved'
        text_found = re.search(text_to_search, src)
        assert (text_found != None), "Not Found."

        return self


    def drop_all_tags(self):
        driver = self.web_driver
        wait = WebDriverWait(self.web_driver, 15)
        self.web_session.logger.info("drop all these tags")

        num_tags = self.count_tags_on_page()
        if num_tags == 0:
            print "Nothing to delete."
            return self

        first_xpath = "(//td[@title='Click to remove this assignment'])[1]"
        xpath_save = "//button[contains(@title,'Save Changes')]"
        WebDriverWait(self.web_driver, 5).until(EC.visibility_of_element_located((By.XPATH, first_xpath)))

        for i in range(0, num_tags):
            #print "({})".format(i)
            x_button = driver.find_element_by_xpath(first_xpath)
            x_button.click()
            wait.until(EC.staleness_of(driver.find_element_by_xpath(first_xpath)))

        save_button = driver.find_element_by_xpath(xpath_save)
        wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath_save)))
        wait.until(EC.element_to_be_clickable((By.XPATH, xpath_save)))
        save_button.click()

        flash_caption = "id('flash_text_div')/div/strong[contains(.,'Tag edits were successfully saved')]"
        WebDriverWait(self.web_driver, 7).until(
            EC.visibility_of_element_located((By.XPATH, flash_caption)))

        import re
        src = self.web_driver.page_source
        text_to_search = r'Tag edits were successfully saved'
        text_found = re.search(text_to_search, src)
        assert(text_found != None), "Not Found."

        return self
