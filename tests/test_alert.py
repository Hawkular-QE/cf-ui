import pytest
from common.session import session
from common.eap_alerts import eap_alerts


@pytest.fixture (scope='session')
def web_session(request):
    web_session = session(add_provider=True)

    def closeSession():
        web_session.logger.info("Close browser session")
        web_session.close_web_driver()
    request.addfinalizer(closeSession)

    return web_session

def test_add_mw_alert(web_session):
    web_session.logger.info("Begin Add alert test")
    assert eap_alerts(web_session).add_alert()
