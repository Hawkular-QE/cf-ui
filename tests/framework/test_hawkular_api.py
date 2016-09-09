import pytest
from common.session import session
from hawkular.hawkular_api import hawkular_api


@pytest.fixture
def web_session(request):
    web_session = session(add_provider=False, login=False)

    def closeSession():
        web_session.logger.info("Close browser session")
        web_session.close_web_driver()
    request.addfinalizer(closeSession)

    return web_session

def test_cfui_api(web_session):
    assert hawkular_api(web_session).get_hawkular_servers(), "Hawkular Servers List Empty"
    assert hawkular_api(web_session).get_hawkular_deployments(), "Hawkular Deployments List Empty"
    assert hawkular_api(web_session).get_hawkular_datasources(), "Hawkular Datasources List Empty"
    assert hawkular_api(web_session).get_hawkular_domains(), "Hawkular Domains List Empty"
