import pytest
from common.session import session
from views.topology import topology
from common.db import db

@pytest.fixture (scope='session')
def web_session(request):
    web_session = session()

    def closeSession():
        web_session.logger.info("Close browser session")
        web_session.close_web_driver()
    request.addfinalizer(closeSession)

    return web_session

def test_cfui_validate_display_names_checkbox(web_session):
    assert topology(web_session).validate_display_names_checkbox()

def test_cfui_default_topology_view(web_session):
    assert topology(web_session).validate_default_topology_view()

def test_cfui_servers_entities(web_session):
    assert topology(web_session).validate_middleware_servers_entities()

def test_cfui_deployments_entities(web_session):
    assert topology(web_session).validate_middleware_deployments_entities()

def test_cfui_datasources_entities(web_session):
    assert topology(web_session).validate_middleware_datasources_entities()

def test_cfui_server_groups_entities(web_session):
    assert topology(web_session).validate_middleware_server_groups_entities()

def test_cfui_domains_entities(web_session):
    assert topology(web_session).validate_middleware_domains_entities()

def test_cfui_messaging_entities(web_session):
    assert topology(web_session).validate_middleware_messaging_entities()

def test_cfui_container_entities(web_session):
    if not db(web_session).is_container_provider_present(web_session.OPENSHIFT_PROVIDER_NAME):
        pytest.skip("Skip test - No Container Provider found.")
    assert topology(web_session).validate_middleware_container_entities()

