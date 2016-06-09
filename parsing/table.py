
class Table():

    """
    paths = dict({ 'middleware_servers'     : '/middleware_server/show_list'    },
                 { 'middleware_deployments' : '/middleware_deployment/show_list'},
                 { 'middleware_datasources' : '/middleware_datasource/show_list'},
                 { 'middleware_providers'   : '/ems_middleware/show_list'       }
                 )
    """

    keys = [ 'middleware_servers' ,         'middleware_deployments' ,          'middleware_datasources',           'middleware_providers'     ]
    urls = [ '/middleware_server/show_list','/middleware_deployment/show_list', '/middleware_datasource/show_list', '/ems_middleware/show_list' ]



    def __init__(self, web_session):
        self.web_session = web_session
        self.driver = web_session.web_driver
        self.paths = {key: value for key, value in zip(self.keys, self.urls)}

    """
    def __init__(self, web_session, url):
        self.__init__(web_session)
        #self.web_session = web_session
        #self.driver = web_session.web_driver
        #path = web_session.MIQ_HOSTNAME + url
        #self.paths = {key: value for key, value in zip(self.keys, self.urls)}
        self.driver.get(web_session.MIQ_HOSTNAME + url)
    """

    def from_url(self, url):
        self.driver.get(self.web_session.MIQ_HOSTNAME + url)
        return self


    def elements(self):

        list = self.driver.find_element_by_name("view_list")
        list.click()

        from time import sleep
        sleep(2)

        dictionary = dict()
        headers = []
        data = []

        theads = self.driver.find_elements_by_xpath('.//table//thead')
        table_rows = self.driver.find_elements_by_xpath('.//table//tbody//tr')


        for th in theads:
            ths = th.find_elements_by_tag_name('th')
            if ths:
                headers.append([td.text for td in ths])
        i = 0
        for table_row in table_rows:
            i += 1
            table_row_point = table_row.find_elements_by_tag_name('td')
            if table_row_point:

                head_iter = iter(headers[0])
                table_row_list = []
                dict_rows = []
                for td in table_row_point:

                    dict_row = {head_iter.next() : td.text}
                    table_row_list.append(dict_row)
                    dict_rows.append(table_row_list)

            dictionary.update({ "row_{}".format(i) : table_row_list})

        full_table = dict({"metadata": []})
        full_table.update({"row_array" : dictionary})

        #print "Headers: ", headers
        #print "Data: ", data
        #print "Dictionary (", type(full_table) is dict, "): ", full_table
        return full_table


    def provider_elements(self):
        ### TODO! Providers View has other table...
        dictionary = dict()
        headers = []
        data = []

        theads = self.driver.find_elements_by_xpath('.//table')
#        print "\n Tables? :", theads
        table_rows = self.driver.find_elements_by_xpath('.//table//tbody//tr')

        tables_point = self.driver.find_elements_by_xpath("id('#records_div')")
        #print tables_point

        tahs = theads[0].find_elements_by_tag_name('tr')

        for table in theads:
            #print table
            print table.tag_name
            trs = table.find_elements_by_tag_name('tr')
            #print "TRS: "
            for tr in trs:
                #print tr
                tds = tr.find_elements_by_tag_name('td')
                print "TDS"
                for td in tds:
                    #print td

                    if td.text != '':
                        print td.tag_name, " == ", td.text


#           if trs:
#              headers.append([td.text for td in trs])
        """
        i = 0
        for table_row in table_rows:
            i += 1
            table_row_point = table_row.find_elements_by_tag_name('td')
            if table_row_point:

                ### TODO! there is some issue here -> Providers View has other table...
                head_iter = iter(headers[0])

                table_row_list = []
                dict_rows = []
                for td in table_row_point:
                    dict_row = {head_iter.next(): td.text}
                    table_row_list.append(dict_row)
                    dict_rows.append(table_row_list)
            dictionary.update({"row_{}".format(i): table_row_list})

        full_table = dict({"metadata": []})
        full_table.update({"row_array": dictionary})
        """

        print "Headers: ", headers
        #print "Data: ", data
        #print "Dictionary (", type(full_table) is dict, "): ", full_table
        #return full_table




    def get_middleware_providers_table(self):
        return self.from_url( self.paths.get('middleware_providers')).elements()


    def get_middleware_servers_table(self):
        return self.from_url(self.paths.get('middleware_servers')).elements()


    def get_middleware_w_deployments_table(self):
        return self.from_url(self.paths.get('middleware_deployments')).elements()


    def get_middleware_datasources_table(self):
        return self.from_url(self.paths.get('middleware_datasources')).elements()

