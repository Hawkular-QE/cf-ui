import pytest
from common.session import session
from views.datasource import datasources
from navigation.navigation import NavigationTree
from time import sleep


@pytest.fixture (scope='session')
def web_session(request):
    web_session = session(add_provider=True)

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

def test_cfui_datasource_detail(web_session):
    web_session.logger.info("Begin datasource detail page test")
    assert datasources(web_session).validate_datasource_detail()

def test_cfui_delete_datasource_a(web_session):
    web_session.logger.info("Begin undeletable datasource test A")
    driver = web_session.web_driver
    ds = datasources(web_session)
    nav = NavigationTree(web_session).jump_to_middleware_datasources_view().to_first_details()
    number_before = ds.count_datasources()
    nav.select_and_click('Operations', 'Remove')
    alert = driver.switch_to_alert()
    alert.accept()
    number_after = ds.count_datasources()
    assert number_before == number_after+1, "== BUG STILL PRESENT. =="

    #assert number_before == number_after+1, "Bug still present."

def test_cfui_delete_datasource_b(web_session):
    web_session.logger.info("Begin undeletable datasource test B")
    driver = web_session.web_driver
    ds = datasources(web_session)
    nav = NavigationTree(web_session).jump_to_middleware_datasources_view()
    number_before = ds.count_datasources()
    nav.check_first_datasource()
    nav.select_and_click('Operations', 'Remove')
    sleep(3)
    alert = driver.switch_to_alert()
    alert.accept()
    number_after = ds.count_datasources()
    assert number_before == number_after + 1, "== BUG STILL PRESENT. =="
