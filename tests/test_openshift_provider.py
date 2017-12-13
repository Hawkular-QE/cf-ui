import pytest
from common.session import session
from views.mm_openshift_provider import mm_openshift_providers


@pytest.fixture (scope='session')
def web_session(request):
    web_session = session(add_provider=True)
    return web_session

def test_cfui_add_provider(web_session):
    provs = mm_openshift_providers(web_session)
    provs.add_mm_openshift_provider()

def test_cfui_hawkular_Services_crosslink(web_session):
    provs = mm_openshift_providers(web_session)
    provs.verify_hawkular_Services_crosslink()

def test_cfui_hawkular_Services_topology_crosslink(web_session):
    provs= mm_openshift_providers(web_session)
    provs.verify_topology_crosslink_to_hawkular_services_container()

