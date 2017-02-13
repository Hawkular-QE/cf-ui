import pytest
from common.session import session
from common.ui_utils import ui_utils

@pytest.fixture
def web_session(request):
    web_session = session(add_provider=True)

    def closeSession():
        web_session.logger.info("Close browser session")
        web_session.close_web_driver()
    request.addfinalizer(closeSession)

    return web_session

def test_cfui_test(web_session):
    web_session.logger.info("Begin Test")
    assert True, "Sanity Login Test"


def test_cfui_log_sleep(web_session):
    web_session.logger.info("Begin Long Wait")
    ui_utils(web_session).sleep(10000)