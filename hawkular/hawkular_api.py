from mgmtsystem.hawkular import Hawkular
from common.timeout import timeout
from common.ui_utils import ui_utils

class hawkular_api():
    web_session = None
    __hawkular__ = None

    def __init__(self, web_session, ws_connect=False):
        self.web_session = web_session
        try:
            self.web_session.logger.info("hostname: {}, port: {}, username: {}, password: {}"
                                         .format(web_session.HAWKULAR_HOSTNAME, web_session.HAWKULAR_PORT,
                                                 web_session.HAWKULAR_USERNAME, web_session.HAWKULAR_PASSWORD,))

            self.__hawkular__ = Hawkular(hostname=web_session.HAWKULAR_HOSTNAME, port=web_session.HAWKULAR_PORT,
                                     username=web_session.HAWKULAR_USERNAME, password=web_session.HAWKULAR_PASSWORD,
                                     ws_connect=ws_connect)
        except Exception, e:
            raise Exception(e)

    # Hide the Hawkular object, but provide ability to get and use if need be
    def get_hawkular(self):
        return self.__hawkular__

    def __exception_handler(self, e):
        assert False, "Hawkular Services {} failed to connect, Exception: {}".format(self.web_session.HAWKULAR_HOSTNAME, e)

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
        except Exception, e:
            self.__exception_handler(e)

        for datasource in rows:
            dict = {}
            dict['Nativeid'] = datasource.id
            dict['Name'] = datasource.name
            dict['path'] = datasource.path
            datasources.append(dict)

        return datasources

    def get_hawkular_deployments(self):
        deployments = []

        with timeout(seconds=30, error_message="Timed out - No Deployments Returned"):
            while True:
                try:
                    rows = self.__hawkular__.inventory.list_server_deployment()
                    if rows:
                        for deployment in rows:
                            dict = {}
                            dict['Nativeid'] = deployment.id
                            dict['Name'] = deployment.name
                            dict['path'] = deployment.path
                            deployments.append(dict)
                        break
                    else:
                        ui_utils(self.web_session).sleep(2)
                except Exception, e:
                    self.__exception_handler(e)

        return deployments

    def get_hawkular_domains(self, feed_id = None):
        domains = []

        try:
            rows = self.__hawkular__.inventory.list_domain(feed_id)
        except Exception, e:
            self.__exception_handler(e)

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
        except Exception, e:
            self.__exception_handler(e)

        for group in rows:
            dict = {}
            dict['id'] = group.id
            dict['name'] = group.name
            dict['path'] = group.path
            dict['data'] = group.data
            server_groups.append(dict)

        return server_groups

    def get_hawkular_messagings(self):
        messagings = []

        try:
            rows = self.__hawkular__.inventory.list_messaging()
        except Exception, e:
            self.__exception_handler(e)

        for message in rows:
            dict = {}
            dict['id'] = message.id
            dict['name'] = message.name
            dict['path'] = message.path
            messagings.append(dict)

        return messagings

    def get_port(self):
        try:
            return self.__hawkular__.port
        except Exception, e:
            self.__exception_handler(e)

    def get_ip_address(self):
        try:
            return self.__hawkular__.get_ip_address
        except Exception, e:
            self.__exception_handler(e)

        def generic_for_testing(self):
            return self.__hawkular__.list_server()

    ''' Alerts '''

    def get_alert_list_event(self):
        # TO-DO: Return formatted Dict
        try:
            return self.__hawkular__.alert.list_event()
        except Exception, e:
            self.__exception_handler(e)

    def get_alert_auth(self):
        try:
            auth =  self.__hawkular__.alert.auth
        except Exception, e:
            self.__exception_handler(e)

        auth_dict = {}
        auth_dict['username'] = auth[0]
        auth_dict['password'] = auth[1]

        return auth_dict

    def get_alert_tenant_id(self):
        try:
            return self.__hawkular__.alert.tenant_id
        except Exception, e:
            self.__exception_handler(e)

    def get_alert_hostname(self):
        try:
            return self.__hawkular__.alert.hostname
        except Exception, e:
            self.__exception_handler(e)

    def get_alert_status(self):
        try:
            return self.__hawkular__.alert.status()
        except Exception, e:
            self.__exception_handler(e)

    ''' Metrics '''

    def get_metric_hostname(self):
        try:
            return self.__hawkular__.metric.hostname
        except Exception, e:
            self.__exception_handler(e)

    def get_metric_auth(self):
        try:
            auth = self.__hawkular__.metric.auth
        except Exception, e:
            self.__exception_handler(e)

        auth_dict = {}
        auth_dict['username'] = auth[0]
        auth_dict['password'] = auth[1]

        return auth_dict

    def get_metric_status(self):
        try:
            return self.__hawkular__.metric.status()
        except Exception, e:
            self.__exception_handler(e)

    def get_metric_list_gauge_definition(self):
        try:
            return self.__hawkular__.metric.list_gauge_definition()
        except Exception, e:
            self.__exception_handler(e)

    def get_metric_tenant_id(self):
        try:
            return self.__hawkular__.metric.tenant_id()
        except Exception, e:
            self.__exception_handler(e)

    def get_metric_protocol(self):
        try:
            return self.__hawkular__.metric.protocol()
        except Exception, e:
            self.__exception_handler(e)


    def list_availability_server(self, feed_id, server_id):
        try:
            return self.__hawkular__.metric.list_availability_server(feed_id, server_id)
        except Exception, e:
            self.__exception_handler(e)

    ''' Operations '''

    def add_jdbc_driver(self, feed_id, server_id, driver_name, module_name,
                        driver_class, driver_jar_name=None, binary_content=None, binary_file_location=None):
        try:
            return self.__hawkular__.add_jdbc_driver(feed_id, server_id, driver_name, module_name,
                                                    driver_class, driver_jar_name, binary_content, binary_file_location)
        except Exception, e:
            self.__exception_handler(e)

    def remove_jdbc_driver(self, feed_id, server_id, driver_name):

        try:
            return self.__hawkular__.remove_jdbc_driver(feed_id, server_id, driver_name)
        except Exception, e:
            self.__exception_handler(e)

    def add_deployment(self, feed_id, server_id, destination_file_name, force_deploy=False,
                       enabled=True, server_groups=None, binary_file_location=None, binary_content=None):

        try:
            return self.__hawkular__.add_deployment(feed_id, server_id, destination_file_name, force_deploy,
                                                    enabled, server_groups, binary_file_location, binary_content)
        except Exception, e:
            self.__exception_handler(e)

    def undeploy(self, feed_id, server_id, destination_file_name, remove_content=True, server_groups=None):

        try:
            return self.__hawkular__.undeploy(feed_id, server_id, destination_file_name, remove_content, server_groups)
        except Exception, e:
            self.__exception_handler(e)

    def disable_deployment(self, feed_id, server_id, destination_file_name, server_groups=None):

        try:
            return self.__hawkular__.disable_deployment(feed_id, server_id, destination_file_name, server_groups)
        except Exception, e:
            self.__exception_handler(e)

    def enable_deployment(self, feed_id, server_id, destination_file_name, server_groups=None):

        try:
            return self.__hawkular__.enable_deployment(feed_id, server_id, destination_file_name, server_groups)
        except Exception, e:
            self.__exception_handler(e)

    def restart_deployment(self, feed_id, server_id, destination_file_name, server_groups=None):

        try:
            return self.__hawkular__.restart_deployment(feed_id, server_id, destination_file_name, server_groups)
        except Exception, e:
            self.__exception_handler(e)