from common.ui_utils import ui_utils
from common.timeout import timeout

class navigate():
    web_driver = None
    web_session = None
    ui_utils = None

    minutes_to_wait = (10 * 60)

    def __init__(self, web_session):
        self.web_driver = web_session.web_driver
        self.web_session = web_session
        self.ui_utils = ui_utils(web_session)

    def get(self, url):
        with timeout(seconds=self.minutes_to_wait, error_message="Timed out with \"We're sorry, but something went wrong\"."):
            while True:
                self.web_driver.get(url)
                if not self.ui_utils.isTextOnPage("sorry, but something went wrong"):
                    break
                else:
                    self.web_session.logger.info('Encountered "Sorry" message.')
                    self.ui_utils(self.web_session).sleep(5)
                    self.web_driver.refresh()