import numpy as np
from enum import Enum


"""
TODO:
* connections
* inductors
* AC voltage suppliers (?)
    * capacitive reactance and impedance

"""

class Component:
    """
    emf: voltage drop across the component
    curr: the current through the component
    res: resistance of the component
    name: vertex number of the component
    num_cxns: the number of connections the component has
    """
    def __init__(self, V_o, I_o, R_o, name, num_cxns=2):
        self.__emf = V_o
        self.__I = I_o
        self.__R = R_o
        self.__name = name
        self.__cxns = np.ones(num_cxns) * name

    def emf():
        doc = "The emf property."
        def fget(self):
            return self.__emf
        def fset(self, value):
            self.__emf = value
        def fdel(self):
            del self.__emf
        return locals()
    emf = property(**emf())

    def curr():
        doc = "The current property."
        def fget(self):
            return self.__I
        def fset(self, value):
            self.__I = value
        def fdel(self):
            del self.__I
        return locals()
    curr = property(**curr())

    def res():
        doc = "The resistance property."
        def fget(self):
            return self.__R
        def fset(self, value):
            self.__R = value
        def fdel(self):
            del self.__R
        return locals()
    res = property(**res())

    @property
    def power(self):
        return self.curr * self.emf

    @property
    def get_name(self):
        return self.__name

    def cxns():
        doc = "An array of connections."
        def fget(self):
            return self.__cxns
        def fset(self, value):
            self.__cxns = value
        def fdel(self):
            del self.__cxns
        return locals()
    cxns = property(**cxns())


class Wire(Component):
    def __init__(self, R=0):
        super().__init__(0, 0, R)

class Junction(Component):
    """These are merely for splitting wires and don't have any physical
    properties"""
    def __init__(self, cxns):
        super().__init(0, 0, 0, cxns)

class State(Enum):
    OPEN = true
    CLOSED = false
    ON = true
    OFF = false #this is probably stylistically super bad

class Switch(Component):
    def __init__(self, state=State.CLOSED): #probably not the best use of enums
        super().__init__(self, 0, 0, 0)
        self.__state = state

    def state():
        doc = "The state of the switch (OPEN or CLOSED)"
        def fget(self):
            return self.__state
        def fset(self, value):
            self.__state = value
        def fdel(self):
            del self.__state
        return locals()
    state = property(**_state())

class Type(Enum):
    AMMETER = 0
    VOLTMETER = 1
    OHMMETER = 2

class Multimeter(Component):
    def __init__(self, meter_type=Type.VOLTMETER):
        super().__init__(0, 0, 0)
        self.__meter_type = meter_type
        self.__reading

    def meter_type():
        doc = "The multimeter setting."
        def fget(self):
            return self.__meter_type
        def fset(self, value):
            self.__meter_type = value
        def fdel(self):
            del self.__meter_type
        return locals()
    meter_type = property(**meter_type())

    def reading():
        doc = "The _reading property."
        def fget(self):
            return self.__reading
        def fset(self, value):
            self.__reading = value
        def fdel(self):
            del self.__reading
        return locals()
    reading = property(**reading())

class DC_Battery(Component):
    """Direct Current emf source"""
    def __init__(self, V=3, R=0):
        #R represents the battery's internal resistance
        super().__init__(V, 0, R)

class Resistor(Component):
    def __init__(self, R=5):
        super().__init__(0, 0, R)

class Light_Bulb(Resistor):
    def __init__(self, R, W, state=State.OFF):
        super().__init(0, 0, R)
        self.__state = state
        self.__wattage = W

    def state():
        doc = "The state of the light bulb (ON or OFF)"
        def fget(self):
            return self.__state
        def fset(self, value):
            self.__state = value
        def fdel(self):
            del self.__state
        return locals()
    state = property(**_state())

    def wattage():
        doc = "The wattage required for the bulb to light up"
        def fget(self):
            return self.__wattage
        def fset(self, value):
            self.__wattage = value
        def fdel(self):
            del self.__wattage
        return locals()
    wattage = property(**wattage())

class Capacitor(Component):
    """
    Parallel-plate capacitor
    A: area of the plate
    C: capacitance
    d: distance of separation between the plates
    V: voltage across the parallel plates
    Q: charge of the capacitor
    kappa: the dielectric constant (1 in vacuum)
    epsilon: permittivity of the dielectric = vacuum permittivity * kappa
    """
    def __init__(self, V, A, d=0.01, kappa=1):
        super().__init__(V, 0, 0)
        self.epsilon = kappa * 8.854e-12
        self.__C = self.epsilon * A / d
        self.__Q = self.cpty * self.emf

    def cpty():
        doc = "The Capacitance property."
        def fget(self):
            return self.__C
        def fset(self, value):
            self.__C = value
        def fdel(self):
            del self.__C
        return locals()
    cpty = property(**cpty())

    def chg():
        doc = "The Charge property."
        def fget(self):
            return self.__Q
        def fset(self, value):
            self.__Q = value
        def fdel(self):
            del self.__Q
        return locals()
    chg = property(**chg())
