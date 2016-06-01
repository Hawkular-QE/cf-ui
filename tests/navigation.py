import pytest
from common.session import session
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from tree import NavigationTree
from . import UI_Route

@pytest.fixture (scope='session')
def web_session(request):
    web_session = session()

    def closeSession():
        print ("Close browser session")
        web_session.close_web_driver()
    request.addfinalizer(closeSession)
    return web_session

def test_navigation (web_session):
        driver = web_session.web_driver
        delay= 1
        tree = NavigationTree(driver)
        route = UI_Route("compute").add("middleware").add("middleware_deployments")
        tree.navigate(route, delay)

