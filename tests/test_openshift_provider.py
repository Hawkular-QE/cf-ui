import pytest
from common.session import session
from views.mm_openshift_provider import mm_openshift_providers
from views.providers import providers
from views.eap_crosslink import eap_crosslink


@pytest.fixture (scope='session')
def web_session(request):
    web_session = session(add_provider=False)


    return web_session

def test_cfui_add_provider(web_session):
    provs = mm_openshift_providers(web_session)
    provs.add_mm_openshift_provider()

def test_add_middleware_provider(web_session):
    provs = providers(web_session)
    provs.add_provider()

def test_eap_crosslink(web_session):
    provs = eap_crosslink(web_session)
    provs.crosslink_eap()
