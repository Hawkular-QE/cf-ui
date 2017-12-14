import pytest
from common.session import session
from views.policies import policies

DEPLOYMENTS_POLICY = {'policy':'mw-test-deployments-policy', 'event':'deployments'}
JDBC_POLICY = {'policy':'mw-test-jdbc-policy', 'event':'jdbc'}
DATASOURCES_POLICY = {'policy':'mw-test-datasources-policy', 'event':'datasources'}

@pytest.fixture
def web_session(request):
    web_session = session()

    def closeSession():
        web_session.logger.info("Close browser session")
        web_session.close_web_driver()
    request.addfinalizer(closeSession)

    return web_session

def test_add_deployments_policy(web_session):
    assert policies(web_session).add_middleware_control_policy(DEPLOYMENTS_POLICY.get('policy'), 'JBoss EAP',
                                            delete_policy=True, assignment_events=DEPLOYMENTS_POLICY.get('event'))

def test_add_datasources_policy(web_session):
    assert policies(web_session).add_middleware_control_policy(DATASOURCES_POLICY.get('policy'), 'JBoss EAP',
                                            delete_policy=True, assignment_events=DATASOURCES_POLICY.get('event'))

def test_add_jdbc_policy(web_session):
    assert policies(web_session).add_middleware_control_policy(JDBC_POLICY.get('policy'), 'JBoss EAP',
                                            delete_policy=True, assignment_events=JDBC_POLICY.get('event'))

def _test_delete_middleware_control_policy(web_session):
    assert policies(web_session).delete_middleware_control_policy(DEPLOYMENTS_POLICY.get('policy'))

def _test_delete_middleware_control_policy(web_session):
    assert policies(web_session).delete_middleware_control_policy(DATASOURCES_POLICY.get('policy'))

def _test_delete_middleware_control_policy(web_session):
    assert policies(web_session).delete_middleware_control_policy(JDBC_POLICY.get('policy'))