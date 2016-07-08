import pytest
from common.session import session
from views.servers import servers


@pytest.fixture (scope='session')
def web_session(request):
    web_session = session()

    def closeSession():
        web_session.logger.info("Close browser session")
        web_session.close_web_driver()
    request.addfinalizer(closeSession)

    return web_session

def test_servers_view(web_session):
    web_session.logger.info("Begin Server View")
    assert servers(web_session).validate_servers_list()

def test_server_details(web_session):
    web_session.logger.info("Begin Server Details")
    assert servers(web_session).validate_server_details()

def test_server_policy_edit_hawkular(web_session):
    web_session.logger.info("Begin Server Policy Edit")
    assert servers(web_session).server_policy_edit(web_session.PROVIDER)

def test_server_policy_edit_eap(web_session):
    web_session.logger.info("Begin Server Policy Edit")
    # EAP choice "JBoss" or "WildFly"
    assert servers(web_session).server_policy_edit('JBoss')

def test_eap_power_stop(web_session):
    web_session.logger.info("Begin Server Stop")
    assert servers(web_session).eap_power_stop()

def test_eap_power_restart(web_session):
    web_session.logger.info("Begin Server Restart")
    assert servers(web_session).eap_power_restart()

def _test_eap_power_reload(web_session):
    web_session.logger.info("Begin Server Reload")
    assert servers(web_session).eap_power_reload()

def _test_eap_power_suspend(web_session):
    web_session.logger.info("Begin Server Suspend")
    assert servers(web_session).eap_power_suspend()

def _test_eap_power_resume(web_session):
    web_session.logger.info("Begin Server Resume")
    assert servers(web_session).eap_power_resume()

def _test_eap_power_graceful_shutdown(web_session):
    web_session.logger.info("Begin Server Graceful Shutdown")
    assert servers(web_session).eap_power_graceful_shutdown()