import paramiko
from common.ui_utils import ui_utils
import re

class ssh():
    web_session = None
    ip = None
    port = None
    username = None
    password = None
    ssh = None

    # IP is a required param, while port/username/password will default to properties.properties
    def __init__(self, web_session, ip, port = None, username = None, password = None):

        self.web_session = web_session
        self.ip = ip
        self.port = self.web_session.SSH_PORT if port == None else port
        self.username = self.web_session.SSH_USERNAME if username == None else username
        self.password = self.web_session.SSH_PASSWORD if password == None else password

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        self.web_session.logger.info(
            "SSH connecting to server: {}, port: {}, username: {}, password: {}."
            .format(self.ip, self.port, self.username, self.password))

        try:
            self.ssh.connect(self.ip, int(self.port), self.username, self.password, allow_agent=True, timeout=60)
        except paramiko.AuthenticationException:
            raise Exception('Authentication failure.')
        except paramiko.SSHException:
            raise Exception('SSH failure.')
        except Exception, e:
            raise Exception(e)


    def execute_command(self, command):
        ssh_result = {}

        self.web_session.logger.info('Execute command \"{}\" on IP \"{}\".'.format(command, self.ip))

        try:
            stdin, stdout, stderr = self.ssh.exec_command(command)

            while not stdout.channel.exit_status_ready():
                self.web_session.logger.info('Exit status not ready after command execute: {}'.format(command))
                ui_utils(self.web_session).sleep(1)

            if stdout.channel.exit_status == 0:
                ssh_result['output'] = stdout.read()
            else:
                ssh_result['output'] = stderr.read()

            ssh_result['result'] = stdout.channel.exit_status

        except Exception, e:
            self.web_session.logger.error('Failed to execute command \"{}\" on IP \"{}\".'.format(command, self.ip))
            ssh_result['output'] = e
            ssh_result['result'] = -1

        return ssh_result


    def get_pid(self, process_name):
        pid = None
        cmd = "ps -ef | grep {} | grep -v grep  | awk {}".format(process_name, "'{ print $2 }'")

        self.web_session.logger.info("Get pid for process: {}  on ip: {}".format(process_name, self.ip))

        ssh_result = self.execute_command(cmd)
        if ssh_result['result'] == 0:
            pid = re.sub('[^0-9]+', "", ssh_result["output"])
            if len(pid) == 0: pid = None
        else:
            self.web_session.logger.info("Unable to get pid for process: {}  on ip: {}".format(process_name, self.ip))

        self.web_session.logger.info("Returning pid: {} for process: {}  on ip: {}".format(pid, process_name, self.ip))

        return pid

    def get_appliance_version(self):
        version = None
        version_file = '/var/www/miq/vmdb/VERSION'
        command = None

        # First, attempt to 'cat /var/www/miq/vmdb/VERSION'
        # If 'No such file', then most likely appliance is running in a container. Thus, get version via 'docker cp'

        try:
            command = 'cat {}'.format(version_file)
            ssh_result = self.execute_command(command)

            if ssh_result['result'] != 0:
                if 'No such file or directory' in ssh_result['output']:
                    command = "docker cp `docker ps | grep cfme |  awk {}`:{} VERSION_CFUI ; cat ./VERSION_CFUI".format("'{ print $1 }'", version_file)
                    ssh_result = self.execute_command(command)
                    if ssh_result['result'] == 0:
                        version = ssh_result["output"]
            else:
                version = ssh_result["output"]

        except Exception, e:
            self.web_session.logger.error('Failed to execute command \"{}\" on IP \"{}\".'.format(command, self.ip))

        return version.rstrip()
