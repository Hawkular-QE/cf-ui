import pytest
from common.session import session
from views.settings import settings

@pytest.fixture (scope='session')
def web_session(request):
    web_session = session(add_provider=True)

    def closeSession():
        web_session.logger.info("Close browser session")
        web_session.close_web_driver()

    request.addfinalizer(closeSession)

    return web_session


def test_settings_default_view(web_session):
    web_session.logger.info("Begin Settings Default View test")
    assert settings(web_session).default_view()

def test_providers_default_views(web_session):
    web_session.logger.info("Begin Providers Settings Default View test")
    assert settings(web_session).validate_providers_default_views()

def test_servers_default_views(web_session):
    web_session.logger.info("Begin Servers Settings Default View test")
    assert settings(web_session).validate_servers_default_views()

def test_deployments_default_views(web_session):
    web_session.logger.info("Begin Deployments Settings Default View test")
    assert settings(web_session).validate_deployments_default_views()

def test_datasources_default_views(web_session):
    web_session.logger.info("Begin Datasources Settings Default View test")
    assert settings(web_session).validate_datasources_default_views()

def test_messagings_default_views(web_session):
    web_session.logger.info("Begin Messagings Settings Default View test")
    assert settings(web_session).validate_messagings_default_views()

def test_settings_after_relogin(web_session):
    web_session.logger.info("Begin Settings After Logout/Login")
    assert settings(web_session).validate_settings_after_relogin()