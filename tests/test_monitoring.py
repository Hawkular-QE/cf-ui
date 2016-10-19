import pytest
from common.session import session
from views.monitoring import monitoring

@pytest.fixture (scope='session')
def web_session(request):
    web_session = session(add_provider=True)

    def closeSession():
        web_session.logger.info("Close browser session")
        web_session.close_web_driver()
        request.addfinalizer(closeSession)

    return web_session

def test_cfui_provider_monitoring_timelines(web_session):
    web_session.logger.info("Provider Monitoring Timelines")
    assert monitoring(web_session).validate_provider_monitoring_timelines()

def test_cfui_eap_servers_monitoring_utilization(web_session):
    web_session.logger.info("Servers Monitoring Utilization - Middlware Server (MET-005)")
    assert monitoring(web_session).validate_eap_servers_monitoring_utilization()

def test_cfui_messagings_monitoring_utilization_jms_queues(web_session):
    web_session.logger.info("EAP Monitoring Utilization - JMS Queues (MET-008)")
    assert monitoring(web_session).validate_messagings_monitoring_utilization_jms_queues()

def test_cfui_messagings_monitoring_utilization_jms_topics(web_session):
    web_session.logger.info("EAP Monitoring Utilization - JMS Topoics (MET-009)")
    assert monitoring(web_session).validate_messagings_monitoring_utilization_jms_topics()

def test_cfui_datasources_monitoring_utilization(web_session):
    web_session.logger.info("EAP Monitoring Utilization - Wait and Creation Times (MET-006 and MET-007)")
    assert monitoring(web_session).validate_datasources_monitoring_utilization()
