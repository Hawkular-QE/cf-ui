import time

class ui_utils():

    web_driver = None

    def __init__(self, web_driver):
        self.web_driver = web_driver

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
                print 'Timed out waiting for "', text, '"'
                return False
            else:
                time.sleep(1)

        return True

    def isElementOnPage(self, el):
        ## Flesh out - web_driver.isElementPresent(el)
        if True:
            return True
        else:
            return False

    def waitForElementOnPage(self, el, waitTime):
        print "To Do"