
class Table():

    keys = [ 'middleware_servers' ,         'middleware_deployments' ,          'middleware_datasources',           'middleware_providers'     ]
    urls = [ '/middleware_server/show_list','/middleware_deployment/show_list', '/middleware_datasource/show_list', '/ems_middleware/show_list' ]


    def __init__(self, web_session):
        self.web_session = web_session
        self.driver = web_session.web_driver
        self.paths = {key: value for key, value in zip(self.keys, self.urls)}

    def from_url(self, url):
        self.driver.get(self.web_session.MIQ_HOSTNAME + url)
        return self


    def elements(self):
        list = self.driver.find_element_by_name("view_list")
        list.click()

        dictionary = dict()
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
                dict_rows = []
                for td in table_row_point:

                    dict_row = {head_iter.next() : td.text}
                    table_row_list.append(dict_row)
                    dict_rows.append(table_row_list)

            dictionary.update({ "row_{}".format(row_number) : table_row_list})

        full_table = dict({"metadata": []})
        full_table.update({"row_array" : dictionary})

        return full_table


    def get_middleware_providers_table(self):
        return self.from_url( self.paths.get('middleware_providers')).elements()


    def get_middleware_servers_table(self):
        return self.from_url(self.paths.get('middleware_servers')).elements()


    def get_middleware_w_deployments_table(self):
        return self.from_url(self.paths.get('middleware_deployments')).elements()


    def get_middleware_datasources_table(self):
        return self.from_url(self.paths.get('middleware_datasources')).elements()

