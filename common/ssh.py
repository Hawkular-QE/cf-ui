import paramiko
from common.ui_utils import ui_utils

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

        stdin, stdout, stderr = self.ssh.exec_command(command)

        while not stdout.channel.exit_status_ready():
            self.web_session.logger.info('Exit status not ready after command execute: {}'.format(command))
            ui_utils(self.web_session).sleep(1)

        if stdout.channel.exit_status == 0:
            ssh_result['output'] = stdout.read()
        else:
            ssh_result['output'] = stderr.read()

        ssh_result['result'] = stdout.channel.exit_status

        return ssh_result
