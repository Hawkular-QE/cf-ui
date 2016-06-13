import pytest
from common.session import session
from views.providers import providers


@pytest.fixture (scope='session')
def web_session(request):
    web_session = session(add_provider=False)

    def closeSession():
        web_session.logger.info("Close browser session")
        web_session.close_web_driver()
    request.addfinalizer(closeSession)

    return web_session

def test_add_provider(web_session):
    provs = providers(web_session)
    provs.add_provider()

def test_update_provider(web_session):
    provs = providers(web_session)
    provs.update_provider()

def test_delete_provider(web_session):
    provs = providers(web_session)
    provs.delete_provider(delete_all_providers=True)
    provs.add_provider()
    provs.delete_hawkular_provider()
