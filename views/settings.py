from selenium.webdriver.support.color import Color
from common.ui_utils import ui_utils
from common.timeout import timeout

class settings():
    web_session = None
    web_driver = None
    ui_utils = None

    def __init__(self, web_session):
        self.web_session = web_session
        self.web_driver = web_session.web_driver
        self.ui_utils = ui_utils(self.web_session)


    def default_view(self):
        self.navigate_to_settings_default_view()

        assert (self.ui_utils.isTextOnPage("Middleware Providers"))
        assert(self.ui_utils.isTextOnPage("Middleware Servers"))
        assert(self.ui_utils.isTextOnPage("Middleware Deployments"))
        assert(self.ui_utils.isTextOnPage("Middleware Datasources"))
        assert(self.ui_utils.isTextOnPage("Middleware Domains"))
        assert(self.ui_utils.isTextOnPage("Middleware Messaging"))

        return True;

    def validate_providers_default_views(self):
        self.navigate_to_settings_default_view()

        # Middleware Prviders List View
        try:
            self.web_driver.find_element_by_css_selector("a[href*='manageiq_providers_middlewaremanager&view=list']").click()
            self.click_save_button()
        except:
            pass

        self.navigate_to_providers_view()
        assert self.is_view_list_selected()

        self.navigate_to_settings_default_view()

        # Middleware Prviders List View
        try:
            self.web_driver.find_element_by_css_selector("a[href*='manageiq_providers_middlewaremanager&view=tile']").click()
            self.click_save_button()
        except:
            pass

        self.navigate_to_providers_view()
        assert self.is_view_tile_selected()

        return True

    # Note:
    #   Selected icon color: blue(ish) = #0099d3 (hex)
    #   Non-selected icon color: black = #252525 (hex)

    def is_view_grid_selected(self):
        grid, tile, list = self.get_view_color_values()

        if grid < tile and grid < list:
            return True

        return False

    def is_view_tile_selected(self):
        grid, tile, list = self.get_view_color_values()

        if tile < grid and tile < list:
            return True

        return False

    def is_view_list_selected(self):
        grid, tile, list = self.get_view_color_values()

        if list < grid and list < tile:
            return True

        return False

    def get_view_color_values(self):
        grid = Color.from_string(self.web_driver.find_element_by_name("view_grid").value_of_css_property('color')).hex
        tile = Color.from_string(self.web_driver.find_element_by_name("view_tile").value_of_css_property('color')).hex
        list = Color.from_string(self.web_driver.find_element_by_name("view_list").value_of_css_property('color')).hex

        self.web_session.logger.debug("grid: {}  tile: {}  list: {}".format(grid, tile, list))

        return grid, tile, list

    def navigate_to_settings_default_view(self):
        self.web_driver.get("{}/configuration/index".format(self.web_session.MIQ_URL))
        self.ui_utils.waitForTextOnPage("Default Views", 15)
        self.web_driver.find_element_by_xpath("//*[contains(text(),'Default View')]").click()
        self.ui_utils.waitForTextOnPage("Middleware Providers", 15)

    def navigate_to_providers_view(self):
        self.web_session.web_driver.get("{}//ems_middleware/show_list".format(self.web_session.MIQ_URL))
        assert ui_utils(self.web_session).waitForTextOnPage("Middleware Providers", 30)

    def click_save_button(self):
        with timeout(seconds=15, error_message="Timed out waiting for Save."):
            while True:
                try:
                    self.web_driver.find_element_by_id('save').click()
                    break
                except:
                    self.web_session.logger.info("Settings Save Failed")
                    self.ui_utils.sleep(1)
                    pass
