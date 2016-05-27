import pytest
from common.session import session
from views.providers import providers


@pytest.fixture (scope='session')
def web_session(request):
    web_session = session()

    def closeSession():
        print ("Close browser session")
        web_session.close_web_driver()
    request.addfinalizer(closeSession)

    return web_session

def test_add_provider(web_session):
    provs = providers(web_session)
    provs.add_provider()
    assert True, "Validate Success - To-Do"