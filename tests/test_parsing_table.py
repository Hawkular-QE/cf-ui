
import pytest
from common.session import session
from parsing.table import Table


@pytest.fixture (scope='session')
def web_session(request):
    web_session = session()

    def closeSession():
        print ('Close browser session')
        web_session.close_web_driver()
    request.addfinalizer(closeSession)
    return web_session


def test_sucess(web_session):
    print 'Start parsing'
    table = Table(web_session)

    print table.get_middleware_datasources_table()
    print table.get_middleware_providers_table()
    print table.get_middleware_servers_table()
    print table.get_middleware_w_deployments_table()
