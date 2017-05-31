import pytest
from common.session import session
from views.search import search


@pytest.fixture (scope='session')
def web_session(request):
    web_session = session(add_provider=True)

    def closeSession():
        web_session.logger.info("Close browser session")
        web_session.close_web_driver()
    request.addfinalizer(closeSession)

    return web_session

def test_cfui_search_by_name(web_session):
    web_session.logger.info("Begin test - search by name")
    assert search(web_session).simple_search()

