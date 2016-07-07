from moviepy.editor import *
import os
import time
import inspect
from multiprocessing import Process, Value

def execCommandParallel(cmd):
    os.system(cmd)

class recorder(object):

    START_COMMAND = "flvrec.py localhost:5"
    STOP_COMMAND = "pkill -SIGINT -f flvrec.py"
    FILENAME = ""
    RECORDSDIRPATH = ""


    def __init__(self, testName = None, session = None):
        self.RECORDSDIRPATH =  os.path.dirname(__file__) + "/../records/"
        if testName:
            self.FILENAME = "out_" + testName
        else:
            # TODO use inspect or traceback package to get testname and use it as filename
            # - not possible because of pytest's fixtures -> using fixture request
            self.FILENAME = os.path.splitext(os.path.basename(inspect.stack()[2][1]))[0]
        if session:
            print(  self.RECORDSDIRPATH )
            print(self.FILENAME)
            print(session.VNC_HOSTNAME)
            print(session.DISPLAY_PORT)
            self.START_COMMAND = "flvrec.py -P " + self.RECORDSDIRPATH + "vncpassword.txt -o " + self.RECORDSDIRPATH + self.FILENAME + ".flv " + session.VNC_HOSTNAME + ":" + session.DISPLAY_PORT
        else:
            self.START_COMMAND = "flvrec.py -P " + self.RECORDSDIRPATH + "vncpassword.txt -o " + self.RECORDSDIRPATH + self.FILENAME + ".flv localhost:5"
        pass

    def start(self):
        print("Start recording...")
        print(self.START_COMMAND)
        # start recording as parallel process
        p = Process(target=execCommandParallel, args=(self.START_COMMAND,))
        p.start()

    def stop(self):
        print("Stop recording...")
        print(self.STOP_COMMAND)
        os.system(self.STOP_COMMAND)
        time.sleep(10)

    def convertToGif(self):
        print("Start converting " + self.FILENAME + ".flv to " + self.FILENAME + ".gif")
        path = self.RECORDSDIRPATH + self.FILENAME + ".flv"
        clip = (VideoFileClip(path))
        clip.write_gif(self.RECORDSDIRPATH + self.FILENAME + ".gif")
        print("Converting flv to gif done.")



