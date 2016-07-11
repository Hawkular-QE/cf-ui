import pytest
from common.session import session
from parsing.table import table
from views.datasource import datasource

@pytest.fixture (scope='session')
def web_session(request):
    web_session = session()

    def closeSession():
        print ('Close browser session')
        web_session.close_web_driver()

    request.addfinalizer(closeSession)
    return web_session

def test_datasourceList(web_session):
    data_source = datasource(web_session)
    data_source.list_datasource()
    data_source.validate_datasource("ExampleDS")
    data_source.validate_datasource("KeycloakDS")
    print ("Datasource Found")

