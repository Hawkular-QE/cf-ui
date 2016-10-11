import pytest
from common.session import session
from common.ssh import ssh
from views.servers import servers

@pytest.fixture
def web_session(request):
    web_session = session(add_provider=False, login=False)

    def closeSession():
        web_session.logger.info("Close browser session")
        web_session.close_web_driver()
    request.addfinalizer(closeSession)

    return web_session

def _test_cfui_test(web_session):
    server = servers(web_session).find_eap_in_state("running")
    assert server
    
    ssh_result = ssh(web_session, server.get("details").get("Hostname")).execute_command('echo "Hello From Server: `hostname`"')
    assert ssh_result
    web_session.logger.info("ssh_result: {}".format(ssh_result))
    web_session.logger.info("result: {}".format(ssh_result.get('result')))
    web_session.logger.info("output: {}".format(ssh_result.get('output')))

def _test_cfui_get_ip(web_session):
    server = servers(web_session).find_non_container_eap_in_state("any")
    assert server

    pid = ssh(web_session, server.get("details").get("Hostname")).get_pid("standalone.sh")
    assert pid
    web_session.logger.info("pid: {}".format(pid))

def test_cfui_get_appliance_version(web_session):
    try:
        s = ssh(web_session, web_session.MIQ_HOSTNAME)
    except:
        # For the case where MIQ/CFME is Sprout provisioned running on the Host VM
        s = ssh(web_session, web_session.MIQ_HOSTNAME, web_session.SSH_PORT, web_session.SSH_USERNAME, web_session.MIQ_PASSWORD)

    assert s.get_appliance_version()