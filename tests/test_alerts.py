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
        edit_alert = web_session.factory.copy_alert(alert)
        copied_alert = web_session.factory.copy_alert(alert)
        web_session.logger.info("Begin Add alert {}".format(alert.category_description()))
        assert alerts(web_session).add_alert(alert)
        web_session.logger.info("Begin Edit alert {}".format(alert.category_description()))
        assert alerts(web_session).edit_alert(alert, edit_alert)
        web_session.logger.info("Begin Remove alert {}".format(alert.category_description()))
        assert alerts(web_session).remove_alert(edit_alert)
        time.sleep(2)
        # web_session.logger.info("Begin Add to Copy alert {}".format(alert.category_description()))
        # assert alerts(web_session).add_alert(alert)
        # web_session.logger.info("Begin Copy alert {}".format(alert.category_description()))
        # assert alerts(web_session).copy_alert(alert, copied_alert)
        # web_session.logger.info("Begin Remove copied alert {}".format(alert.category_description()))
        # assert alerts(web_session).remove_alert(copied_alert)


def test_web_session_alerts(web_session):
    list_alerts = web_session.factory.web_sessions_alerts()
    for alert in list_alerts:
        edit_alert = web_session.factory.copy_alert(alert)
        copied_alert = web_session.factory.copy_alert(alert)
        web_session.logger.info("Begin Add alert {}".format(alert.category_description()))
        assert alerts(web_session).add_alert(alert)
        web_session.logger.info("Begin Edit alert {}".format(alert.category_description()))
        assert alerts(web_session).edit_alert(alert, edit_alert)
        web_session.logger.info("Begin Remove alert {}".format(alert.category_description()))
        assert alerts(web_session).remove_alert(edit_alert)
        time.sleep(2)
        # web_session.logger.info("Begin Add to Copy alert {}".format(alert.category_description()))
        # assert alerts(web_session).add_alert(alert)
        # web_session.logger.info("Begin Copy alert {}".format(alert.category_description()))
        # assert alerts(web_session).copy_alert(alert, copied_alert)
        # web_session.logger.info("Begin Remove copied alert {}".format(alert.category_description()))
        # assert alerts(web_session).remove_alert(copied_alert)

def test_eap_transactions_alerts(web_session):
    list_alerts = web_session.factory.eap_transactions_alerts()
    for alert in list_alerts:
        edit_alert = web_session.factory.copy_alert(alert)
        copied_alert = web_session.factory.copy_alert(alert)
        web_session.logger.info("Begin Add alert {}".format(alert.category_description()))
        assert alerts(web_session).add_alert(alert)
        web_session.logger.info("Begin Edit alert {}".format(alert.category_description()))
        assert alerts(web_session).edit_alert(alert, edit_alert)
        web_session.logger.info("Begin Remove alert {}".format(alert.category_description()))
        assert alerts(web_session).remove_alert(edit_alert)
        time.sleep(2)
        # web_session.logger.info("Begin Add to Copy alert {}".format(alert.category_description()))
        # assert alerts(web_session).add_alert(alert)
        # web_session.logger.info("Begin Copy alert {}".format(alert.category_description()))
        # assert alerts(web_session).copy_alert(alert, copied_alert)
        # web_session.logger.info("Begin Remove copied alert {}".format(alert.category_description()))
        # assert alerts(web_session).remove_alert(copied_alert)

def test_messaging_alerts(web_session):
    list_alerts = web_session.factory.messaging_alerts()
    for alert in list_alerts:
        edit_alert = web_session.factory.copy_alert(alert)
        copied_alert = web_session.factory.copy_alert(alert)
        web_session.logger.info("Begin Add alert {}".format(alert.category_description()))
        assert alerts(web_session).add_alert(alert)
        web_session.logger.info("Begin Edit alert {}".format(alert.category_description()))
        assert alerts(web_session).edit_alert(alert, edit_alert)
        web_session.logger.info("Begin Remove alert {}".format(alert.category_description()))
        assert alerts(web_session).remove_alert(edit_alert)
        time.sleep(2)
        # web_session.logger.info("Begin Add to Copy alert {}".format(alert.category_description()))
        # assert alerts(web_session).add_alert(alert)
        # web_session.logger.info("Begin Copy alert {}".format(alert.category_description()))
        # assert alerts(web_session).copy_alert(alert, copied_alert)
        # web_session.logger.info("Begin Remove copied alert {}".format(alert.category_description()))
        # assert alerts(web_session).remove_alert(copied_alert)

def test_datasource_alerts(web_session):
    list_alerts = web_session.factory.datasource_alerts()
    for alert in list_alerts:
        edit_alert = web_session.factory.copy_alert(alert)
        copied_alert = web_session.factory.copy_alert(alert)
        web_session.logger.info("Begin Add alert {}".format(alert.category_description()))
        assert alerts(web_session).add_alert(alert)
        web_session.logger.info("Begin Edit alert {}".format(alert.category_description()))
        assert alerts(web_session).edit_alert(alert, edit_alert)
        web_session.logger.info("Begin Remove alert {}".format(alert.category_description()))
        assert alerts(web_session).remove_alert(edit_alert)
        time.sleep(2)
        # web_session.logger.info("Begin Add to Copy alert {}".format(alert.category_description()))
        # assert alerts(web_session).add_alert(alert)
        # web_session.logger.info("Begin Copy alert {}".format(alert.category_description()))
        # assert alerts(web_session).copy_alert(alert, copied_alert)
        # web_session.logger.info("Begin Remove copied alert {}".format(alert.category_description()))
        # assert alerts(web_session).remove_alert(copied_alert)
