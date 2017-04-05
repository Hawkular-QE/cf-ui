import pytest
from common.session import session
from views.datasource import datasources
from views.servers import servers


@pytest.fixture (scope='session')
def web_session(request):
    web_session = session(add_provider=True)

    def closeSession():
        web_session.logger.info("Close browser session")
        web_session.close_web_driver()
    request.addfinalizer(closeSession)

    return web_session

def test_cfui_datasource_list(web_session):
    web_session.logger.info("Begin datasource list test (INV-011b)")
    assert datasources(web_session).validate_datasource_list()

def test_cfui_datasource_detail(web_session):
    web_session.logger.info("Begin datasource detail page test (INV-011b)")
    assert datasources(web_session).validate_datasource_detail()

def _test_cfui_delete_datasource_list_view(web_session):
    web_session.logger.info("Begin List view delete datasource test (OPR-036a)")
    assert servers(web_session).add_datasource("H2-Test")
    assert datasources(web_session).delete_datasource_list_view()

def test_cfui_delete_datasource_detail_view(web_session):
    web_session.logger.info("Begin Detail view delete datasource test (OPR-036a)")
    assert servers(web_session).add_datasource("H2-Test")
    assert datasources(web_session).delete_datasource_detail_view()