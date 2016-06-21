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

    def get_hawkular_servers_list(self):
        list = self.__hawkular__.list_server()
        return list

    def get_hawkular_datasource_list(self):
        list = self.__hawkular__.list_server_datasource()
        return list

    def get_hawkular_deployments_list(self):
        list = self.__hawkular__.list_server_deployment()
        return list

    def generic_for_testing(self):
        return self.__hawkular__.list_resource()