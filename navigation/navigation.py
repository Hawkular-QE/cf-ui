from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class UI_Point():

    """ Representation of any addressable place in UI, """

    _value = None
    _name = None

    def __init__(self, name, value):
        self._name = name
        self._value = value

    def name(self):
        return self._name

    def value(self):
        return self._value



class UI_Operation():

    """ Possible enumeration (radio) options: Click or HoverMouse. """

    # TODO: enumeration
    Click, Hover = range(2)
    _operation = None

    def __init__(self, op):
        if op == "Click" or op == "Hover":
            self._operation = op
        else:
            raise ValueError("Value of Operation is out of range!")

class UI_Action():

    """ composition of UI_Points and UI_Operations into user actions """

    _point = None
    _operation = None
    def __init__(self, point, op):
        self._point = point
        self._operation = op


class UI_Route():

    """ Set of chains of user actions sucessfully  leading to necessary result (place or page) """

    def __init__(self, point):
        self.steps = [point]
        self.goal = point

    def set_goal(self, point):
        """ Last point of route, final goal - for conditional navigation """
        self.goal = point
        return point

    def add(self, point):
        self.steps.append( self.set_goal(point) )
        return self



class NavigationTree():

    """ Reflection of CF UI, structure and content """

    _tree = dict([])
    web_driver = None
    web_session = None
    wait = None

    paths = {
        'middleware_providers'   : '/ems_middleware/show_list',
        'middleware_domains'     : '/middleware_domain/show_list',
        'middleware_servers'     : '/middleware_server/show_list',
        'middleware_deployments' : '/middleware_deployment/show_list',
        'middleware_datasources' : '/middleware_datasource/show_list',
                      'topology' : '/middleware_topology/show',
        }

    page_marks = {
        'middleware_providers'   : '/ems_middleware/show_list',
        'middleware_domains'     : '/middleware_domain/show_list',
        'middleware_servers'     : '/middleware_server/show_list',
        'middleware_deployments' : '/middleware_deployment/show_list',
        'middleware_datasources' : '/middleware_datasource/show_list',
                      'topology' : '/middleware_topology/show',
        }

    def add_point(self, name, location, action):
        self._tree.update( { name : UI_Action( UI_Point(name, location), UI_Operation(action)) } )

    def __init__(self, session):
        self.web_session = session
        self.web_driver = self.web_session.web_driver
        time_delay = 7
        self.wait = WebDriverWait(self.web_driver, time_delay)

        self.add_point("middleware", ".//*[@id='maintab']/li[6]/a/span[contains(.,'Middleware')]", "Hover")
        self.add_point("middleware_providers",   "id('#menu-mdl')//span[contains(.,'Providers')]", "Click")
        self.add_point("middleware_domains",     "id('#menu-mdl')//span[contains(.,'Middleware Domains')]/..", "Click")
        self.add_point("middleware_servers",     "id('#menu-mdl')//span[contains(.,'Middleware Servers')]", "Click")
        self.add_point("middleware_deployments", "id('#menu-mdl')//span[contains(.,'Middleware Deployments')]", "Click")
        self.add_point("middleware_datasources", "id('#menu-mdl')//span[contains(.,'Middleware Datasources')]", "Click")
        self.add_point("topology",               "id('#menu-mdl')//span[contains(.,'Topology')]", "Click")


    def navigate(self, route, force_navigation=True):
        driver = self.web_driver
        goal = route.goal
        if self.paths.get(goal) == None:
            raise ValueError("Fast navigation: no such key in dict 'paths', update it!")

        current_page = self.web_driver.current_url
        target_page = self.paths.get(goal)
        if not current_page.endswith(target_page) or force_navigation:

            for step in route.steps:
                self.click_turn(driver, step)


    def click_turn(self, driver, step):
        try:
            hover = ActionChains(driver)
            action = self._tree.get(step)
            target = action._point._value
            operation = action._operation._operation
            elem = driver.find_element_by_xpath(target)
            hover.move_to_element(elem).perform()
            wait = WebDriverWait(self.web_driver, 5)
            wait.until(EC.element_to_be_clickable(elem))
            if operation == "Click":
                elem.click()

        except:
            #self.web_session.logger.warning(" Clicking goes on next turn. Possibly, recursion...")
            #self.click_turn( driver, step )
            pass


    def navigate_to_middleware_providers_view(self):
        self.navigate(UI_Route("middleware").add("middleware_providers"))

    def navigate_to_middleware_servers_view(self):
        self.navigate(UI_Route("middleware").add("middleware_servers"))

    def navigate_to_middleware_domains_view(self):
        self.navigate(UI_Route("middleware").add("middleware_domains"))

    def navigate_to_middleware_deployment_view(self):
        self.navigate(UI_Route("middleware").add("middleware_deployments"))

    def navigate_to_middleware_datasources_view(self):
        self.navigate(UI_Route("middleware").add("middleware_datasources"))

    def navigate_to_topology_view(self):
        self.navigate(UI_Route("middleware").add("topology"))


    def _jump_to(self, target, force_navigation=True):
        # Fast navigation
        if self.paths.get(target)==None:
            raise ValueError("Fast navigation: no such key in dict 'paths', update it!")
        current_page = self.web_driver.current_url
        target_page = self.paths.get(target)
        if not current_page.endswith(target_page) or force_navigation:
                self.web_driver.get(self.web_session.MIQ_URL + target_page)
        return self


    def jump_to_middleware_providers_view(self, force_navigation=True):
        self._jump_to('middleware_providers', force_navigation)
        return self

    def jump_to_middleware_servers_view(self, force_navigation=True):
        self._jump_to('middleware_servers', force_navigation)
        return self

    def jump_to_middleware_deployment_view(self, force_navigation=True):
        self._jump_to('middleware_deployments', force_navigation)
        return self

    def jump_to_middleware_datasources_view(self, force_navigation=True):
        self._jump_to('middleware_datasources', force_navigation)
        return self

    def jump_to_topology_view(self, force_navigation=True):
        self._jump_to('topology', force_navigation)
        return self

    def jump_to_middleware_domain_view(self, force_navigation=True):
        self._jump_to('middleware_domains', force_navigation)
        return self

    def waiting_ability(self, xpath, seconds):
        try:
            WebDriverWait(self.web_driver, seconds).until(
                EC.visibility_of_element_located((By.XPATH, xpath)))
        except:
            self.web_session.logger.info(" Given object is not clickable. (waiting_clickability)")
            self.waiting_ability(xpath, seconds - 1)

    def power_click(self, clickable):
        driver = self.web_driver
        hover = ActionChains(driver)
        if clickable:
            hover.move_to_element(clickable).perform()

            clickable.click()

    def select_and_click(self, click_point, select_option):
        driver = self.web_driver
        xpath_top = ".//div[contains(@class, 'dropdown')]/button[contains(.,'{}')]".format(click_point)
        xpath_select = "{}/../ul[contains(@class, 'dropdown-menu')]/li/a[contains(.,'{}')]".format(xpath_top, select_option)

        WebDriverWait(self.web_driver, 7).until(
            EC.visibility_of_element_located((By.XPATH, xpath_top))
            )

        found_top = driver.find_elements_by_xpath(xpath_top)
        found_select = driver.find_elements_by_xpath(xpath_select)
        if len(found_top)==0 or len(found_select)==0:
            raise Exception("Page does not contain such pattern(s) {}, {}: ".format(click_point, select_option))

        self.waiting_ability(xpath_top, 7)
        self.power_click(driver.find_element_by_xpath(xpath_top))

        self.waiting_ability(xpath_select, 7)
        self.power_click(driver.find_element_by_xpath(xpath_select))
        return self


    def to_exact_details(self, param='first'):
        driver = self.web_driver
        list_view_click = "//i[contains(@class,'fa fa-th-list')]"
        first_item = ".//*[@id='list_grid']/table/tbody/tr"

        driver.find_element_by_xpath(list_view_click).click()
        sub_links = driver.find_elements_by_xpath(first_item)
        num_link = len(sub_links)
        ind = 0
        use_numeric_param = False
        try:
            ind = int(param) - 1 ## Visual numeration from 1 !!
            use_numeric_param = True
        except: pass

        assert (use_numeric_param == True or param == 'first' or param == 'last'), "-- Possible wrong value of param '{}'?".format(param)
        if len(sub_links) > 0:

            if param == 'first':
                sub_links[0].click()

            elif param=='last':
                sub_links[num_link - 1].click()

            elif use_numeric_param:
                assert (ind <= num_link and ind >= 0), "-- Definitely wrong value of param: '{}'".format(param)
                sub_links[ind].click()
        else:
            # raise ValueError("Not enough items for searching!") # ??
            print "Not enough items for selection!"
        return self


    def to_first_details(self):
        self.to_exact_details('first')
        return self


    def to_last_details(self):
        self.to_exact_details('last')
        return self


    def is_ok(self, point):
        if point.is_displayed() and point.is_enabled():
            return True

    def go_up_till_clickable(self, click_point):
        xpath_up = ".."
        parent = click_point.find_element_by_xpath(xpath_up)
        if self.is_ok(parent):
            parent.click()
        else:
            self.go_up_till_clickable(parent)


    def found_by_pattern(self, pattern):
        driver = self.web_driver
        driver.find_element_by_name("view_list").click()
        xpath = "//*[contains(text(), '{}')]".format(pattern)
        click_points = driver.find_elements_by_xpath(xpath)
        if len(click_points) > 1:
            click_point = click_points[0]
            if self.is_ok(click_point):
                click_point.click()
            else:
                self.go_up_till_clickable(click_point)
        return True
