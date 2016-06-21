import pytest
from common.session import session
from common.ui_utils import ui_utils
from parsing.table import table

class datasource():
    web_session = None

    def __init__(self, web_session):
        self.web_session = web_session
        self.web_driver = web_session.web_driver

    def list_datasource(self):
        elements_list = table(self.web_session).get_middleware_datasources_table()


        print (elements_list[2])

    def validate_datasource(self, text):
        table = []
        for tr in self.web_driver.find_elements_by_xpath('.//tr'):
            tds = tr.find_elements_by_tag_name('td')
            if tds:
                table.append([td.text for td in tds])
                for row in table:
                    for value in row:
                        if value == text:
                            return;