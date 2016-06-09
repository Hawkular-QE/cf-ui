import pytest
from common.session import session
from common.view import view
from navigation.navigation import NavigationTree
'''

Created on June 8, 2016



@author: pyadav

'''

@pytest.fixture (scope='session')
def web_session(request):
    web_session = session()
    return web_session

def test_view(web_session):
    driver = web_session.web_driver
    nav = NavigationTree(driver)
    nav.navigate_to_middleware_deployment_view()
    viewHaw = view(web_session)
    print ("Show Grid View")
    viewHaw.grid_View()
    print ("Show Tile View")
    viewHaw.tile_View()
    print ("Show List View")
    viewHaw.list_View()