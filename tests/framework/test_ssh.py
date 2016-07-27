import pytest
from common.session import session
from common.ssh import ssh

@pytest.fixture
def web_session(request):
    web_session = session(add_provider=False, login=False)

    def closeSession():
        web_session.logger.info("Close browser session")
        web_session.close_web_driver()
    request.addfinalizer(closeSession)

    return web_session

def test_cfui_test(web_session):
    ip = 'eapserver'

    ssh_result = ssh(web_session, ip).execute_command('echo "Hello From Server: `hostname`"')
    assert ssh_result
    web_session.logger.info("ssh_result: {}".format(ssh_result))
    web_session.logger.info("result: {}".format(ssh_result.get('result')))
    web_session.logger.info("output: {}".format(ssh_result.get('output')))

def test_cfui_get_ip(web_session):
    ip = 'eapserver'

    pid = ssh(web_session, ip).get_pid("standalone.sh")
    assert pid
    web_session.logger.info("pid: {}".format(pid))