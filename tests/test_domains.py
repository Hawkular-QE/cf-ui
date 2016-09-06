import pytest
from common.session import session
from views.domains import domains


@pytest.fixture (scope='session')
def web_session(request):
    web_session = session(add_provider=True)

    def closeSession():
        web_session.logger.info("Close browser session")
        web_session.close_web_driver()
        request.addfinalizer(closeSession)

    return web_session

def test_cfui_domains_view(web_session):
    web_session.logger.info("Begin Domains View")
    assert domains(web_session).validate_domains_list()

def test_cfui_domain_details(web_session):
    web_session.logger.info("Begin Domain Details")
    assert domains(web_session).validate_domain_details()