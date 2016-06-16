from common.ui_utils import ui_utils
from selenium.webdriver.common.by import By

class table():

    paths = {
                'middleware_servers'     : '/middleware_server/show_list',
                'middleware_deployments' : '/middleware_deployment/show_list',
                'middleware_datasources' : '/middleware_datasource/show_list',
                'middleware_providers'   :  '/ems_middleware/show_list'
            }


    def __init__(self, web_session):
        self.web_session = web_session
        self.driver = web_session.web_driver

    def from_url(self, url):
        self.driver.get(self.web_session.MIQ_URL + url)
        # wait 60 sec till data appears
        ui_utils(self.web_session).waitForTextOnPage("No Records Found.",60, exist=False)
        return self

    def elements(self):
        list = self.driver.find_element_by_name("view_list")
        list.click()

        dictionary = []
        headers = []
        theads = self.driver.find_elements_by_xpath('.//table//thead')
        table_rows = self.driver.find_elements_by_xpath('.//table//tbody//tr')

        for th in theads:
            ths = th.find_elements_by_tag_name('th')
            if ths:
                headers.append([td.text for td in ths])
        row_number = 0
        for table_row in table_rows:
            row_number += 1
            table_row_point = table_row.find_elements_by_tag_name('td')
            if table_row_point:

                head_iter = iter(headers[0])
                table_row_list = []
                cell = dict()
                for td in table_row_point:

                    head_next = head_iter.next()
                    if head_next != '':
                        cell.update({ head_next : td.text })
                        table_row_list = cell

            dictionary.append( table_row_list)
        return dictionary


    def get_middleware_providers_table(self):
        return self.from_url( self.paths.get('middleware_providers')).elements()

    def get_middleware_servers_table(self):
        return self.from_url(self.paths.get('middleware_servers')).elements()

    def get_middleware_deployments_table(self):
        return self.from_url(self.paths.get('middleware_deployments')).elements()

    def get_middleware_datasources_table(self):
        return self.from_url(self.paths.get('middleware_datasources')).elements()

