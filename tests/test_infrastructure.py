import pytest
from common.session import session
from views.providers import providers
from views.infrastructures import infrastructures


@pytest.fixture (scope='session')
def web_session(request):
    web_session = session(add_provider=False)

    def closeSession():
        web_session.logger.info("Close browser session")
        web_session.close_web_driver()
    request.addfinalizer(closeSession)

    return web_session

def test_cfui_add_provider(web_session):
    infra = infrastructures(web_session)
    infra.add_provider()
