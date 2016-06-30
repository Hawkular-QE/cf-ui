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

def test_test(web_session):
    ip = 'myserver'

    ssh_result = ssh(web_session, ip).execute_command('echo "Hello From Server: `hostname`"')
    assert ssh_result
    print "ssh_result: ", ssh_result
    print 'result: {}'.format(ssh_result.get('result'))
    print 'output: {}'.format(ssh_result.get('output'))

