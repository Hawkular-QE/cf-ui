import pytest
import time

from common.session import session
from views.alerts import alerts
from common.model.alert_factory import AlertFactory


@pytest.fixture (scope='session')
def web_session(request):
    web_session = session(add_provider=True)
    web_session.logger.info("Alerts")
    web_session.factory = AlertFactory()

    def closeSession():
        web_session.logger.info("Close browser session")
        web_session.close_web_driver()

    request.addfinalizer(closeSession)

    return web_session


def test_jvm_alerts(web_session):
    list_alerts = web_session.factory.jvm_alerts()
    for alert in list_alerts:
        copy_alert = web_session.factory.copy_for_edit(alert)
        web_session.logger.info("Begin Add alert {}".format(alert.category_description()))
        assert alerts(web_session).add_alert(alert)
        web_session.logger.info("Begin Edit alert {}".format(alert.category_description()))
        assert alerts(web_session).edit_alert(alert, copy_alert)
        web_session.logger.info("Begin Remove alert {}".format(alert.category_description()))
        assert alerts(web_session).remove_alert(copy_alert)
        time.sleep(2)

def test_web_session_alerts(web_session):
    list_alerts = web_session.factory.web_sessions_alerts()
    for alert in list_alerts:
        copy_alert = web_session.factory.copy_for_edit(alert)
        web_session.logger.info("Begin Add alert {}".format(alert.category_description()))
        assert alerts(web_session).add_alert(alert)
        web_session.logger.info("Begin Edit alert {}".format(alert.category_description()))
        assert alerts(web_session).edit_alert(alert, copy_alert)
        web_session.logger.info("Begin Remove alert {}".format(alert.category_description()))
        assert alerts(web_session).remove_alert(copy_alert)
        time.sleep(2)

def test_eap_transactions_alerts(web_session):
    list_alerts = web_session.factory.eap_transactions_alerts()
    for alert in list_alerts:
        copy_alert = web_session.factory.copy_for_edit(alert)
        web_session.logger.info("Begin Add alert {}".format(alert.category_description()))
        assert alerts(web_session).add_alert(alert)
        web_session.logger.info("Begin Edit alert {}".format(alert.category_description()))
        assert alerts(web_session).edit_alert(alert, copy_alert)
        web_session.logger.info("Begin Remove alert {}".format(alert.category_description()))
        assert alerts(web_session).remove_alert(copy_alert)
        time.sleep(2)

def test_messaging_alerts(web_session):
    list_alerts = web_session.factory.messaging_alerts()
    for alert in list_alerts:
        copy_alert = web_session.factory.copy_for_edit(alert)
        web_session.logger.info("Begin Add alert {}".format(alert.category_description()))
        assert alerts(web_session).add_alert(alert)
        web_session.logger.info("Begin Edit alert {}".format(alert.category_description()))
        assert alerts(web_session).edit_alert(alert, copy_alert)
        web_session.logger.info("Begin Remove alert {}".format(alert.category_description()))
        assert alerts(web_session).remove_alert(copy_alert)
        time.sleep(2)

def test_datasource_alerts(web_session):
    list_alerts = web_session.factory.datasource_alerts()
    for alert in list_alerts:
        copy_alert = web_session.factory.copy_for_edit(alert)
        web_session.logger.info("Begin Add alert {}".format(alert.category_description()))
        assert alerts(web_session).add_alert(alert)
        web_session.logger.info("Begin Edit alert {}".format(alert.category_description()))
        assert alerts(web_session).edit_alert(alert, copy_alert)
        web_session.logger.info("Begin Remove alert {}".format(alert.category_description()))
        assert alerts(web_session).remove_alert(copy_alert)
        time.sleep(2)
