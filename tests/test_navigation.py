import pytest
from common.session import session
from navigation.navigation import NavigationTree

@pytest.fixture (scope='session')
def web_session(request):
    web_session = session(add_provider=False)

    def closeSession():
        print ("Close browser session")
        web_session.close_web_driver()

    request.addfinalizer(closeSession)
    return web_session

def test_deployments (web_session):
    driver = web_session.web_driver
    nav = NavigationTree(driver)
    nav.navigate_to_middleware_deployment_view()

def sleep_test_providers (web_session):
    driver = web_session.web_driver
    nav = NavigationTree(driver)
    nav.navigate_to_middleware_providers_view()

def sleep_test_servers (web_session):
    driver = web_session.web_driver
    nav = NavigationTree(driver)
    nav.navigate_to_middleware_servers_view()


def sleep_test_topology(web_session):
    driver = web_session.web_driver
    nav = NavigationTree(driver)
    nav.navigate_to_topology_view()

def sleep_test_datasources(web_session):
    driver = web_session.web_driver
    nav = NavigationTree(driver)
    nav.navigate_to_middleware_datasources_view()

def test_all_navegitions_1(web_session):
    nav = NavigationTree(web_session.web_driver)
    nav.navigate_to_middleware_providers_view()
    nav.navigate_to_middleware_servers_view()
    nav.navigate_to_middleware_deployment_view()
    nav.navigate_to_middleware_datasources_view()
    nav.navigate_to_topology_view()

def _test_all_navigations_2(web_session):
    NavigationTree(web_session.web_driver).navigate_to_middleware_providers_view()
    NavigationTree(web_session.web_driver).navigate_to_middleware_servers_view()
    NavigationTree(web_session.web_driver).navigate_to_middleware_deployment_view()
    NavigationTree(web_session.web_driver).navigate_to_middleware_datasources_view()
    NavigationTree(web_session.web_driver).navigate_to_topology_view()
