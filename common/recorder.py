import os
import time
import inspect
from multiprocessing import Process, Value
import subprocess

def runCommand(cmd):
    os.system(cmd)

class recorder(object):

    START_COMMAND = "flvrec.py localhost:5"
    STOP_COMMAND = "pkill -SIGINT -f flvrec.py"
    FILENAME = ""
    RECORDSDIRPATH = ""

    web_session = None

    def __init__(self, session = None):
        self.web_session = session

        self.RECORDSDIRPATH =  os.path.dirname(__file__) + "/../records/"

        if self.web_session and self.web_session.fixture_request:
            self.FILENAME = "record_" + self.web_session.fixture_request.function.__name__
        else:
            # TODO use inspect or traceback package to get testname and use it as filename
            # - not possible because of pytest's fixtures -> using fixture request
            self.FILENAME = "record_" + os.path.splitext(os.path.basename(inspect.stack()[2][1]))[0]
        if self.web_session:
            self.START_COMMAND = "flvrec.py -C " + str(int(self.web_session.BROWSER_WIDTH)-10) + "x" + \
                                 str(int(self.web_session.BROWSER_HEIGHT)-40+int(self.web_session.TERMINAL_HEIGHT)) + "+0-0 -r 10 -P " + \
                                 self.RECORDSDIRPATH + "vncpassword.txt -o " + self.RECORDSDIRPATH + \
                                 self.FILENAME + ".flv " + self.web_session.VNC_HOSTNAME + ":" + \
                                 self.web_session.DISPLAY_PORT
        else:
            self.START_COMMAND = "flvrec.py -C " + str(int(self.web_session.BROWSER_WIDTH)-10) + "x" + \
                                 str(int(self.web_session.BROWSER_HEIGHT)-40+int(self.web_session.TERMINAL_HEIGHT)) + "+0-0 -r 10 -P " + \
                                 self.RECORDSDIRPATH + "vncpassword.txt -o " + self.RECORDSDIRPATH + \
                                 self.FILENAME + ".flv localhost:5"
        pass

    def start(self):
        self.web_session.logger.info("Start recording...")
        self.web_session.logger.info(self.START_COMMAND)
        # start recording as parallel process
        p = Process(target=runCommand, args=(self.START_COMMAND,))
        p.start()

    def stop(self):
        self.web_session.logger.info("Stop recording...")
        self.web_session.logger.info(self.STOP_COMMAND)
        os.system(self.STOP_COMMAND)
        time.sleep(10)
