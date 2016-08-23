import psycopg2
import psycopg2.extras
import string

class db():
    web_session = None
    miq_ip = None
    db_port = None
    username = None
    password = None

    database = 'vmdb_production'
    connection = None
    dict_cursor = None

    # To-Do: return only needed columns (aka add filters)
    sql_providers = 'select * from endpoints, ext_management_systems where endpoints.id=ext_management_systems.id;'
    sql_servers = 'select * from middleware_servers'
    sql_datasources = 'select * from middleware_datasources'
    sql_deployments = 'select * from middleware_deployments'
    sql_domains = 'select * from middleware_domains'
    sql_server_groups = 'select * from  middleware_server_groups'

    def __init__(self, web_session, miq_ip = None, username = None, password = None, db_port = None):

        self.web_session = web_session
        self.miq_ip = self.web_session.MIQ_HOSTNAME if db_port == None else miq_ip
        self.username = self.web_session.DB_USERNAME if username == None else username
        self.password = self.web_session.DB_PASSWORD if password == None else password
        self.db_port = self.web_session.DB_PORT if db_port == None else db_port

        try:
            self.connection = psycopg2.connect(
                database=self.database, user=self.username, password=self.password, host=self.miq_ip, port=self.db_port)
            self.dict_cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        except Exception, e:
            raise Exception(e)


    def execute(self, query):
        rows = None

        self.web_session.logger.info('Execute SQL \"{}\" on IP \"{}\".'.format(query, self.miq_ip))

        try:
            self.dict_cursor.execute(query)
            rows = self.dict_cursor.fetchall()
        except Exception, e:
            self.web_session.logger.error('Failed to execute SQL \"{}\". Exception: {}".'.format(query, e))

        return rows

    def get_providers(self):
        providers = []
        rows = self.execute(self.sql_providers)

        for row in rows:
            if self.web_session.PROVIDER in row.get('type'):
                providers.append(row)

        return providers

    def get_servers(self):
        rows = self.execute(self.sql_servers)
        for server in rows:
            server['nativeid'] = server.get('nativeid').strip('~')

        return rows

    def get_datasources(self):
        return self.execute(self.sql_datasources)

    def get_deployments(self):
        return self.execute(self.sql_deployments)

    def get_domains(self):
        return self.execute(self.sql_domains)

    def get_server_groups(self):
        return self.execute(self.sql_server_groups)