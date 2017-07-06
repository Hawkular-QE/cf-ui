import pytest
from common.session import session
from views.mm_openshift_provider import mm_openshift_providers


@pytest.fixture (scope='session')
def web_session(request):
    web_session = session(add_provider=False)


    return web_session

def test_cfui_add_provider(web_session):
    provs = mm_openshift_providers(web_session)
    provs.add_mm_openshift_provider()