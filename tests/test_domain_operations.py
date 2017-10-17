import pytest
from common.session import session
from views.domain_eap_operations import domain_eap_operations


@pytest.fixture (scope='session')
def web_session(request):
    web_session = session(add_provider=True)
    web_session.logger.info("OPR010, OPR011, OPR012, OPR013, OPR014, OPR015: Operations on Single JBoss EAP in a server group")

    def closeSession():
        web_session.logger.info("Close browser session")
        web_session.close_web_driver()

    request.addfinalizer(closeSession)

    return web_session


def test_domain_mode_eap_stop(web_session):
    web_session.logger.info("Begin eap Stop Test")
    assert domain_eap_operations(web_session).stop_eap()

def test_eap_start(web_session):
    web_session.logger.info("Begin eap Start Test")
    assert domain_eap_operations(web_session).start_eap()

def test_eap_restart(web_session):
    web_session.logger.info("Begin eap Restart Test")
    assert domain_eap_operations(web_session).restart_eap()

def test_eap_suspend(web_session):
    web_session.logger.info("Begin eap Suspend Test")
    assert domain_eap_operations(web_session).suspend_eap()

def test_eap_resume(web_session):
    web_session.logger.info("Begin eap Resume Test")
    assert domain_eap_operations(web_session).resume_eap()

def test_eap_reload(web_session):
    web_session.logger.info("Begin eap Reload Test")
    assert domain_eap_operations(web_session).reload_eap()

def test_eap_kill(web_session):
    web_session.logger.info("Begin eap Kill Test")
    assert domain_eap_operations(web_session).kill_eap()
    assert domain_eap_operations(web_session).start_eap()











