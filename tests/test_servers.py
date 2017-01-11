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

def test_cfui_eap_operation_suspend(web_session):
    web_session.logger.info("Begin Server Suspend (OPR-005 and OPR-007)")
    assert servers(web_session).eap_power_suspend()

def test_cfui_eap_operation_resume(web_session):
    web_session.logger.info("Begin Server Resume (OPR-006)")
    assert servers(web_session).eap_power_resume()

# EAP Power Not fully functional, as of yet

def _test_cfui_eap_power_reload(web_session):
    web_session.logger.info("Begin Server Reload")
    assert servers(web_session).eap_power_reload()

def _test_cfui_eap_power_graceful_shutdown(web_session):
    web_session.logger.info("Begin Server Graceful Shutdown")
    assert servers(web_session).eap_power_graceful_shutdown()

# End EAP Power

def test_cfui_deploy_application_archive(web_session):
    assert servers(web_session).deploy_application_archive()

def test_cfui_undeploy_application_archive(web_session):
    assert servers(web_session).undeploy_application_archive()

def test_cfui_redeploy_application_archive(web_session):
    assert servers(web_session).restart_application_archive()

def test_cfui_stop_application_archive(web_session):
    web_session.logger.info("Begin Stop Application Archive (OPR-038)")
    assert servers(web_session).disable_application_archive()

def test_cfui_start_application_archive(web_session):
    web_session.logger.info("Begin Start Application Archive (OPR-038)")
    assert servers(web_session).enable_application_archive()

# Add JDBC Driver
def test_cfui_add_jdbc_driver(web_session):
    web_session.logger.info("Begin Add JDBC driver test (OPR-034a)")
    assert servers(web_session).add_jdbc_driver()

# Add datasource
def test_cfui_add_datasource(web_session):
    web_session.logger.info("Begin Add datasource test (OPR-035a)")
    assert servers(web_session).add_datasource("H2-DS")

# More Archive Tests:

def test_cfui_add_disabled_application_archive(web_session):
    web_session.logger.info("Begin add disabled Application Archive")
    assert servers(web_session).add_deployment_disable()

def test_cfui_add_application_archive_overwrite(web_session):
    web_session.logger.info("Begin overwrite Application Archive")
    assert servers(web_session).add_deployment_overwrite()

def test_cfui_add_application_archive_runtime_name(web_session):
    web_session.logger.info("Begin add runtime name to Application Archive")
    assert servers(web_session).add_deployment_runtime_name()

def test_cfui_add_application_archive_cancel(web_session):
    web_session.logger.info("Begin test to cancel the addition of Application Archive")
    assert servers(web_session).add_deployment_cancel()
