from subprocess import Popen, PIPE, STDOUT
import re

class openshift_utils():
    oc = 'tools/oc'
    web_session = None
    os_url = None

    def __init__(self, web_session):
        self.web_session = web_session
        self.os_url = "https://{}:{}".format(web_session.OPENSHIFT_HOSTNAME, web_session.OPENSHIFT_PORT)
        self.web_session.logger.info("Openshift URL: {}".format(self.os_url))
        self.cli_login()


    def __exec_cmd__(self, cmd):
        self.web_session.logger.info("OC cmd: {}".format(cmd))
        return Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)


    def cli_login(self):
        p = self.__exec_cmd__("{} login {} -u {} -p {}"
                .format(self.oc, self.os_url, self.web_session.OPENSHIFT_USERNAME, self.web_session.OPENSHIFT_PASSWORD))

        stdout = p.stdout.read()
        stderror = p.stderr.read()

        if stderror:
            raise Exception("Openshift command failed: {}").format(stderror)
        else:
            if not "Login successful" in stdout:
                raise Exception("Openshift Login failed: {}".format(stdout))
            else:
                self.web_session.logger.debug("Openshift login output: {}".format(stdout))


    def get_token(self):
        p = self.__exec_cmd__("{} whoami --token".format(self.oc))
        token = re.sub(r"\W", "", p.stdout.read())
        self.web_session.logger.info("Openshift Token: {}".format(token))

        return token
