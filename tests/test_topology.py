import pytest
from common.session import session
from views.topology import topology


@pytest.fixture (scope='session')
def web_session(request):
    web_session = session()

    def closeSession():
        web_session.logger.info("Close browser session")
        web_session.close_web_driver()
    request.addfinalizer(closeSession)

    return web_session

def test_default_topology_view(web_session):
    assert topology(web_session).validate_default_topology_view()