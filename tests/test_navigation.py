import pytest
from common.session import session
from time import sleep
from navigation.navigation import NavigationTree

@pytest.fixture (scope='session')
def web_session(request):
    web_session = session()

    def closeSession():
        print ("Close browser session")
        web_session.close_web_driver()
    request.addfinalizer(closeSession)
    return web_session

# to run 1 test at a time
# (by removing "sleep_*")
# due to the fact that Session closes browser (driver)
# TODO: clarify!

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


