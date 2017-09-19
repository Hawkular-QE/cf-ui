from common.ui_utils import ui_utils
from common.timeout import timeout

class navigate():
    web_driver = None
    web_session = None
    ui_utils = None

    minutes_to_wait = (10 * 60)
    wait_for_text = 'Middleware'

    def __init__(self, web_session):
        self.web_driver = web_session.web_driver
        self.web_session = web_session
        self.ui_utils = ui_utils(web_session)

    def get(self, url):
        self.web_sesssion.logger.debug("Navigate to URL {}".format(url))
        with timeout(seconds=self.minutes_to_wait, error_message="Timed Navigating \"{}\"".format(url)):
            while True:
                try:
                    self.web_driver.get(url)
                    assert self.ui_utils.waitForTextOnPage(self.wait_for_text, 15), "Failed to find text '{}'".format(self.wait_for_text)
                    break
                except:
                    if self.ui_utils.isTextOnPage("sorry, but something went wrong"):
                        self.web_session.logger.info('Encountered "Sorry" message.')
                        self.ui_utils.sleep(5)
                        pass
                    else:
                        self.web_session.logger.error('Failed URL navigation')
                        raise
 