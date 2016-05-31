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

target_miq = 'https://10.16.5.131'
driver = webdriver.Firefox()
driver.get(target_miq)
sleep(5)
do_click = False

@pytest.fixture (scope='session')
def miq_login(web_session):

    userName = driver.find_element_by_id("user_name")
    userName.send_keys("admin")
    userPass = driver.find_element_by_id("user_password")
    userPass.send_keys("smartvm")
    loginButton = driver.find_element_by_id("login")
    loginButton.click()
    sleep(5)
    pass

def test_tree(miq_login):

    hover = ActionChains(driver)

    compute = driver.find_element_by_xpath(".//*[@id='maintab']/li[3]/a/span[2]")
    hover.move_to_element(compute)
    hover.perform()
    sleep(3)

    middleware = compute.find_element_by_xpath("//span[contains(.,'Middleware')]")
    hover.move_to_element(middleware)
    hover.perform()
    if do_click:
        middleware.click()
    sleep(3)

    middleware_providers = middleware.find_element_by_xpath("//span[contains(.,'Providers')]")
    hover.move_to_element(middleware_providers)
    hover.perform()
    if do_click:
        middleware_providers.click()
    sleep(3)

    middleware_servers = middleware.find_element_by_xpath("//span[contains(.,'Middleware Servers')]")
    hover.move_to_element(middleware_servers)
    hover.perform()
    if do_click:
        middleware_servers.click()
    sleep(3)

    middleware_deployments = middleware.find_element_by_xpath("//span[contains(.,'Middleware Deployments')]")
    hover.move_to_element(middleware_deployments)
    hover.perform()
    if do_click:
        middleware_deployments.click()
    sleep(3)

    middleware_datasources = middleware.find_element_by_xpath("//span[contains(.,'Topology')]")
    hover.move_to_element(middleware_datasources)
    hover.perform()
    if do_click:
        middleware_datasources.click()
    sleep(3)

    topology = middleware.find_element_by_xpath("//span[@class='list-group-item-value']")
    hover.move_to_element(topology)
    hover.perform()
    if do_click:
        topology.click()
    sleep(3)

def test_navigation(miq_login):
    """ Demo mode. For real usage set do_click to True before necessary branch """

    tree = NavigationTree(driver)
    route = UI_Route("compute").add("middleware").add("middleware_deployments")
    tree.navigate(route)
    pass
