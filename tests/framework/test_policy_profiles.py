import pytest
from common.session import session
from views.policy_profiles import policy_profiles
from views.servers import servers

DEPLOYMENTS_POLICY = 'mw-test-deployments-policy'
DEPLOYMENTS_POLICY_PROFILE = 'mw-test-deployment-policy-profile'

JDBC_POLICY = 'mw-test-jdbc-policy'
JDBC_POLICY_PROFILE = 'mw-test-JDBC-policy-profile'

DATASOURCES_POLICY = 'mw-test-datasources-policy'
DATASOURCES_POLICY_PROFILE = 'mw-test-datasources-policy-profile'

@pytest.fixture
def web_session(request):
    web_session = session()

    def closeSession():
        web_session.logger.info("Close browser session")
        web_session.close_web_driver()
    request.addfinalizer(closeSession)

    return web_session

def test_add_policy_profile(web_session):
    assert policy_profiles(web_session).add_middleware_policy_profile(DATASOURCES_POLICY, DATASOURCES_POLICY_PROFILE, delete_profile=True)

def test_add_policy_profile_to_server(web_session):
    web_session.logger.info("Begin Policy Event Deployment")
    server = servers(web_session).find_eap_in_state("Running")
    assert server
    assert policy_profiles(web_session).add_policy_profile_to_server(JDBC_POLICY_PROFILE, server.get('Host Name'))

def _test_delete_middleware_policy_profile(web_session):
    assert policy_profiles(web_session).delete_policy_profile(DEPLOYMENTS_POLICY_PROFILE)