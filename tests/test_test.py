import pytest
from common.session import session


@pytest.fixture
def web_session(request):
    web_session = session()

    def closeSession():
        web_session.logger.info("Close browser session")
        web_session.close_web_driver()
    request.addfinalizer(closeSession)

    return web_session

def test_test(web_session):
    web_session.logger.info("Begin Test")
    assert True, "Sanity Login Test"


