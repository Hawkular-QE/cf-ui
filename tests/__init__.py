
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
    pass

class UI_Place():
    """ Representation of any addressable place in UI, could consist of few alternative points (overlay) """
    _value = None
    _name = None
    _alt_values = [] # Or () or {} ??

    def __init__(self, name, value):
        self._name = name
        self._value = value

    def name(self):
        return self._name

    def value(self):
        return self._value

    def add_alt_point(self, value):
        self._alt_values.append(value)

class UI_Operation():
    """ Possible enumeration (radio) options: Click or HoverMouse. TODO: enumeration """
    Click, Hover = range(2)
    _operation = None

    def __init__(self, op):
        if op == "Click" or op == "Hover":
            self._operation = op
        else:
            raise ValueError("Value of Operation is out of range!")
    pass

class UI_Action():
    """ composition of UI_Points and UI_Operations into user actions """
    _point = None
    _operation = None
    def __init__(self, point, op):
        self._point = point
        self._operation = op

    pass

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

    pass

