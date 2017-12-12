import pytest
from common.session import session
from views.alerts import eap_web_session_alerts
from common.model.alert_factory import AlertFactory


@pytest.fixture (scope='session')
def web_session(request):
    web_session = session(add_provider=True)
    web_session.logger.info("Alerts")

    def closeSession():
        web_session.logger.info("Close browser session")
        web_session.close_web_driver()

    request.addfinalizer(closeSession)

    return web_session


def test_add_and_remove_jvm_alerts(web_session):
    alerts = AlertFactory().jvm_alerts()
    for alert in alerts:
        web_session.logger.info("Begin Add/Remove alert {}", alert.category)
        assert eap_web_session_alerts(web_session, alert).add_alert()
        assert eap_web_session_alerts(web_session, alert).remove_alert()

def test_add_and_remove_web_session_alerts(web_session):
    alerts = AlertFactory().web_sessions_alerts()
    for alert in alerts:
        web_session.logger.info("Begin Add/Remove alert {}", alert.category)
        assert eap_web_session_alerts(web_session, alert).add_alert()
        assert eap_web_session_alerts(web_session, alert).remove_alert()

def test_add_and_remove_eap_transactions_alerts(web_session):
    alerts = AlertFactory().eap_transactions_alerts()
    for alert in alerts:
        web_session.logger.info("Begin Add/Remove alert {}", alert.category)
        assert eap_web_session_alerts(web_session, alert).add_alert()
        assert eap_web_session_alerts(web_session, alert).remove_alert()

def test_add_and_remove_messaging(web_session):
    alerts = AlertFactory().messaging_alerts()
    for alert in alerts:
        web_session.logger.info("Begin Add/Remove alert {}", alert.category)
        assert eap_web_session_alerts(web_session, alert).add_alert()
        assert eap_web_session_alerts(web_session, alert).remove_alert()

def test_add_and_remove_datasource(web_session):
    alerts = AlertFactory().datasource_alerts()
    for alert in alerts:
        web_session.logger.info("Begin Add/Remove alert {}", alert.category)
        assert eap_web_session_alerts(web_session, alert).add_alert()
        assert eap_web_session_alerts(web_session, alert).remove_alert()
