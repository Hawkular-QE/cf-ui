from selenium.webdriver.common.action_chains import ActionChains
from time import sleep


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

    paths = {
                'middleware_servers'     : '/middleware_server/show_list',
                'middleware_deployments' : '/middleware_deployment/show_list',
                'middleware_datasources' : '/middleware_datasource/show_list',
                'middleware_providers'   : '/ems_middleware/show_list',
                              'topology' : '/middleware_topology/show',
            }

    def add_point(self, name, location, action):
        self._tree.update( { name : UI_Action( UI_Point(name, location), UI_Operation(action)) } )

    def __init__(self, session):
        self.web_session = session
        self.web_driver = self.web_session.web_driver
        self.add_point("middleware", "id('maintab')/li[6]/a/span[2]", "Hover")
        self.add_point("middleware_providers",   "id('#menu-mdl')/ul/li[1]/a/span", "Click")
        self.add_point("middleware_servers",     "id('#menu-mdl')/ul/li[2]/a/span", "Click")
        self.add_point("middleware_deployments", "id('#menu-mdl')/ul/li[3]/a/span", "Click")
        self.add_point("middleware_datasources", "id('#menu-mdl')/ul/li[4]/a/span", "Click")
        self.add_point(              "topology", "id('#menu-mdl')/ul/li[5]/a/span", "Click")


    def navigate(self, route, force_navigation=True):
        driver = self.web_driver
        goal = route.goal
        if self.paths.get(goal) == None:
            raise ValueError("Fast navigation: no such key in dict 'paths', update it!")

        current_page = self.web_driver.current_url
        target_page = self.paths.get(goal)
        if not current_page.endswith(target_page) or force_navigation:
            self.web_driver.get(self.web_session.MIQ_URL + target_page)

        for step in route.steps:
            hover = ActionChains(driver)
            action = self._tree.get(step)
            target = action._point._value
            operation = action._operation._operation
            elem = driver.find_element_by_xpath(target)
            hover.move_to_element(elem).perform()
            if operation == "Click":
                elem.click()
            sleep(2)


    def navigate_to_middleware_providers_view(self):
        self.navigate(UI_Route("middleware").add("middleware_providers"))

    def navigate_to_middleware_servers_view(self):
        self.navigate(UI_Route("middleware").add("middleware_servers"))

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


    def jump_to_middleware_providers_view(self, force_navigation=True):
        self._jump_to('middleware_providers', force_navigation)

    def jump_to_middleware_servers_view(self, force_navigation=True):
        self._jump_to('middleware_servers', force_navigation)

    def jump_to_middleware_deployment_view(self, force_navigation=True):
        self._jump_to('middleware_deployments', force_navigation)

    def jump_to_middleware_datasources_view(self, force_navigation=True):
        self._jump_to('middleware_datasources', force_navigation)

    def jump_to_topology_view(self, force_navigation=True):
        self._jump_to('topology', force_navigation)
