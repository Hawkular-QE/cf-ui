
class table():

    paths = {
                'middleware_servers'     : '/middleware_server/show_list',
                'middleware_deployments' : '/middleware_deployment/show_list',
                'middleware_datasources' : '/middleware_datasource/show_list',
                'middleware_providers'   : '/ems_middleware/show_list',
                'middleware_datasources_details': '/middleware_datasource/show/{}',
    }

    def __init__(self, web_session):
        self.web_session = web_session
        self.driver = web_session.web_driver

    def is_url_different(self, url):
        return (self.driver.current_url != url)

    def from_path(self, path):
        url = self.web_session.MIQ_URL + path
        if self.is_url_different(url):
            self.driver.get(self.web_session.MIQ_URL + path)
        return self

    def from_url(self, url):
        if self.is_url_different(url):
            self.driver.get(url)
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


    def details(self):
        table = []
        dict = {}
        for tr in self.driver.find_elements_by_xpath('.//tbody/tr'):
            tds = tr.find_elements_by_tag_name('td')
            if tds:
                table.append([td.text for td in tds])
                for pair in table:
                    dict[pair[0]] = pair[1]
            else:
                self.web_session.logger.warning("No element found for table.")
        return dict

    def get_leaf(self, page, number):
        leaf = []
        req_path = self.paths.get(page)
        leaf_url = req_path.replace("/show_list", "/show/")
        leaf = self.from_url(leaf_url).details()
        dict_size = len(leaf)
        leaf.update({'web_page': leaf_url})
        leaf.update({'Length': dict_size})
        if dict_size == 0:
            leaf.update({'Message': 'Unexpected error encountered'})
        return leaf

    def get_page_details(self, page):
        details = []
        req_path  = self.paths.get(page)

        urls = self.from_path(req_path).get_leafes_urls()
        for url in urls:
            #details.append(self.get_leaf(req_path, n ))

            table = self.from_url(url).details()

            # additional metadata
            dict_size = len(table)
            page = self.driver.current_url
            table.update({'web_page' : page})
            table.update({'Length' : dict_size })
            if dict_size == 0:
                table.update({'Message' : 'Unexpected error encountered'})
            details.append(table)
        return details


    def get_middleware_providers_table(self):
        return self.from_path( self.paths.get('middleware_providers')).elements()


    def get_middleware_servers_table(self):
        return self.from_path(self.paths.get('middleware_servers')).elements()


    def get_middleware_deployments_table(self):
        return self.from_path(self.paths.get('middleware_deployments')).elements()


    def get_middleware_datasource_table(self):
        return self.from_path(self.paths.get('middleware_datasources')).elements()


    def get_leafes_urls(self):
        from lxml import etree
        d = etree.HTML(self.driver.page_source)
        xpath_selector = ".//tbody/tr/td/input[@class='list-grid-checkbox']/@value"
        values = d.xpath(xpath_selector)
        base_url = self.driver.current_url.replace("/show_list", "/show/")
        urls = [ base_url+value for value in values]
        return urls

    """
    def get_leaf(self, url):
        return self.from_url(url).details()


    def get_all(self):
        all = []
        for url in self.get_leafes_urls():
            all.append( self.get_leaf(url) )
        return all
    """

    def get_datasource_details(self):
        return self.get_page_details('middleware_datasources')

    def get_datasource_details_of(self, offset):
        return self.get_page_details('middleware_datasources')

    def get_servers_details(self):
        return self.get_page_details('middleware_servers')


    def get_providers_details(self):
        return self.get_page_details('middleware_providers')


    def get_deployments_details(self):
        return self.get_page_details('middleware_deployments')


    def pretty_print(self, complex_data):
        import pprint as pp
        pp.pprint(complex_data)
