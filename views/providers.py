

class providers():
    web_session = None

    def __init__(self, web_session):
        self.web_session = web_session

    def add_provider(self):
        self.web_session.logger.info("To Do")
        # navigate_to_provider_new()
        # add_provider()

    def delete_provider(self):
        self.web_session.logger.info("To Do")
        # navigate_to_providers
        # delete_provider()

    def update_provider(self):
        self.web_session.logger.info("To Do")
        # navigate_to_providers
        # update_provider

    def add_provider_if_not_present(self):
        self.web_session.logger.info("To Do")
        # navigate_to_providers
        # If provider is not present, add provider

    def does_provider_exist(self):
        self.web_session.logger.info("To Do")
        # navigate_to_providers
        # is_provider_present (note: use ui_utils.isTextOnPage OR create new ui_utils.isElementPresent)