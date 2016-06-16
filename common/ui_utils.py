import time
from selenium.common.exceptions import NoSuchElementException

class ui_utils():

    web_session = None
    web_driver = None

    def __init__(self, web_session):
        self.web_session = web_session
        self.web_driver = web_session.web_driver

    def isTextOnPage(self, text):
        if self.web_driver.find_elements_by_xpath("//*[contains(text(), '" + text + "')]"):
            return True
        else:
            return False

    def waitForTextOnPage(self, text, waitTime):
        currentTime = time.time()
        ## print "Waiting for text: " + text
        while self.isTextOnPage(text) == False:
            if time.time() - currentTime >= waitTime:
                self.web_session.logger.error("Timed out waiting for: %s", text)
                return False
            else:
                time.sleep(1)

        return True

    def isElementPresent(self, locatormethod, locatorvalue):
        try:
            self.web_driver.find_element(by=locatormethod, value=locatorvalue)
        except NoSuchElementException:
            return False
        return True

    def waitForElementOnPage(self, el, waitTime):
        print "To Do"

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
