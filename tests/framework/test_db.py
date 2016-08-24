import pytest
from common.session import session
from common.db import db

@pytest.fixture (scope='session')
def web_session(request):
    web_session = session(add_provider=False, login=False)

    def closeSession():
        web_session.logger.info("Close browser session")
        web_session.close_web_driver()
    request.addfinalizer(closeSession)

    return web_session

def test_cfui_db_datasources(web_session):
    rows = db(web_session).get_datasources()
    assert rows
    for row in rows:
        print "name: ", row.get('name')

def test_cfui_db_servers(web_session):
    rows = db(web_session).get_servers()
    assert rows
    for row in rows:
        print "product: ", row.get('product')

def test_cfui_db_deployments(web_session):
    rows = db(web_session).get_deployments()
    assert rows
    for row in rows:
        print "name: ", row.get('name')

def test_cfui_db_domains(web_session):
    rows = db(web_session).get_domains()
    assert rows
    for row in rows:
        print "name: ", row.get('name')