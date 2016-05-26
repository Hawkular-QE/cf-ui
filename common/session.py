
from common.miq_login import miq_login
from conf.properties import properties
from selenium import webdriver
from views.servers import servers

class session(properties):

    MIQ_URL = None
    HAWKULAR_URL = None

    web_driver = None
    login = None

    def __init__(self, login=True, add_provider=True):
        self.login = login

        self.MIQ_URL = "http://{}:{}/".format(self.MIQ_HOSTNAME, self.MIQ_PORT)
        self.HAWKULAR_URL = "http://{}:{}/".format(self.HAWKULAR_HOSTNAME, self.HAWKULAR_PORT)

        ''' Get the Selenium Web Driver, and then navegate to the MIQ URL '''
        self.web_driver = self.__get_web_driver__()

        ''' Add provider, if the provider has not all ready been added '''
        if (add_provider):
            servers(self.web_session).add_provider_if_not_present()

    def __get_web_driver__(self):

        driver = webdriver.Firefox()
        print "URL: %s", self.MIQ_URL
        driver.get(self.MIQ_URL)

        if (self.login):
            miq_login(driver).login(self.MIQ_USERNAME, self.MIQ_PASSWORD)

        return driver

    def close_web_driver(self):
        self.web_driver.close()
