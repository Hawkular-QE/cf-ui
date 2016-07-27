import pytest
import time
from common.session import session

@pytest.fixture
def web_session(request):
    web_session = session(add_provider=False, request = request)
    def closeSession():
        web_session.logger.info("Close browser session")
        web_session.close_web_driver()

    request.addfinalizer(closeSession)

    return web_session

def test_cfui_failing(web_session):
    web_session.logger.info("Begin Test")
    time.sleep(5)
    raise Exception('A very specific bad thing happened')
    assert False, "Sanity Login Test Fail"
