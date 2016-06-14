import time
from selenium.common.exceptions import NoSuchElementException

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
                    self.web_driver.refresh();
                time.sleep(1)
            isTextOnPage = self.isTextOnPage(text)

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
