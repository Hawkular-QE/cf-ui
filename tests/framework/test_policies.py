import pytest
from common.session import session
from views.policies import policies

@pytest.fixture
def web_session(request):
    web_session = session(add_provider=False)

    def closeSession():
        web_session.logger.info("Close browser session")
        web_session.close_web_driver()
    request.addfinalizer(closeSession)

    return web_session

def test_add_policy(web_session):
    assert policies(web_session).add_middleware_control_policy('mw-test-policy', 'JBoss EAP', delete_policy=True, assignment_events='jdbc')

def test_delete_middleware_control_policy(web_session):
    assert policies(web_session).delete_middleware_control_policy('mw-test-policy')