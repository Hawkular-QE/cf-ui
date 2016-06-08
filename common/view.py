from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from common.ui_utils import ui_utils
from common.session import session

'''

Created on June 6, 2016



@author: pyadav

'''

class view():
    web_session = None

    def __init__(self,web_session):

        self.web_session = web_session

        self.web_driver = web_session.web_driver




    def gridView(self):

        grid = self.web_driver.find_element_by_name("view_grid")
        grid.click()


    def tileView(self):


        tile = self.web_driver.find_element_by_name("view_tile")
        tile.click()

    def listView(self):

        list = self.web_driver.find_element_by_name("view_list")
        list.click()
