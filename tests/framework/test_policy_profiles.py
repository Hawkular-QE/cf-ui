import pytest
from common.session import session
from views.policy_profiles import policy_profiles
from views.servers import servers

@pytest.fixture
def web_session(request):
    web_session = session(add_provider=False)

    def closeSession():
        web_session.logger.info("Close browser session")
        web_session.close_web_driver()
    request.addfinalizer(closeSession)

    return web_session

def test_add_policy_profile(web_session):
    assert policy_profiles(web_session).add_middleware_policy_profile('mw-test-policy', 'mw-test-policy-profile', delete_profile=True)

def test_add_policy_profile_to_server(web_session):
    web_session.logger.info("Begin Policy Event Deployment")
    server_name = servers(web_session).find_eap_in_state("Running").get('Host Name')
    assert server_name
    assert policy_profiles(web_session).add_policy_profile_to_server("mw-test-policy-profile", server_name)

def test_delete_middleware_policy_profile(web_session):
    assert policy_profiles(web_session).delete_policy_profile('mw-test-policy')