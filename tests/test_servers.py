import pytest
from common.session import session
from views.servers import servers


@pytest.fixture (scope='session')
def web_session(request):
    web_session = session(add_provider=True)

    def closeSession():
        web_session.logger.info("Close browser session")
        web_session.close_web_driver()
        request.addfinalizer(closeSession)

    return web_session

def test_cfui_servers_view(web_session):
    web_session.logger.info("Begin Server View")
    assert servers(web_session).validate_servers_list()

def test_cfui_server_details(web_session):
    web_session.logger.info("Begin Server Details")
    assert servers(web_session).validate_server_details()

def test_cfui_server_policy_edit_hawkular(web_session):
    web_session.logger.info("Begin Server Policy Edit")
    assert servers(web_session).server_policy_edit('provider')

def test_cfui_server_policy_edit_eap(web_session):
    web_session.logger.info("Begin Server Policy Edit")
    # EAP choice "JBoss" or "WildFly"
    assert servers(web_session).server_policy_edit('eap')

def test_cfui_eap_power_stop(web_session):
    web_session.logger.info("Begin Server Stop")
    assert servers(web_session).eap_power_stop()

def test_cfui_eap_power_restart(web_session):
    web_session.logger.info("Begin Server Restart")
    assert servers(web_session).eap_power_restart()

# EAP Power Not fully functional, as of yet

def _test_cfui_eap_power_reload(web_session):
    web_session.logger.info("Begin Server Reload")
    assert servers(web_session).eap_power_reload()

def _test_cfui_eap_power_suspend(web_session):
    web_session.logger.info("Begin Server Suspend")
    assert servers(web_session).eap_power_suspend()

def _test_cfui_eap_power_resume(web_session):
    web_session.logger.info("Begin Server Resume")
    assert servers(web_session).eap_power_resume()

def _test_cfui_eap_power_graceful_shutdown(web_session):
    web_session.logger.info("Begin Server Graceful Shutdown")
    assert servers(web_session).eap_power_graceful_shutdown()

# End EAP Power

def test_cfui_deploy_application_archive(web_session):
    assert servers(web_session).deploy_application_archive()

def test_cfui_undeploy_application_archive(web_session):
    assert servers(web_session).undeploy_application_archive()

def test_cfui_redeploy_application_archive(web_session):
    assert servers(web_session).redeploy_application_archive()

def test_cfui_stop_application_archive(web_session):
    assert servers(web_session).stop_application_archive()

def test_cfui_start_application_archive(web_session):
    assert servers(web_session).start_application_archive()