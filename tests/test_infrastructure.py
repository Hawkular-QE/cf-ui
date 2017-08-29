import pytest
from common.session import session
from views.infrastructures import infrastructures
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
    infra = infrastructures(web_session)
    infra.add_provider()

@pytest.fixture (scope='session')
def web_session(request):
    web_session = session(add_provider=False)

    def closeSession():
        web_session.logger.info("Close browser session")
        web_session.close_web_driver()
    request.addfinalizer(closeSession)

    return web_session

def test_cfui_add_provider(web_session):
    infra = infrastructures(web_session)
    infra.add_provider()

def test_cfui_update_provider(web_session):
    infra = infrastructures(web_session)
    infra.update_provider()

def test_cfui_delete_all_infrastructures(web_session):
    infra = infrastructures(web_session)
    infra.add_provider()
    infra.delete_provider(delete_all_providers=True)

def test_cfui_delete_single_provider(web_session):
    infra = infrastructures(web_session)
    infra.add_provider()
    infra.delete_hawkular_provider()

def test_cfui_validate_infrastructures_list(web_session):
    infra = infrastructures(web_session)
    infra.add_provider()
    assert infra.validate_infrastructures_list()

def test_cfui_validate_infrastructures_details(web_session):
    assert infrastructures(web_session).validate_infrastructures_details()

def test_cfui_recheck_authentication(web_session):
    assert infrastructures(web_session).recheck_authentication()

def test_cfui_validate_eap_rhevm_crosslink(web_session):
    web_session.logger.info("[INV008] Validate eap, rhevm, MIQ crosslink relationship")
    infra = infrastructures(web_session)
    infra.add_provider(delete_if_provider_present=False, validate_provider=True)
    # todo change providers
    provider = providers(web_session)
    provider.add_provider(delete_if_provider_present=False, validate_provider=True)
    # steps:
    # navigate to vm, get its vm_name, IP,hostname
    infra.navigate_to_vm_view()
    # todo
    # go to middleware provider (hawkular) get eap by its name
    # (either in conf/properties.properties or matching/contains VM name)
    # validate that link exists and its vm_name, IP, hostname matches