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
    target = None
    steps = []

    def __init__(self, point):
        self.target = point
        self.steps.append(point)
        pass

    def target_point(self, point):
        """ Last point of route, final goal """
        self.target = point
        return self

    def add(self, point):
        self.steps.append(point)
        return self



class NavigationTree():

    """ Reflection of CF UI, structure and content """
    _tree = dict([])
    web_driver = None
    _pivot = None

    def add_point(self, name, location, action):
        self._tree.update({ name : UI_Action( UI_Point(name, location), UI_Operation(action)) } )


    def __init__(self, driver):

        self._pivot = driver
        self.web_driver = driver
        self.add_point(   "compute", ".//*[@id='maintab']/li[3]/a/span[2]", "Hover")
        self.add_point("middleware", "id('#menu-compute')/ul/li[4]/a/span", "Hover")

        self.add_point("middleware_providers",   "id('#menu-compute')/ul/li[4]/div/ul/li[1]/a/span", "Click")
        self.add_point("middleware_servers",     "id('#menu-compute')/ul/li[4]/div/ul/li[2]/a/span", "Click")
        self.add_point("middleware_deployments", "id('#menu-compute')/ul/li[4]/div/ul/li[3]/a/span", "Click")
        self.add_point("middleware_datasources", "id('#menu-compute')/ul/li[4]/div/ul/li[4]/a/span", "Click")
        self.add_point(              "topology", "id('#menu-compute')/ul/li[4]/div/ul/li[5]/a/span", "Click")

    def navigate(self, route):
        driver = self.web_driver

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
        self.navigate(UI_Route("compute").add("middleware").add("middleware_providers"))

    def navigate_to_middleware_servers_view(self):
        self.navigate(UI_Route("compute").add("middleware").add("middleware_servers"))

    def navigate_to_middleware_deployment_view(self):
        self.navigate(UI_Route("compute").add("middleware").add("middleware_deployments"))

    def navigate_to_middleware_datasources_view(self):
        self.navigate(UI_Route("compute").add("middleware").add("middleware_datasources"))

    def navigate_to_topology_view(self):
        self.navigate(UI_Route("compute").add("middleware").add("topology"))



