import pytest
from common.session import session
from views.eap_jvm_alerts import eap_jvm_alerts

# TODO @gbaufake - to be refactored and included on test_alerts (edit, copy)

@pytest.fixture (scope='session')
def web_session(request):
    web_session = session(add_provider=True)
    web_session.logger.info("ALR-001: Define Alerts based upon EAP metrics")

    def closeSession():
        web_session.logger.info("Close browser session")
        web_session.close_web_driver()

    request.addfinalizer(closeSession)

    return web_session


def test_add_mw_alert(web_session):
    web_session.logger.info("Begin Add alert test")
    assert eap_jvm_alerts(web_session).add_alert()

def test_copy_mw_alert(web_session):
    web_session.logger.info("Begin Copy alert test")
    assert eap_jvm_alerts(web_session).copy_alert()

def test_edit_mw_alert(web_session):
    web_session.logger.info("Begin Edit alert test")
    assert eap_jvm_alerts(web_session).edit_alert()

def test_delete_mw_alert(web_session):
    web_session.logger.info("Begin delete alert test")
    assert eap_jvm_alerts(web_session).delete_alert(eap_jvm_alerts.editalert_desc)
    assert eap_jvm_alerts(web_session).delete_alert(eap_jvm_alerts.copyalert_desc)

