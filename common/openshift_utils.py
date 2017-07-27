import subprocess

class openshift_utils():
    oc = 'tools/oc'
    web_session = None
    os_url = None
    login_cmd = None

    def __init__(self, web_session):
        self.web_session = web_session
        self.os_url = "https://{}:{}".format(web_session.OPENSHIFT_HOSTNAME, web_session.OPENSHIFT_PORT)
        self.web_session.logger.info("Openshift URL: {}".format(self.os_url))
        self.login_cmd = "{} login {} -u {} -p {}".format(self.oc, self.os_url,
                                self.web_session.OPENSHIFT_USERNAME, self.web_session.OPENSHIFT_PASSWORD)


    def __exec_cmd__(self, cmd):
        self.web_session.logger.info("OC cmd: {}".format(cmd))
        p = subprocess.Popen("/bin/bash", shell=True, stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.stdin.write(cmd)
        stdout, stderr = p.communicate()

        self.web_session.logger.debug("STDOUT: {}".format(stdout))
        self.web_session.logger.debug("STDERR: {}".format(stderr))

        return stdout, stderr

    def get_token(self):
        cmd = "{};{} whoami --token".format(self.login_cmd, self.oc)
        stdout, stderr = self.__exec_cmd__(cmd)
        assert str(stdout) != '', "Error: No OC stdout text."
        token = stdout.split()[-1]
        self.web_session.logger.info("Openshift Token: {}".format(token))

        return(token)
