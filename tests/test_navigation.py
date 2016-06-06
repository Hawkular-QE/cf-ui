import pytest
from common.session import session
from navigation.navigation import NavigationTree

@pytest.fixture (scope='session')
def web_session(request):
    web_session = session()

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


