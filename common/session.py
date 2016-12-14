
from common.miq_login import miq_login
from conf.properties import properties
from common.recorder import recorder
from selenium import webdriver
import os
from views.providers import providers
import logging
import logging.config
from selenium.webdriver.chrome.options import Options
from common.ssh import ssh

class session(properties):

    MIQ_URL = None
    HAWKULAR_URL = None
    PROVIDER = "Hawkular"

    web_driver = None
    login = None

    logger = None
    logging_level = logging.DEBUG

    session_recorder = None
    fixture_request = None

    appliance_version = None

    def __init__(self, login=True, add_provider=True, request = None):
        # call parent method to load properties from files
        super(session, self).__init__()

        self.fixture_request = request

        assert self.MIQ_HOSTNAME, "Property MIQ_HOSTNAME in conf/" + self.PROPERTIES_FILE_NAME + " can not be empty"
        assert self.HAWKULAR_HOSTNAME, "Property HAWKULAR_HOSTNAME in conf/" + self.PROPERTIES_FILE_NAME + " can not be empty"

        self.login = login

        self.MIQ_URL = "{}://{}".format(self.MIQ__HTTP, self.MIQ_HOSTNAME)
        if self.MIQ_PORT:
            self.MIQ_URL = "{}:{}/".format(self.MIQ_URL, self.MIQ_PORT)

        self.HAWKULAR_URL = "http://{}:{}/".format(self.HAWKULAR_HOSTNAME, self.HAWKULAR_PORT)

        self.__logger__()

        ''' Record to gif if enabled by property RECORD_TESTS in properties.properties'''
        if "True" in self.RECORD_TESTS:
            self.session_recorder = recorder(session=self)
            self.session_recorder.start()

        ''' Get the Selenium Web Driver, and then navegate to the MIQ URL '''
        self.__get_web_driver__()

        ''' Add provider, if the provider has not all ready been added '''
        if (add_provider):
            providers(self).add_provider(delete_if_provider_present=False)

    def __get_web_driver__(self):

        if self.BROWSER == "Firefox":
            self.logger.info("Using Browser: %s", self.BROWSER)
            profile = webdriver.FirefoxProfile()
            # enable auto download
            # http://stackoverflow.com/questions/24852709/how-do-i-automatically-download-files-from-a-pop-up-dialog-using-selenium-python
            profile.set_preference("browser.download.folderList", 2)
            profile.set_preference("browser.download.manager.showWhenStarting", False)
            profile.set_preference("browser.download.dir", '~/Downloads/')
            profile.set_preference("browser.download.panel.shown", False)
            profile.set_preference("browser.helperApps.neverAsk.openFile","text/csv,application/vnd.ms-excel,text/plain")
            profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv,application/vnd.ms-excel,text/plain")

            self.web_driver = getattr(webdriver,self.BROWSER)(firefox_profile=profile)
        elif self.BROWSER == "Chrome":
            self.logger.info("Using Browser: %s", self.BROWSER)
            chrome_options = Options()
            # enable auto download
            # http://stackoverflow.com/questions/21082499/selenium-chromedriver-download-profile
            #prefs = {'download.prompt_for_download': "False", 'download.default_directory' : '~/Downloads/'}
            prefs = {"prefs": {
                            "download.default_directory": '~/Downloads/',
                            "download.prompt_for_download": False
                        },
                "switches": ["-silent", "--disable-logging"],
                "chromeOptions": {
                            "args": ["-silent", "--disable-logging"]
                        }
                }
            chrome_options.add_experimental_option("prefs", prefs)
            self.web_driver = getattr(webdriver,self.BROWSER)(chrome_options=chrome_options)
        else:
            self.logger.info("Using Browser (no options): %s", self.BROWSER)
            self.web_driver = getattr(webdriver,self.BROWSER)()

        self.web_driver.set_window_size(self.BROWSER_WIDTH, self.BROWSER_HEIGHT)
        self.logger.info("MIQ URL: %s", self.MIQ_URL)
        self.logger.info("Hawkular URL: %s", self.HAWKULAR_URL)
        self.web_driver.get(self.MIQ_URL)

        ''' Get Appliance Version - MIQ will be 'master', CFME will be 5.x '''
        try:
            # Appliance is running on a Forman provisioned vm or in a container on a Docker server - use SSH creds
            ssh_session = ssh(self, self.MIQ_HOSTNAME)
        except:
            # Appliance is Sprout provisioned running on the Host VM - use MIQ-PASSWORD
            ssh_session = ssh( self, self.MIQ_HOSTNAME, self.SSH_PORT, self.SSH_USERNAME, self.MIQ_PASSWORD )

        self.appliance_version = ssh_session.get_appliance_version()
        assert self.appliance_version, "Appliance version not found"
        self.logger.info("MIQ/CFME Version: %s", self.appliance_version)

        if (self.login):
            miq_login(self).login(self.MIQ_USERNAME, self.MIQ_PASSWORD)

        return

    def __logger__(self):

        self.logger = logging.getLogger('cf-ui')

        if len(self.logger.handlers[:]) == 0:
            self.logger.setLevel(logging.DEBUG)

            # create formatter
            formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
            ch = logging.StreamHandler()
            ch.setLevel(self.logging_level)
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)

            if "True" in self.RECORD_TESTS:
                ch = logging.FileHandler(os.path.dirname(__file__) + "/../pytest.log")
                ch.setLevel(self.logging_level)
                ch.setFormatter(formatter)
                self.logger.addHandler(ch)

            self.logger.info("Logger Handler created.")

        else:
            self.logger.info("Logger Handler already created.")

    def close_web_driver(self):
        if "True" in self.RECORD_TESTS:
            self.session_recorder.stop()
        if not "True" in self.KEEP_BROWSER_RUNNING:
            # close browser window
            # self.web_driver.close()
            # close browser windows & exit webdriver
            self.web_driver.quit()

