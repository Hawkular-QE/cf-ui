import pytest
from common.session import session
from views.eap_web_sessions_alerts import eap_web_session_alerts
from common.model.alert_factory import AlertFactory
import uuid

@pytest.fixture (scope='session')
def web_session(request):
    web_session = session(add_provider=True)
    web_session.logger.info("Alerts")

    def closeSession():
        web_session.logger.info("Close browser session")
        web_session.close_web_driver()

    request.addfinalizer(closeSession)

    return web_session


def test_add_web_session_alert(web_session):
    alert = AlertFactory().create_alert("Alert-" + str(uuid.uuid4()), "web_sessions_active", ['0'])
    alert.operator = ">="
    web_session.logger.info("Begin " + alert.category + " Test")
    assert eap_web_session_alerts(web_session, alert).add_alert()

def test_add_remove_web_session_alert(web_session):
    alert = AlertFactory().create_alert("Alert-" + str(uuid.uuid4()), "web_sessions_active", ['0'])
    alert.operator = ">="
    web_session.logger.info("Begin " + alert.category + " Test")
    assert eap_web_session_alerts(web_session, alert).add_alert()
    assert eap_web_session_alerts(web_session, alert).remove_alert()


def test_add_jvm_alert(web_session):
    alert = AlertFactory().create_alert("Alert-" + str(uuid.uuid4()), "jvm_heap_used", ['90', '10'])
    web_session.logger.info("Begin " + alert.category + " Test")
    assert eap_web_session_alerts(web_session, alert).add_alert()