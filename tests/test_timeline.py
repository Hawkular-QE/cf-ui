import pytest
from common.session import session
from views.timelines import timelines

@pytest.fixture (scope='session')
def web_session(request):
    web_session = session(add_provider=True)

    def closeSession():
        web_session.logger.info("Close browser session")
        web_session.close_web_driver()
        request.addfinalizer(closeSession)

    return web_session

def test_cfui_test_event_successful_deployment(web_session):
    web_session.logger.info("Begin test to check event generated for successful deployment")
    assert timelines(web_session).test_event_for_successful_deployment()

def test_cfui_test_event_unsuccessful_deployment(web_session):
    web_session.logger.info("Begin test to check event generated for unsuccessful deployment")
    assert timelines(web_session).test_event_for_unsuccessful_deployment()