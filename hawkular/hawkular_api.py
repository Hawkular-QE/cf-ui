from mgmtsystem.hawkular import Hawkular

class hawkular_api():
    web_session = None
    __hawkular__ = None

    def __init__(self, web_session):
        self.web_session = web_session
        self.__hawkular__ = Hawkular(hostname=web_session.HAWKULAR_HOSTNAME, port=web_session.HAWKULAR_PORT,
                                     username=web_session.HAWKULAR_USERNAME, password=web_session.HAWKULAR_PASSWORD)

    # Hide the Hawkular object, but provide ability to get and use if need be
    def get_hawkular(self):
        return self.__hawkular__

    def __exception_handler(self, e):
        assert False, "Hawkular Server {} failed to connect, Exception: {}".format(self.web_session.HAWKULAR_HOSTNAME, e)

    def get_hawkular_servers(self):
        servers = []

        try:
            rows = self.__hawkular__.list_server()
        except Exception, e:
            self.__exception_handler(e)

        for server in rows:
            dict = {}
            dict['Server Name'] = server.id.strip('~')
            dict['Product Name'] = server.data['Name']
            dict['Host Name'] = server.data['Hostname']
            dict['Feed'] = server.path.feed
            dict['Provider'] = self.web_session.PROVIDER
            dict['details'] = server.data
            servers.append(dict)

        return servers

    def get_hawkular_datasources(self):
        datasources = []

        try:
            rows = self.__hawkular__.list_server_datasource()
        except:
            self.__exception_handler()

        for datasource in rows:
            dict = {}
            dict['Nativeid'] = datasource.id
            dict['Name'] = datasource.name
            dict['path'] = datasource.path
            datasources.append(dict)

        return datasources

    def get_hawkular_deployments(self):
        deployments = []

        try:
            rows = self.__hawkular__.list_server_deployment()
        except:
            self.__exception_handler()

        for deployment in rows:
            dict = {}
            dict['Nativeid'] = deployment.id
            dict['Name'] = deployment.name
            dict['path'] = deployment.path
            deployments.append(dict)

        return deployments

    def generic_for_testing(self):
        return self.__hawkular__.list_server_deployment()