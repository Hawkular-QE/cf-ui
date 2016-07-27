import pytest
from common.session import session
from views.deployments import deployments


@pytest.fixture (scope='session')
def web_session(request):
    web_session = session(add_provider=True)

    def closeSession():
        web_session.logger.info("Close browser session")
        web_session.close_web_driver()
    request.addfinalizer(closeSession)

    return web_session

def test_cfui_deployment_details(web_session):
    web_session.logger.info("Begin deployment details test")
    assert deployments(web_session).validate_deployment_details()

def test_cfui_deployment_list(web_session):
    web_session.logger.info("Begin deployment list test")
    assert deployments(web_session).validate_deployments_list()
