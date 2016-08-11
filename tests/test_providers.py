import pytest
from common.session import session
from views.providers import providers


@pytest.fixture (scope='session')
def web_session(request):
    web_session = session(add_provider=False)

    def closeSession():
        web_session.logger.info("Close browser session")
        web_session.close_web_driver()
    request.addfinalizer(closeSession)

    return web_session

def test_cfui_add_provider(web_session):
    provs = providers(web_session)
    provs.add_provider()

def test_cfui_update_provider(web_session):
    provs = providers(web_session)
    provs.update_provider()

def test_cfui_delete_all_providers(web_session):
    provs = providers(web_session)
    provs.add_provider()
    provs.delete_provider(delete_all_providers=True)

def test_cfui_delete_single_provider(web_session):
    provs = providers(web_session)
    provs.add_provider()
    provs.delete_hawkular_provider()

def test_cfui_validate_providers_list(web_session):
    provs = providers(web_session)
    provs.add_provider()
    assert provs.validate_providers_list()

def test_cfui_validate_providers_details(web_session):
    assert providers(web_session).validate_providers_details()

def test_cfui_recheck_authentication(web_session):
    assert providers(web_session).recheck_authentication()

