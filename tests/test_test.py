import pytest
from common.session import session

@pytest.fixture
def web_session(request):
    web_session= session()

    def closeSession():
        print ("Close browser session")
        web_session.close_web_driver()
    request.addfinalizer(closeSession)

    return web_session

def test_test(web_session):
    assert True, "Sanity Login Test"
