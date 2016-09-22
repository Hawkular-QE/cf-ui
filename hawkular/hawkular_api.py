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
            rows = self.__hawkular__.inventory.list_server()
        except Exception, e:
            self.__exception_handler(e)

        for server in rows:
            dict = {}
            dict['Server Name'] = server.id.strip('~')
            dict['Product Name'] = server.data.get('Product Name')
            dict['Host Name'] = server.data.get('Hostname')
            dict['UUID'] = server.data.get('UUID')
            dict['Feed'] = server.path.feed_id
            dict['Provider'] = self.web_session.PROVIDER
            dict['details'] = server.data
            servers.append(dict)

        return servers

    def get_hawkular_datasources(self):
        datasources = []

        try:
            rows = self.__hawkular__.inventory.list_server_datasource()
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
            rows = self.__hawkular__.inventory.list_server_deployment()
        except:
            self.__exception_handler()

        for deployment in rows:
            dict = {}
            dict['Nativeid'] = deployment.id
            dict['Name'] = deployment.name
            dict['path'] = deployment.path
            deployments.append(dict)

        return deployments

    def get_hawkular_domains(self, feed_id = None):
        domains = []

        try:
            rows = self.__hawkular__.inventory.list_domain(feed_id)
        except:
            self.__exception_handler()

        for domain in rows:
            dict = {}
            dict['id'] = domain.id
            dict['name'] = domain.name
            dict['path'] = domain.path
            dict['data'] = domain.data
            domains.append(dict)

        return domains

    def get_hawkular_server_groups(self, feed_id):
        server_groups = []

        try:
            rows = self.__hawkular__.inventory.list_server_group(feed_id)
        except:
            self.__exception_handler()

        for group in rows:
            dict = {}
            dict['id'] = group.id
            dict['name'] = group.name
            dict['path'] = group.path
            dict['data'] = group.data
            server_groups.append(dict)

        return server_groups

    def get_hawkular_messaging(self):
        messaging = []

        try:
            rows = self.__hawkular__.inventory.list_messaging()
        except:
            self.__exception_handler()

        for message in rows:
            dict = {}
            dict['id'] = message.id
            dict['name'] = message.name
            dict['path'] = message.path
            messaging.append(dict)

        return messaging

    def get_port(self):
        try:
            return self.__hawkular__.port
        except:
            self.__exception_handler()

    def get_ip_address(self):
        try:
            return self.__hawkular__.get_ip_address
        except:
            self.__exception_handler()

        def generic_for_testing(self):
            return self.__hawkular__.list_server()

    ''' Alerts '''

    def get_alert_list_event(self):
        # TO-DO: Return formatted Dict
        try:
            return self.__hawkular__.alert.list_event()
        except:
            self.__exception_handler()

    def get_alert_auth(self):
        try:
            auth =  self.__hawkular__.alert.auth
        except:
            self.__exception_handler()

        auth_dict = {}
        auth_dict['username'] = auth[0]
        auth_dict['password'] = auth[1]

        return auth_dict

    def get_alert_tenant_id(self):
        try:
            return self.__hawkular__.alert.tenant_id
        except:
            self.__exception_handler()

    def get_alert_hostname(self):
        try:
            return self.__hawkular__.alert.hostname
        except:
            self.__exception_handler()

    def get_alert_status(self):
        try:
            return self.__hawkular__.alert.status()
        except:
            self.__exception_handler()

    ''' Metrics '''

    def get_metric_hostname(self):
        try:
            return self.__hawkular__.metric.hostname
        except:
            self.__exception_handler()

    def get_metric_auth(self):
        try:
            auth = self.__hawkular__.metric.auth
        except:
            self.__exception_handler()

        auth_dict = {}
        auth_dict['username'] = auth[0]
        auth_dict['password'] = auth[1]

        return auth_dict

    def get_metric_status(self):
        try:
            return self.__hawkular__.metric.status()
        except:
            self.__exception_handler()

    def get_metric_list_gauge_definition(self):
        try:
            return self.__hawkular__.metric.list_gauge_definition()
        except:
            self.__exception_handler()

    def get_metric_tenant_id(self):
        try:
            return self.__hawkular__.metric.tenant_id()
        except:
            self.__exception_handler()

    def get_metric_protocol(self):
        try:
            return self.__hawkular__.metric.protocol()
        except:
            self.__exception_handler()


    ''' Operations '''

    def add_jdbc_driver(self, feed_id, server_id, driver_name, module_name,
                        driver_class, driver_jar_name=None, binary_content=None, binary_file_location=None):
        try:
            return self.__hawkular__.add_jdbc_driver(feed_id, server_id, driver_name, module_name,
                                                    driver_class, driver_jar_name, binary_content, binary_file_location)
        except:
            self.__exception_handler()

    def remove_jdbc_driver(self, feed_id, server_id, driver_name):

        try:
            return self.__hawkular__.remove_jdbc_driver(feed_id, server_id, driver_name)
        except:
            self.__exception_handler()

    def add_deployment(self, feed_id, server_id, destination_file_name, force_deploy=False,
                       enabled=True, server_groups=None, binary_file_location=None, binary_content=None):

        try:
            return self.__hawkular__.add_deployment(feed_id, server_id, destination_file_name, force_deploy,
                                                    enabled, server_groups, binary_file_location, binary_content)
        except:
            self.__exception_handler()

    def undeploy(self, feed_id, server_id, destination_file_name, remove_content=True, server_groups=None):

        try:
            return self.__hawkular__.undeploy(destination_file_name, remove_content, server_groups)
        except:
            self.__exception_handler()

    def disable_deployment(self, feed_id, server_id, destination_file_name, server_groups=None):

        try:
            return self.__hawkular__.disable_deployment(feed_id, server_id, destination_file_name, server_groups)
        except:
            self.__exception_handler()

    def enable_deployment(self, feed_id, server_id, destination_file_name, server_groups=None):

        try:
            return self.__hawkular__.enable_deployment(feed_id, server_id, destination_file_name, server_groups)
        except:
            self.__exception_handler()

    def restart_deployment(self, feed_id, server_id, destination_file_name, server_groups=None):

        try:
            return self.__hawkular__.restart_deployment(feed_id, server_id, destination_file_name, server_groups)
        except:
            self.__exception_handler()