
import pytest
from common.session import session
from parsing.table import table


@pytest.fixture (scope='session')
def web_session(request):
    web_session = session()

    def closeSession():
        print ('Close browser session')
        web_session.close_web_driver()
    request.addfinalizer(closeSession)
    return web_session


def _test_instance(web_session):

    t = table(web_session)

    print "List of middleware datasources: ", t.get_middleware_datasource_table(), "\n"
    print "List of middleware providers: ", t.get_middleware_providers_table(), "\n"
    print "List of middleware deployments: ", t.get_middleware_deployments_table(), "\n"

    servers_list = t.get_middleware_servers_table()
    print "Full servers list: ", servers_list, "\n"


def test_details(web_session):

    t = table(web_session)

    datasources_table = t.get_middleware_datasource_table()
    ds_num = len(datasources_table)
    print "List of middleware datasources ({}): ".format(ds_num)
    t.pretty_print(datasources_table)

    print "\nList of middleware datasources: "
    t.pretty_print( t.get_datasource_details() )

    print "List of middleware providers: "
    t.pretty_print( t.get_providers_details())

    print "List of middleware deployments: "
    t.pretty_print( t.get_deployments_details())

    print "Middleware servers list: "
    t.pretty_print( t.get_servers_details())



