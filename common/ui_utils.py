import time
from selenium.common.exceptions import NoSuchElementException
from random import sample

class ui_utils():

    web_session = None
    web_driver = None

    def __init__(self, web_session):
        self.web_session = web_session
        self.web_driver = web_session.web_driver

    def isTextOnPage(self, text):
        # Just visible text - http://stackoverflow.com/a/651801
        if self.web_driver.find_elements_by_xpath(".//*[contains(text(), '" + text + "') and not (ancestor::*[contains( @ style,'display:none')]) and not (ancestor::*[contains( @ style, 'display: none')])]"):
            return True
        else:
            return False

    # if exist=False then we wait till texts disappears (waitTillTextOnPage[Not]Exists)
    def waitForTextOnPage(self, text, waitTime, exist=True):
        currentTime = time.time()
        ## print "Waiting for text: " + text
        isTextOnPage = self.isTextOnPage(text)
        while (( not isTextOnPage and exist ) or
                   ( isTextOnPage and not exist )) :
            if time.time() - currentTime >= waitTime:
                self.web_session.logger.error("Timed out waiting for: %s", text)
                return False
            else:
                if not exist:
                    self.web_driver.refresh()
                time.sleep(1)
            isTextOnPage = self.isTextOnPage(text)

        return True

    def isElementPresent(self, locatormethod, locatorvalue):
        try:
            self.web_driver.find_element(by=locatormethod, value=locatorvalue)
        except NoSuchElementException:
            return False
        return True

    # if exist=False then refresh the page and wait till element disappears

    def waitForElementOnPage(self, locatormethod, locatorvalue, waitTime, exist=True):
        currentTime = time.time()

        isElementPresent = self.isElementPresent(locatormethod, locatorvalue)
        while ((not isElementPresent and exist) or
                   (isElementPresent and not exist)):
            if time.time() - currentTime >= waitTime:
                self.web_session.logger.error("Timed out waiting for: %s", locatorvalue)
                return False
            else:
                if not exist:
                    self.web_driver.refresh()
                time.sleep(1)
                isElementPresent = self.isElementPresent(locatormethod, locatorvalue)

        return True

    def sleep(self, waitTime):
        time.sleep(waitTime)

    def get_elements_containing_text(self, text):
        el = self.web_driver.find_elements_by_xpath("//*[contains(text(), '{}')]".format(text))
        if not el:
            self.web_session.logger.warning("No element found for {}".format(text))
        return el

    # Temp method
    def get_generic_table_as_dict(self):
        table = []
        dict = {}

        # 1) Get table as list
        # 2) Convert to Dictionary
        # 3) Return Dictionary

        for tr in self.web_driver.find_elements_by_xpath('.//tr'):
            tds = tr.find_elements_by_tag_name('td')
            if tds: table.append([td.text for td in tds])

        if table:
            for pair in table:
                if len(pair) >= 2:
                    dict[pair[0]] = pair[1]
        else:
            self.web_session.logger.warning("No element found for table.")

        return dict

    def get_list_table(self):
        header = []
        table = []
        dict = []

        # Get table headers
        for tr in self.web_driver.find_elements_by_xpath('.//tr'):
            tds = tr.find_elements_by_tag_name('th')
            if tds: header.append([td.text for td in tds])

        # Get table values
        for tr in self.web_driver.find_elements_by_xpath('.//tr'):
            tds = tr.find_elements_by_tag_name('td')
            if tds: table.append([td.text for td in tds])

        # Build the Dictionary
        for row in table:
            d = {}
            for index, value in enumerate(row, start=0):
                d[header[0][index]] = value

            dict.append(d)

        return dict

    def get_list_table_as_elements(self):
        table = []
        for tr in self.web_driver.find_elements_by_xpath('.//tr'):
            tds = tr.find_elements_by_tag_name('td')
            if tds:
                table.append(tds)

        return table

    def find_row_in_element_table_by_text(self, table, value):
        for row in table:
            for el in row:
                if value in el.text:
                    # self.web_session.logger.info("Found row with text: %s", value)
                    return row

        return None

    # Refresh the page and wait till expected text appears on the page

    def refresh_until_text_appears(self, text, waitTime):
        currentTime = time.time()
        isTextOnPage = self.isTextOnPage(text)
        while not isTextOnPage:
            if time.time() - currentTime >= waitTime:
                self.web_session.logger.error("Timed out waiting for: %s", text)
                return False
            else:
                self.web_driver.refresh()
                time.sleep(1)
            isTextOnPage = self.isTextOnPage(text)

        return True

    def click_on_row_containing_text(self, text):
        ## Click on first row that is found to contain 'value'

        table = []
        for tr in self.web_driver.find_elements_by_xpath('.//tr'):
            tds = tr.find_elements_by_tag_name('td')
            if tds:
                table.append([td.text for td in tds])
                for row in table:
                    for value in row:
                        if value == text:
                            self.web_session.logger.info("Click on {}".format(text))
                            tds[3].click()
                            return;

        assert False, "Did not find value {}.".format(text)

    def get_random_list(self, items, limit):
        if len(items) > limit:
            return sample(items, limit)
        else:
            return items

        return None

    # Given a list of directories, dictionary key and value - find a specific row
    def find_row_in_list(self, list, key, value):
        for row in list:
            if value in row.get(key):
                return row

        return None

    # Ex: [{'column_name':'Feed', 'value':'Feed Value'},{'column_name':'Server Name', 'value':'Server Name Value')}]
    def find_row_in_list_by_multi_value(self, list, key_value_pairs):

        for row in list:
            count = 0
            for pair in key_value_pairs:
                if pair.get('value') not in row.get(pair.get('column_name')):
                    break

                count += 1
                if count == len(key_value_pairs):
                    return row

        return None

    def accept_alert(self, waitTime):
        currentTime = time.time()

        while (time.time() - currentTime < waitTime):
            try:
                self.web_driver.switch_to_alert().accept()
                return True
            except:
                self.web_session.logger.info('Alert not present.')
                self.sleep(1)

        assert False, "Timed out waiting for Alert dialog."

    def adjust_screen_resolution(self, horizontal, vertical):
        self.web_driver.set_window_size(horizontal, vertical)
