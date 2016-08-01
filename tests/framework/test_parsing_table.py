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


def _test_details(web_session):
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

from navigation.navigation import NavigationTree
from time import sleep

def _test_single_detail_page(web_session):
    nav = NavigationTree(web_session)
    nav.jump_to_middleware_providers_view()
    nav.to_first_details()
    t = table(web_session)
    t.pretty_print(t.page_elements())

def test_details_by_text(web_session):

    nav = NavigationTree(web_session)
    nav.jump_to_middleware_servers_view()

    pattern = "488ef4f1-9df2-4a79"
    if nav.found_by_pattern(pattern):
        sleep(5)
        t = table(web_session)
        t.pretty_print(t.page_elements())
    else:
        raise ValueError("Detail page is still unavailable")


