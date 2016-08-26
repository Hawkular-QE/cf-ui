from common.ui_utils import ui_utils
from hawkular.hawkular_api import hawkular_api
from common.db import db


class domains():
    web_session = None
    web_driver = None
    ui_utils = None
    db = None
    hawkular_api = None

    def __init__(self, web_session):
        self.web_session = web_session
        self.web_driver = web_session.web_driver
        self.ui_utils = ui_utils(self.web_session)
        self.hawkular_api = hawkular_api(self.web_session)

        try:
            self.db = db(self.web_session)
        except Exception, e:
            self.web_session.logger.warning("Unable to connecto to database. {}".format(e))

    def validate_domains_list(self):
        self.web_session.web_driver.get("{}/middleware_domain/show_list".format(self.web_session.MIQ_URL))
        assert self.ui_utils.waitForTextOnPage("Middleware Domains", 15)

        domains_ui = self.ui_utils.get_list_table()
        domains_db = self.db.get_domains()
        # TBD domains_hawk = ...

        assert len(domains_ui) == len(domains_db), "Domains lists length mismatch."

        for domain_ui in domains_ui:
            domain_db = self.ui_utils.find_row_in_list(domains_db, 'feed', domain_ui.get('Feed'))
            assert domain_db, "No DB Domain found"

            assert domain_ui.get('Feed') == domain_db.get('feed')
            # TBD assert domain_ui.get('Feed') == domain_hawk.get('feed')

        return True

    def validate_domain_details(self):
        self.web_session.web_driver.get("{}/middleware_domain/show_list".format(self.web_session.MIQ_URL))
        assert self.ui_utils.waitForTextOnPage("Middleware Domains", 15)

        domains_ui = self.ui_utils.get_list_table()
        domains_db = self.db.get_domains()

        for domain_ui in domains_ui:
            feed = domain_ui.get('Feed')  # Unique Server identifier
            self.web_session.web_driver.get("{}/middleware_domain/show_list".format(self.web_session.MIQ_URL))
            self.ui_utils.click_on_row_containing_text(domain_ui.get('Feed'))
            self.ui_utils.waitForTextOnPage("Nativeid", 15)

            domain_details_ui = self.ui_utils.get_generic_table_as_dict()
            domain_details_db = self.ui_utils.find_row_in_list(domains_db, 'feed', feed)

            assert domain_details_db, "Feed {} not found in DB Domain List".format(feed)

            assert (domain_details_ui.get('Name') == domain_details_db.get("name"),
                    "Name mismatch ui:{}, DB:{}".format(domain_details_ui.get('Name'),
                                                        domain_details_db.get("name")))
            assert (domain_details_ui.get('Nativeid') == domain_details_db.get("Nativeid"),
                        "Nativeid mismatch ui:{}, DB:{}".format(domain_details_ui.get('Nativeid'),
                                                                domain_details_db.get("nativeid")))

        return True


    def validate_server_groups_list(self):

        self.web_session.web_driver.get("{}/middleware_domain/show_list".format(self.web_session.MIQ_URL))
        assert self.ui_utils.waitForTextOnPage("Middleware Domains", 15)

        domains_ui = self.ui_utils.get_list_table()
        server_groups_db = self.db.get_server_groups()

        for domain in domains_ui:
            self.web_session.web_driver.get("{}/middleware_domain/show_list".format(self.web_session.MIQ_URL))
            assert self.ui_utils.waitForTextOnPage("Middleware Domains", 15)

            self.ui_utils.click_on_row_containing_text(domain.get('Domain Name'))

            try:
                self.ui_utils.get_elements_containing_text('Middleware Server Groups')[0].click()
            except Exception, e:
                raise Exception(e)

            self.ui_utils.waitForTextOnPage("All Middleware Server Groups", 15)

            # To Do: get Table UI table
            server_groups_ui = self.ui_utils.get_list_table()

            for server_group in server_groups_ui:
                name = server_group.get('Server Group Name')
                server_group_db = self.ui_utils.find_row_in_list(server_groups_db, 'name', name)
                assert server_group_db, "Server Group {} not found in DB".format(name)

                assert server_group.get('Feed') == server_group_db.get('feed')
                assert server_group.get('Profile') == server_group_db.get('profile')

        return True