
class table():

    paths = {
                'middleware_servers'     : '/middleware_server/show_list',
                'middleware_deployments' : '/middleware_deployment/show_list',
                'middleware_datasources' : '/middleware_datasource/show_list',
                'middleware_providers'   : '/ems_middleware/show_list',
                'middleware_domains'     : '/middleware_domain/show_list',
                'middleware_datasources_details': '/middleware_datasource/show/{}',
    }

    def __init__(self, web_session):
        self.web_session = web_session
        self.driver = web_session.web_driver

    # temporary while fast navigation is merged
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

    ## TODO: utils for usage in navigation (move to navigation.py)

    def is_url(self):
        pass
    def is_path(self):
        pass

    def build_subtree(self, target):
        """
        if target.is_url:
            self.from_url(target)
        else:
            if target.is_path():
                self.from_path(target)
        else:
            print "Wrong target!"
        """
        self.from_path(target)
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
            table_row_list = [] ## ??
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

    def page_elements(self):

        print "Page URL: ", self.driver.current_url

        dictionary = {}
        table_locator = ".//table//tbody//tr[not(ancestor::tr)]"
        table_rows = self.driver.find_elements_by_xpath(table_locator)

        for table_row in table_rows:
            print "\n > table row: ", table_row.text
            tds = table_row.find_elements_by_tag_name("td")
            property_name = "'{}'".format(tds[0].text)
            print "tds's size: ", len(tds), " -- property_name: ", property_name
            property_value = None

            if len(tds) == 1:
                property_value = "is empty"

            if len(tds) == 2:
                property_value = "'{}'".format(tds[1].text)
            inner_rows = table_row.find_elements_by_xpath(".//table//tbody//tr")

            if inner_rows:
                inner_elem = " '{}' ".format( "".join([inner.text for inner in inner_rows]))
                property_value = inner_elem

            if property_name != None and property_name != "":
                dictionary.update( { property_name : property_value })
        return dictionary



    def details(self):
        table = []
        dict = {}

        for tr in self.driver.find_elements_by_xpath('.//tbody/tr'):
            tds = tr.find_elements_by_tag_name('td')
            if tds:
                table.append([td.text for td in tds])
                for pair in table:
                    #dict[pair[0]] = pair[1]
                    print " pair > ", pair
            else:
                self.web_session.logger.warning("No element found for table.")
        return dict


    def get_leaf(self, number):
        leaf = self.details()
        dict_size = len(leaf)
        leaf.update({'web_page': self.driver.current_url})
        leaf.update({'Length': dict_size})
        if dict_size == 0:
            leaf.update({'Message': 'Unexpected error encountered'})
        return leaf

    def get_page_details(self, page):
        details = []
        req_path  = self.paths.get(page)
        urls = self.from_path(req_path).get_leaves_urls()
        for url in urls:
            self.from_url(url)
            details.append(self.details())
        return details


    def get_middleware_providers_table(self):
        return self.from_path( self.paths.get('middleware_providers')).elements()


    def get_middleware_servers_table(self):
        return self.from_path(self.paths.get('middleware_servers')).elements()


    def get_middleware_deployments_table(self):
        return self.from_path(self.paths.get('middleware_deployments')).elements()


    def get_middleware_datasources_table(self):
        return self.from_path(self.paths.get('middleware_datasources')).elements()

    def get_middleware_domains_table(self):
        return self.from_path(self.paths.get('middleware_domains')).elements()

    def get_leaves_refs(self):
        from lxml import etree
        d = etree.HTML(self.driver.page_source)
        xpath_selector = ".//tbody/tr/td/input[@class='list-grid-checkbox']/@value"
        values = d.xpath(xpath_selector)
        return values


    def get_leaves_urls(self):
        base_url = self.driver.current_url.replace("/show_list", "/show/")
        urls = [ base_url+value for value in self.get_leaves_refs()]
        return urls


    def get_page_details_ref(self, page, ref):
        base_path = self.paths.get(page)
        sub_path = base_path.replace("/show_list", "/show/")
        target = "{}/{}".format(sub_path, ref)
        return self.build_subtree(target).get_leaf(ref)


    def get_datasource_details(self):
        return self.get_page_details('middleware_datasources')

    def get_datasource_details_ref(self, ref):
        return self.get_page_details_ref('middleware_datasource', ref)


    def get_servers_details(self):
        return self.get_page_details('middleware_servers')

    def get_servers_details_ref(self, ref):
        return self.get_page_details_ref('middleware_servers', ref)


    def get_providers_details(self):
        return self.get_page_details('middleware_providers')

    def get_providers_detail_ref(self, ref):
        return self.get_page_details_ref('middleware_providers', ref)


    def get_deployments_details(self):
        return self.get_page_details('middleware_deployments')

    def get_deployments_details_ref(self, ref):
        return self.get_page_details_ref('middleware_deployments', ref)

    ## TODO: next - to use python's magics with method's names substitution for eliminate this spagetti! -^^

    def pretty_print(self, complex_data, caption="DUMP: "):
        import pprint as pp
        print caption
        pp.pprint(complex_data)
