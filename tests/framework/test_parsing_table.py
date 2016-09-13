import pytest
from common.session import session
from parsing.table import table
from navigation.navigation import NavigationTree

@pytest.fixture (scope='session')
def web_session(request):
    web_session = session()

    def closeSession():
        print ('Close browser session')
        web_session.close_web_driver()
    request.addfinalizer(closeSession)
    return web_session


def _test_cfui_instance(web_session):
    t = table(web_session)
    print "List of middleware datasources: ", t.get_middleware_datasources_table(), "\n"
    print "List of middleware providers: ", t.get_middleware_providers_table(), "\n"
    print "List of middleware deployments: ", t.get_middleware_deployments_table(), "\n"
    servers_list = t.get_middleware_servers_table()
    print "Full servers list: ", servers_list, "\n"


def _test_cfui_details(web_session):
    t = table(web_session)
    datasources_table = t.get_middleware_datasources_table()
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


def _test_cfui_single_detail_page(web_session):
    nav = NavigationTree(web_session)
    nav.jump_to_middleware_providers_view()
    nav.to_first_details()
    t = table(web_session)
    t.pretty_print(t.page_elements())


##   Example of usage routines
#    nav.found_by_pattern(pattern)
#    and table.page_as_dict()
#
#    If pattern matches to multiple instances would be used right first.
#    Take correct patterns!
#


def test_cfui_server_details_by_text(web_session):
    nav = NavigationTree(web_session)
    nav.jump_to_middleware_servers_view()

    server_pattern = "488ef4f1-9df2-4a79"
    if nav.found_by_pattern(server_pattern):
        t = table(web_session)
        t.pretty_print(t.page_as_dict())
    else:
        raise ValueError("Detail page is still unavailable")


def test_cfui_datasources_details_by_text(web_session):
    nav = NavigationTree(web_session)
    nav.jump_to_middleware_datasources_view()

    datasource_pattern = "vso-eap7.bc.jonqe.lab.eng.bos"
    if nav.found_by_pattern(datasource_pattern):
        t = table(web_session)
        t.pretty_print(t.page_as_dict())
    else:
        raise ValueError("Detail page is still unavailable")


def test_cfui_deployment_details_by_text(web_session):
    nav = NavigationTree(web_session)
    nav.jump_to_middleware_deployment_view()

    deployment_pattern = "hawkular-command-gateway-war"
    if nav.found_by_pattern(deployment_pattern):
        t = table(web_session)
        t.pretty_print(t.page_as_dict())
    else:
        raise ValueError("Detail page is still unavailable")


def test_cfui_provider_details_by_text(web_session):
    nav = NavigationTree(web_session)
    nav.jump_to_middleware_providers_view()

    provider_pattern = "10.16.23.195"
    if nav.found_by_pattern(provider_pattern):
        t = table(web_session)
        t.pretty_print(t.page_as_dict())
    else:
        raise ValueError("Detail page is still unavailable")
