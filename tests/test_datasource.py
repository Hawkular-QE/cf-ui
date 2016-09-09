import pytest
from common.session import session
from views.datasource import datasources

@pytest.fixture (scope='session')
def web_session(request):
    web_session = session(add_provider=False)

    def closeSession():
        web_session.logger.info("Close browser session")
        web_session.close_web_driver()
    request.addfinalizer(closeSession)

    return web_session

def test_cfui_datasource_list(web_session):
    web_session.logger.info("Begin datasource list test")
    assert datasources(web_session).validate_datasource_list()


def test_cfui_datasource_detail(web_session):
    web_session.logger.info("Begin datasource detail page test")
    assert datasources(web_session).validate_datasource_detail()


def test_cfui_delete_datasource_a(web_session):
    web_session.logger.info("Begin undeletable datasource test A")
    datasources(web_session).validate_delete_datasource_a()


def test_cfui_delete_datasource_b(web_session):
    web_session.logger.info("Begin undeletable datasource test B")
    datasources(web_session).validate_delete_datasource_b()

