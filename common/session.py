
from common.miq_login import miq_login
from conf.properties import properties
from selenium import webdriver
from views.providers import providers
import logging
import logging.config
from selenium.webdriver.remote.remote_connection import LOGGER

class session(properties):

    MIQ_URL = None
    HAWKULAR_URL = None

    web_driver = None
    login = None

    logger = None
    logging_level = logging.DEBUG

    def __init__(self, login=True, add_provider=True):
        # call parent method to load properties from files
        super(session, self).__init__()

        self.login = login

        self.MIQ_URL = "http://{}:{}/".format(self.MIQ_HOSTNAME, self.MIQ_PORT)
        self.HAWKULAR_URL = "http://{}:{}/".format(self.HAWKULAR_HOSTNAME, self.HAWKULAR_PORT)

        self.__logger__()

        ''' Get the Selenium Web Driver, and then navegate to the MIQ URL '''
        self.__get_web_driver__()

        ''' Add provider, if the provider has not all ready been added '''
        if (add_provider):
            providers(self).add_provider_if_not_present()

    def __get_web_driver__(self):

        self.logger.info("Using Browser: %s", self.BROWSER)
        self.web_driver = getattr(webdriver,self.BROWSER)()
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
        self.web_driver.close()
