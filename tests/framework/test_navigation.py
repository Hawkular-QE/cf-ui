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

def _test_cfui_zero (web_session):
    print "(Zero test)"

def _test_cfui_deployments (web_session):
    nav = NavigationTree(web_session)
    nav.navigate_to_middleware_deployment_view()

def _test_cfui_providers (web_session):
    nav = NavigationTree(web_session)
    nav.navigate_to_middleware_providers_view()

def _test_cfui_servers (web_session):
    nav = NavigationTree(web_session)
    nav.navigate_to_middleware_servers_view()


def _test_cfui_topology(web_session):
    nav = NavigationTree(web_session)
    nav.navigate_to_topology_view()


def _test_cfui_datasources(web_session):
    nav = NavigationTree(web_session)
    nav.navigate_to_middleware_datasources_view()


def _test_cfui_all_navigations_1(web_session):
    nav = NavigationTree(web_session)
    nav.navigate_to_middleware_providers_view()
    nav.navigate_to_middleware_servers_view()
    nav.navigate_to_middleware_deployment_view()
    nav.navigate_to_middleware_datasources_view()
    nav.navigate_to_topology_view()

def test_cfui_all_navigations_2(web_session):
    NavigationTree(web_session).navigate_to_middleware_providers_view()
    NavigationTree(web_session).navigate_to_middleware_servers_view()
    NavigationTree(web_session).navigate_to_middleware_deployment_view()
    NavigationTree(web_session).navigate_to_middleware_datasources_view()
    NavigationTree(web_session).navigate_to_topology_view()

def _test_cfui_fast_navigation(web_session):
    nav = NavigationTree(web_session)

    nav.jump_to_middleware_datasources_view()
    nav.jump_to_middleware_datasources_view(force_navigation=False)
    nav.jump_to_middleware_datasources_view(force_navigation=True)

    nav.jump_to_middleware_deployment_view()
    nav.jump_to_middleware_deployment_view(force_navigation=True)
    nav.jump_to_middleware_deployment_view(force_navigation=False)

    nav.jump_to_middleware_providers_view()
    nav.jump_to_middleware_servers_view()
    nav.jump_to_topology_view()

