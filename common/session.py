
from common.miq_login import miq_login
from conf.properties import properties
from common.recorder import recorder
from selenium import webdriver
from views.providers import providers
import logging
import logging.config
from selenium.webdriver.remote.remote_connection import LOGGER

class session(properties):

    MIQ_URL = None
    HAWKULAR_URL = None
    PROVIDER = "Hawkular"

    web_driver = None
    login = None

    logger = None
    logging_level = logging.DEBUG

    session_recorder = None

    def __init__(self, login=True, add_provider=True, request = None):
        # call parent method to load properties from files
        super(session, self).__init__()

        assert self.MIQ_HOSTNAME, "Property MIQ_HOSTNAME in conf/" + self.PROPERTIES_FILE_NAME + " can not be empty"

        self.login = login

        self.MIQ_URL = "{}://{}".format(self.MIQ__HTTP, self.MIQ_HOSTNAME)
        if self.MIQ_PORT:
            self.MIQ_URL = "{}:{}/".format(self.MIQ_URL, self.MIQ_PORT)

        self.HAWKULAR_URL = "http://{}:{}/".format(self.HAWKULAR_HOSTNAME, self.HAWKULAR_PORT)

        ''' Record to gif if enabled by property RECORD_TESTS in properties.properties'''
        if "True" in self.RECORD_TESTS:
            if request:
                self.session_recorder = recorder(testName=request.function.__name__, session=session)
            else:
                self.session_recorder = recorder(testName=None, session=session)
            self.session_recorder.start()

        self.__logger__()

        ''' Get the Selenium Web Driver, and then navegate to the MIQ URL '''
        self.__get_web_driver__()

        ''' Add provider, if the provider has not all ready been added '''
        if (add_provider):
            providers(self).add_provider(delete_if_provider_present=False)


    def __get_web_driver__(self):

        self.logger.info("Using Browser: %s", self.BROWSER)
        self.web_driver = getattr(webdriver,self.BROWSER)()
        self.web_driver.set_window_size(self.BROWSER_WIDTH, self.BROWSER_HEIGHT)
        self.logger.info("MIQ URL: %s", self.MIQ_URL)
        self.web_driver.get(self.MIQ_URL)

        if (self.login):
            miq_login(self).login(self.MIQ_USERNAME, self.MIQ_PASSWORD)

        return

    def __logger__(self):

        self.logger = logging.getLogger('cf-ui')
        self.logger.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
        ch = logging.StreamHandler()
        ch.setLevel(self.logging_level)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def close_web_driver(self):
        if "True" in self.RECORD_TESTS:
            self.session_recorder.stop()
            self.session_recorder.convertToGif()
        # close browser window
        self.web_driver.close()
        # close browser windows & exit webdriver
        self.web_driver.quit()
