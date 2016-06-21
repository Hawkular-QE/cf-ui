import pytest
from common.session import session
from hawkular.hawkular_api import hawkular_api


@pytest.fixture
def web_session(request):
    web_session = session(add_provider=False)

    def closeSession():
        web_session.logger.info("Close browser session")
        web_session.close_web_driver()
    request.addfinalizer(closeSession)

    return web_session

def test_api(web_session):
    hawk = hawkular_api(web_session).hawkular_get_servers_list()
    print hawk
