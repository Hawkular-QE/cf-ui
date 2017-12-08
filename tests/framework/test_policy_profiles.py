import pytest
from common.session import session
from views.policy_profiles import policy_profiles

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

def test_delete_middleware_policy_profile(web_session):
    assert policy_profiles(web_session).delete_policy_profile('mw-test-policy-profile')