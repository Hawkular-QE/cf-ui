import pytest
from common.session import session
from views.providers import providers
from views.menu import menu


@pytest.fixture (scope='session')
def web_session(request):
    web_session = session(add_provider=True)

    def closeSession():
        web_session.logger.info("Close browser session")
        web_session.close_web_driver()
    request.addfinalizer(closeSession)

    return web_session

#def test_cfui_verify_summary_and_relationships_links(web_session):
#    provs = providers(web_session)
#    provs.add_provider(delete_if_provider_present=False)
#    m = menu(web_session)
#    m.validate_all_middleware_summary_and_relationships()

def test_cfui_verify_summary_and_relationships_links_providers(web_session):
    provs = providers(web_session)
    provs.add_provider(delete_if_provider_present=False)
    m = menu(web_session)
    m.navigate_to_middleware()

def test_cfui_verify_summary_and_relationships_links_domains(web_session):
    provs = providers(web_session)
    provs.add_provider(delete_if_provider_present=False)
    m = menu(web_session)
    m.navigate_to_middleware("middleware_domain", "Name")


def test_cfui_verify_summary_and_relationships_links_servers(web_session):
    provs = providers(web_session)
    provs.add_provider(delete_if_provider_present=False)
    m = menu(web_session)
    m.navigate_to_middleware("middleware_server", "Feed")


def test_cfui_verify_summary_and_relationships_links_deployments(web_session):
    provs = providers(web_session)
    provs.add_provider(delete_if_provider_present=False)
    m = menu(web_session)
    m.navigate_to_middleware("middleware_deployment", "Deployment Name")


def test_cfui_verify_summary_and_relationships_links_datasources(web_session):
    provs = providers(web_session)
    provs.add_provider(delete_if_provider_present=False)
    m = menu(web_session)
    m.navigate_to_middleware("middleware_datasource", "Datasource Name")


def test_cfui_verify_summary_and_relationships_links_messaging(web_session):
    provs = providers(web_session)
    provs.add_provider(delete_if_provider_present=False)
    m = menu(web_session)
    m.navigate_to_middleware("middleware_messaging", "Messaging Name")
