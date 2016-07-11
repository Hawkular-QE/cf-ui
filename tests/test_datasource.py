import pytest
from common.session import session
from views.datasource import datasources


@pytest.fixture (scope='session')
def web_session(request):
    web_session = session(add_provider=True)

    def closeSession():
        web_session.logger.info("Close browser session")
        web_session.close_web_driver()
    request.addfinalizer(closeSession)

    return web_session

def test_datasource_list(web_session):
    web_session.logger.info("Begin datasource list test")
    assert datasources(web_session).validate_datasource_list()