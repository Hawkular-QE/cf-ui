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


def _test_deployments (web_session):
    nav = NavigationTree(web_session)
    nav.navigate_to_middleware_deployment_view()

def _test_providers (web_session):
    nav = NavigationTree(web_session)
    nav.navigate_to_middleware_providers_view()

def _test_servers (web_session):
    nav = NavigationTree(web_session)
    nav.navigate_to_middleware_servers_view()


def _test_topology(web_session):
    nav = NavigationTree(web_session)
    nav.navigate_to_topology_view()


def _test_datasources(web_session):
    nav = NavigationTree(web_session)
    nav.navigate_to_middleware_datasources_view()

def _test_all_navigations_1(web_session):
    nav = NavigationTree(web_session)
    nav.navigate_to_middleware_providers_view()
    nav.navigate_to_middleware_servers_view()
    nav.navigate_to_middleware_deployment_view()
    nav.navigate_to_middleware_datasources_view()
    nav.navigate_to_topology_view()

def _test_all_navigations_2(web_session):
    NavigationTree(web_session).navigate_to_middleware_providers_view()
    NavigationTree(web_session).navigate_to_middleware_servers_view()
    NavigationTree(web_session).navigate_to_middleware_deployment_view()
    NavigationTree(web_session).navigate_to_middleware_datasources_view()
    NavigationTree(web_session).navigate_to_topology_view()

def _test_fast_navigation(web_session):
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


def test_cfui_provider_details(web_session):
    NavigationTree(web_session).jump_to_middleware_providers_view().to_exact_details(1) ## Visual numeration from 1 !!


def test_cfui_deployment_details(web_session):
    NavigationTree(web_session).jump_to_middleware_deployment_view().to_exact_details(5)
    NavigationTree(web_session).jump_to_middleware_deployment_view().to_first_details()
    NavigationTree(web_session).jump_to_middleware_deployment_view().to_last_details()


def test_cfui_server_details(web_session):
    NavigationTree(web_session).jump_to_middleware_servers_view().to_exact_details(2)


def test_cfui_datasource_details(web_session):
    NavigationTree(web_session).jump_to_middleware_datasources_view().to_exact_details(2)


def test_cfui_domain_details(web_session):
    # +
    NavigationTree(web_session).jump_to_middleware_domain_view().to_exact_details(1)

    # -
    try:
        NavigationTree(web_session).jump_to_middleware_domain_view().to_exact_details(17)
        raise ValueError("Uncaught Exception!!")
    except(AssertionError):
        print "OK - negative test for number of domain"


def test_cfui_negative_domain_details(web_session):
    nav = NavigationTree(web_session).jump_to_middleware_domain_view()
    try:
        nav.to_exact_details('nonexistent')
        raise ValueError("Uncaught Exception!!")
    except(AssertionError):
        print "OK - negative test for key words"


