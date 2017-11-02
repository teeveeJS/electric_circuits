import numpy as np
from enum import Enum


"""
TODO:
* connections
* capacitor initial charge
* inductors
    * magnetic flux
* AC voltage suppliers (?)
    * capacitive reactance and impedance

"""

# probably won't actually need this
class Comp_Type(Enum):
    WIRE: 0,
    JUNCTION: 1,
    SWITCH: 2,
    MULTIMETER: 3,
    DC_BATTER: 4,
    RESISTOR: 5,
    LIGHT_BULB: 6,
    CAPACITOR: 7,
    INDUCTOR: 8

class Component:
    """
    emf: voltage drop across the component
    curr: the current through the component
    res: resistance of the component
    name: vertex number of the component
    cxns: an array of connections
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
    def name(self):
        return self.__name

    def cxns():
        doc = "An array of endpoints (names) connected to the component."
        def fget(self):
            return self.__cxns
        def fset(self, value):
            self.__cxns = value
        def fdel(self):
            del self.__cxns
        return locals()
    cxns = property(**cxns())

    def formatted_cxns(self):
        """Formats the connections for circuit edges"""
        return np.stack((self.cxns, np.ones(len(self.cxns))*self.name, axis=-1)


class Wire(Component):
    def __init__(self, name, R=0):
        # V is always 0
        super().__init__(0, 0, R, name)

class Junction(Component):
    """For splitting wires."""
    def __init__(self, name, cxns=3):
        super().__init__(0, 0, 0, name, cxns)

class State(Enum):
    ON = True
    OFF = False

class Switch(Component):
    def __init__(self, name, state=State.ON): #probably not the best use of enums
        super().__init__(self, 0, 0, 0, name)
        self.__state = state

    def state():
        doc = "The state of the switch (ON or OFF)"
        def fget(self):
            return self.__state
        def fset(self, value):
            self.__state = value
        def fdel(self):
            del self.__state
        return locals()
    state = property(**state())

class Type(Enum):
    AMMETER = 0
    VOLTMETER = 1
    OHMMETER = 2

class Multimeter(Component):
    def __init__(self, name, meter_type=Type.VOLTMETER):
        super().__init__(0, 0, 0, name)
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
        doc = "The reading to be displayed in the GUI."
        def fget(self):
            return self.__reading
        def fset(self, value):
            self.__reading = value
        def fdel(self):
            del self.__reading
        return locals()
    reading = property(**reading())

    def calc_reading(self, circuit):
        """
        Calculates the value to be displayed
        * current: current flowing out of the previous components
            * direction of current?
        * voltage: total voltage drop of the components in between the two ends
        * resistance: the equivalent resistance of the components in between
        """



        return

class DC_Battery(Component):
    """Direct Current emf source"""
    def __init__(self, name, V=3, R=0):
        #R represents the battery's internal resistance
        super().__init__(V, 0, R, name)

class Resistor(Component):
    def __init__(self, name, R=5):
        super().__init__(0, 0, R, name)

class Light_Bulb(Resistor):
    def __init__(self, R, W, mame, state=State.OFF):
        super().__init(0, 0, R, name)
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
    state = property(**state())

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
    def __init__(self, name, V, A, d=0.01, kappa=1):
        super().__init__(V, 0, 0, name)
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