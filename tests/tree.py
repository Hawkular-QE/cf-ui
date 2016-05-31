from tests import UI_Point, UI_Place, UI_Action, UI_Route, UI_Operation
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

class NavigationTree:

    """ Reflection of CF UI, structure and content """
    _tree = dict([])
    web_driver = None

    def add_point(self, name, location, action):
        self._tree.update({ name : UI_Action( UI_Point(name, location), UI_Operation(action)) } )
        pass

    def __init__(self, driver):
        self.web_driver = driver
        self.add_point("compute", ".//*[@id='maintab']/li[3]/a/span[2]", "Hover")
        """ following points are dependant and should be such used """
        self.add_point("middleware", "//span[contains(.,'Middleware')]", "Hover")
        self.add_point("middleware_providers", "//span[contains(.,'Providers')]", "Click")
        self.add_point("middleware_servers", "//span[contains(.,'Middleware Servers')]", "Click")
        self.add_point("middleware_deployments", "//span[contains(.,'Middleware Deployments')]", "Click")
        self.add_point("middleware_datasources", "//span[contains(.,'Topology')]", "Click")
        self.add_point("topology", "//span[@class='list-group-item-value']", "Click")
    pass

    def dump(self):
        container = self._tree
        for k in container.keys():
            v = container.get(k)
            print " on name '{}' at location '{}' - do '{}!' ".format(k, v._point._value, v._operation._operation)
        pass

    def navigate(self, target_page):

        pivot = self.web_driver
        hover = ActionChains(pivot)

        for step in target_page.steps:
            action = self._tree.get(step)
            point = action._point._value
            operation = action._operation._operation
            #print "\n '{}' ->  on '{}' - make {} ".format(step, point, operation)
            if operation=="Hover":
                elem = pivot.find_element_by_xpath(point)
                hover.move_to_element(elem).perform()
                pivot = elem
                sleep(3)
            else:
                if operation=="Click":
                    elem = pivot.find_element_by_xpath(point)
                    elem.click()
                    pivot = elem

        pass
