
'''

Created on June 6, 2016

@author: pyadav

'''

class view():
    web_session = None

    def __init__(self,web_session):
        self.web_session = web_session
        self.web_driver = web_session.web_driver

    def grid_View(self):
        grid = self.web_driver.find_element_by_name("view_grid")
        grid.click()

    def tile_View(self):
        tile = self.web_driver.find_element_by_name("view_tile")
        tile.click()

    def list_View(self):
        list = self.web_driver.find_element_by_name("view_list")
        list.click()
