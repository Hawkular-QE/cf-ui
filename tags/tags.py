from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from navigation.navigation import NavigationTree


class tags():

    web_driver = None
    web_session = None
    nav = None

    def __init__(self, _web_session):
        self.web_session = _web_session
        self.web_driver = _web_session.web_driver
        self.nav = NavigationTree(self.web_session)
        self.logger = _web_session.logger
        time_delay = 750
        self.wait = WebDriverWait(self.web_driver, time_delay)


    def button_click(self, xpath, seconds):
        driver = self.web_driver
        click = driver.find_element_by_xpath(xpath)
        click.click()


    def click_option(self, option_name, xpath):
        for option in self.web_driver.find_elements_by_xpath( xpath ):
            option_text = "{}".format(option.text)
            if option_name in option.text:
                #print "Click on -> ", option_text
                option.click()
                break


    def get_tag_value_group(self):
        #wait = WebDriverWait(self.web_driver, 5)
        driver = self.web_session.web_driver
        tag_value_group_xpath = ".//*[@id='cat_tags_div']/div/select"

        tag_value_group_value = driver.find_element_by_xpath(tag_value_group_xpath)
        trace = tag_value_group_value.get_attribute('innerHTML')
        self.wait.until_not(EC.staleness_of(tag_value_group_value))
        return trace


    def values_group_is_updated(self, state_before):
        return self.get_tag_value_group() != state_before


    def set_tag(self, tag_name, tag_value):
        driver = self.web_session.web_driver
        #logger = self.web_session.logger
        #wait = WebDriverWait(self.web_driver, 5)

        existent_tags = self.ui_tags()
        if tag_value in existent_tags[tag_name]:
            print "Already added (set_tag: ", tag_name, "::", tag_value, ")"
            return self

        column_xpath = "//button[@data-toggle='dropdown'][@data-id='{}']"
        tag_name_button = column_xpath.format("tag_cat")
        tag_value_button = "//button[@data-toggle='dropdown'][@data-id='tag_add']/span/span[@class='caret']"

        tag_name_options = ".//*[@id='tab_div']/table/thead/tr/th[2]/div/div/ul/li/a/span[@class='text']"
        tag_value_options = ".//*[@id='cat_tags_div']/div/div/ul/li" # NNN matches

        xpath_save = "//button[contains(@title,'Save Changes')]"
        flash_caption = "id('flash_text_div')/div/strong[contains(.,'Tag edits were successfully saved')]"

        state_before = self.get_tag_value_group()

        self.button_click(tag_name_button, 7)
        self.click_option(tag_name, tag_name_options)

        self.wait.until(lambda lamb: self.values_group_is_updated(state_before))
        self.button_click(tag_value_button, 7)
        self.click_option(tag_value, tag_value_options)

        save_click = driver.find_element_by_xpath(xpath_save)
        self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath_save)))
        save_click.click()

        self.wait.until(EC.visibility_of_element_located((By.XPATH, flash_caption)))
        if not driver.find_element_by_xpath("//strong[contains(.,'Tag edits were successfully saved')]"):
            raise ValueError("Flasher not found!")
        return self


    def count_tags_on_page(self):
        driver = self.web_driver
        #wait = WebDriverWait(self.web_driver, 5)
        xpath = './/table/tbody/tr[contains(@id, "_tr")]'
        xpath_0 = ".//*[@id='assignments_div']/table/tbody/tr/td[2]"
        self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath_0)))
        determinator = driver.find_element_by_xpath(xpath_0).get_attribute('innerHTML')

        if 'No My Company Tags are assigned' in determinator:
            return 0
        num_tags = len( driver.find_elements_by_xpath(xpath) )
        return num_tags

    def ui_tags(self):
        #wait = WebDriverWait(self.web_driver, 5)
        xpath = "//table/tbody/tr[contains(@id,'_tr')]/td[not(contains(@title,'Click'))]"
        driver = self.web_driver

        xpath_0 = ".//*[@id='assignments_div']/table/tbody/tr"
        self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath_0)))
        self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath_0)))

        collected_tags = driver.find_elements_by_xpath(xpath)
        tags = [ tag.text for tag in collected_tags ]

        from collections import defaultdict
        tag_dict = defaultdict(list)

        for zz in zip(*[iter(tags)] * 2):
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
            return "Nothing to delete."
            #return self

        magic_xpath = "//td[contains(., '{}')]/../td[contains(., '{}')]/../td[contains(@title, 'to remove this assignment')]".format(tag_name, tag_value)
        magic_button = None
        try:
            magic_button = driver.find_element_by_xpath(magic_xpath)
        except:
            raise ValueError("These tag name or tag value not present on page: {} | {}".format(tag_name, tag_value))

        magic_button.click()

        xpath_save = "//div[@id='buttons_on']/button[@title='Save Changes']"
        self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath_save)))
        save_button = driver.find_element_by_xpath(xpath_save)
        save_button.click()
        return self

    def drop_first_tag(self):
        driver = self.web_driver
        self.web_session.logger.info(" --| drop first tag")
        magic_xpath = "(//td[@title='Click to remove this assignment'])[1]"

        self.wait.until(EC.visibility_of_element_located((By.XPATH, magic_xpath)))
        tag_list = driver.find_elements_by_xpath(magic_xpath)

        x_button = driver.find_element_by_xpath(magic_xpath)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, magic_xpath)))
        x_button.click()

        xpath_save = "//button[contains(@title,'Save Changes')]"
        save_button = driver.find_element_by_xpath(xpath_save)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath_save)))
        save_button.click()

        flash_caption = "id('flash_text_div')/div/strong[contains(.,'Tag edits were successfully saved')]"
        self.wait.until(EC.visibility_of_element_located((By.XPATH, flash_caption)))

        import re
        src = self.web_driver.page_source
        text_to_search = r'Tag edits were successfully saved'
        text_found = re.search(text_to_search, src)
        assert (text_found != None), "Not Found."
        return self


    def drop_all_tags(self):
        driver = self.web_driver
        #wait = WebDriverWait(self.web_driver, 15)
        self.web_session.logger.info("drop all these tags")

        first_xpath = "(//td[@title='Click to remove this assignment'])[1]"
        xpath_save = "//button[contains(@title,'Save Changes')]"

        num_tags = self.count_tags_on_page()
        #print "Number of tags: ", num_tags
        if num_tags == 0:
            print "Nothing to delete."
            return self

        for i in range(0, num_tags):
            x_button = driver.find_element_by_xpath(first_xpath)
            self.wait.until(EC.visibility_of_element_located((By.XPATH, first_xpath)))
            self.wait.until(EC.element_to_be_clickable((By.XPATH, first_xpath)))
            x_button.click()
            self.wait.until(EC.staleness_of(driver.find_element_by_xpath(first_xpath)))

        save_button = driver.find_element_by_xpath(xpath_save)
        self.wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath_save)))
        self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath_save)))
        save_button.click()

        flash_caption = "id('flash_text_div')/div/strong[contains(.,'Tag edits were successfully saved')]"
        self.wait.until(EC.visibility_of_element_located((By.XPATH, flash_caption)))

        import re
        src = self.web_driver.page_source
        text_to_search = r'Tag edits were successfully saved'
        text_found = re.search(text_to_search, src)
        assert(text_found != None), "Not Found."
        return self


    def set_servers_multi_tags_a(self):
        logger = self.logger
        logger.info("Begin set_few_tags test")

        tags_2 = {'Department': ['Engineering', 'Marketing']}
        tags_5 = {
            'Department': ['Engineering'],
            'LifeCycle *': ['Fully retire VM and remove from Provider'],
            'Quota - Max Storage *': ['1TB'],
            'Auto Approve - Max VM *': ['5'],
            'Auto Approve - Max Memory *': ['8GB']
        }

        tag_dict = tags_5
        t = tags(self.web_session)
        nav = NavigationTree(self.web_session).jump_to_middleware_servers_view().to_first_details().select_and_click('Policy', 'Edit Tags')

        logger.info("collect existent tags")
        stored_tags = t.ui_tags()
        print "SAVED TAGS == ", stored_tags

        logger.info("Starting to set given tags")
        for tag_key in tag_dict.keys():
            for tag_value in tag_dict[tag_key]:
                logger.info( " - Set tag: ({} -> {})".format(tag_key, tag_value))
                nav.jump_to_middleware_servers_view().to_first_details().select_and_click('Policy', 'Edit Tags')
                t.set_tag(tag_key, tag_value)

        logger.info(" == drop all tags == ")
        nav.jump_to_middleware_servers_view().to_first_details().select_and_click('Policy', 'Edit Tags')
        t.drop_all_tags()

        logger.info("restoring saved tags")
        nav.jump_to_middleware_servers_view().to_first_details().select_and_click('Policy', 'Edit Tags')

        print "TAGS TO BE RESTORED: ", stored_tags
        for tag_key in stored_tags.keys():
            for tag_value in stored_tags[tag_key]:
                print "Restore (", tag_key, " - ", tag_value, ")"
                nav.jump_to_middleware_servers_view().to_first_details().select_and_click('Policy', 'Edit Tags')
                t.set_tag(tag_key, tag_value)


    def restore_tags(self):
        logger = self.web_session.logger

        tags_5 = {
            'Department': ['Engineering'],
            'LifeCycle *': ['Fully retire VM and remove from Provider'],
            'Quota - Max Storage *': ['1TB'],
            'Auto Approve - Max VM *': ['5'],
            'Auto Approve - Max Memory *': ['8GB']
        }
        t = tags(self.web_session)

        nav = NavigationTree(self.web_session).jump_to_middleware_servers_view().to_first_details().select_and_click('Policy', 'Edit Tags')
        logger.info("collect existent tags")
        # stored_tags = t.ui_tags() # second way to store tags
        stored_tags = tags_5
        print "STORED TAGS == ", stored_tags

        logger.info("drop all tags")
        t.drop_all_tags()

        logger.info("restoring saved tags")
        for tag_key in stored_tags.keys():
            for tag_value in stored_tags[tag_key]:
                print "Restore (", tag_key, " - ", tag_value, ")"
                nav.jump_to_middleware_servers_view().to_first_details().select_and_click('Policy', 'Edit Tags')
                t.set_tag(tag_key, tag_value)
