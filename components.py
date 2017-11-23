import numpy as np
from enum import Enum


class Component:
    """
    emf: voltage drop across the component
    curr: the current through the component
    res: resistance of the component
    name: vertex number of the component
    """
    def __init__(self, V_o, I_o, R_o, name, num_cxns=2):
        self.__emf = V_o
        self.__I = I_o
        self.__R = R_o
        self.__name = name
        self.__cxns = np.ones(num_cxns, dtype='int') * self.name

        self.len_conn = num_cxns

        # direction of current in the component
        # self.curr_dir = np.ones(2, dtype='int') * self.name # [start, end]

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

    def cxns():
        doc = "The _cxns property."
        def fget(self):
            return self.__cxns
        def fset(self, value):
            self.__cxns = value
        def fdel(self):
            del self.__cxns
        return locals()
    cxns = property(**cxns())

    def add_connection(self, cxn):
        for i in range(len(self.cxns)):
            if self.cxns[i] == self.name:
                self.cxns[i] = cxn
                # what if the component has the same connection twice?
                # i.e. a circuit consisting of only a battery and a resistor
                break

    def rm_connection(self, cxn):
        # TODO: handle the (error) case where nothing is removed
        for i in range(len(self.cxns)):
            if self.cxns[i] == cxn:
                self.cxns[i] = self.name
                break
                # potential problem: only the first instance is removed

    @property
    def is_fully_connected(self):
        return not (self.name in self.cxns)

    @property
    def power(self):
        """Power dissipated by the element"""
        return self.curr * self.emf

    @property
    def name(self):
        return self.__name


class Wire(Component):
    def __init__(self, start, end):
        super().__init__(0, 0, 0, -1)
        self.__start = start
        self.__end = end
        self.__pair = (self.start, self.end)

    def start():
        doc = "The _start property."
        def fget(self):
            return self.__start
        def fset(self, value):
            self.__start = value
        def fdel(self):
            del self.__start
        return locals()
    start = property(**start())

    def end():
        doc = "The _end property."
        def fget(self):
            return self.__end
        def fset(self, value):
            self.__end = value
        def fdel(self):
            del self.__end
        return locals()
    end = property(**end())

    def pair():
        doc = "The _pair property."
        def fget(self):
            return self.__pair
        def fset(self, value):
            self.__pair = value
        def fdel(self):
            del self.__pair
        return locals()
    pair = property(**pair())


class Ground:
    """
    Grounds will only be used in circuit analysis; not available to the users
    """
    def __init__(self, name):
        self.__name = name

    def name():
        doc = "The _name property."
        def fget(self):
            return self.__name
        def fset(self, value):
            self.__name = value
        def fdel(self):
            del self.__name
        return locals()
    name = property(**name())


class Junction(Component):
    """For splitting wires."""
    def __init__(self, name, num_cxns=3):
        super().__init__(0, 0, 0, name, num_cxns)

    def add_end(self):
        self.cxns = np.append(self.cxns, self.name)


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


class Meter_Type(Enum):
    AMMETER = 0
    VOLTMETER = 1
    OHMMETER = 2


class Multimeter(Component):
    def __init__(self, name, meter_type=Meter_Type.VOLTMETER):
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
    def __init__(self, name, A, d=0.01, kappa=1):
        super().__init__(0, 0, 0, name)
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
