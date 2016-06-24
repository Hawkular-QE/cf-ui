
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

def test_single_detail_page(web_session):

    t = table(web_session)

    """
    Suppose we want to get details of some deployment.
    Before it is necessary to get list of references from main page of Deployments by method table.get_leaves_refs()
    Firstly we need to build DOM sub-tree, i.e., navigate to Middleware Deployment page...
    and then get list of refs
    """
    from navigation.navigation import NavigationTree

    NavigationTree(web_session).navigate_to_middleware_deployment_view()

    print "List of refs (unsorted): ",\
        t.get_leaves_refs()

    """
    Now we can choose actual values of references, and use it to fetch actual Deployment Details
    """

    ref = '8'
    t.pretty_print(t.get_deployments_details_ref(ref), caption="Deployment Details: ")