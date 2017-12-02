import numpy as np
from enum import Enum


class Component:
    """
    emf: voltage drop across the component
    curr: the current through the component
    res: resistance of the component
    """
    def __init__(self, V_o, I_o, R_o, num_cxns=2):
        self.__emf = V_o
        self.__I = I_o
        self.__R = R_o
        self.__cxns = np.ones(num_cxns, dtype='int') * -1

        self.len_conn = num_cxns

        self.__v_hist = np.array([])
        self.__i_hist = np.array([])

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

    def v_hist():
        doc = "Voltage History."
        def fget(self):
            return self.__v_hist
        def fset(self, value):
            self.__v_hist = value
        def fdel(self):
            del self.__v_hist
        return locals()
    v_hist = property(**v_hist())

    def i_hist():
        doc = "Current (I) History."
        def fget(self):
            return self.__i_hist
        def fset(self, value):
            self.__i_hist = value
        def fdel(self):
            del self.__i_hist
        return locals()
    i_hist = property(**i_hist())

    def change_connection(self, old_c, new_c):
        for i in range(self.len_conn):
            if self.cxns[i] == old_c:
                self.cxns[i] = new_c
                break

    def add_connection(self, cxn):
        self.change_connection(-1, cxn)

    def rm_connection(self, cxn):
        # TODO: handle the (error) case where nothing is removed
        # potential problem: only the first instance is removed
        self.change_connection(cxn, -1)

    def update_connections(self, name, wires):
        for w in wires:
            if w.start == name:
                self.add_connection(w.end)
            elif w.end == name:
                self.add_connection(w.start)

    @property
    def is_fully_connected(self):
        return not (-1 in self.cxns)

    @property
    def power(self):
        """Power dissipated by the element"""
        return self.curr * self.emf


class Wire(Component):
    def __init__(self, start, end):
        super().__init__(0, 0, 0)
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


class Junction(Component):
    """For splitting wires."""
    def __init__(self, num_cxns=3):
        super().__init__(0, 0, 0, int(num_cxns))
        self.is_ground = False

    def add_end(self):
        self.cxns = np.append(self.cxns, -1)


class Null_Component(Component):
    """Added whenever two Junctions are connected to each other"""
    def __init__(self):
        super().__init__(0, 0, 0)


class State(Enum):
    ON = True
    OFF = False


class Switch(Component):
    def __init__(self, state=State.ON): #probably not the best use of enums
        super().__init__(self, 0, 0, 0)
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
    def __init__(self, meter_type=Meter_Type.VOLTMETER):
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

        # will be very easy to implement once the matrix stuff is done

        return


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
        super().__init__(0, 0, R)
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
    # should be initialized through capacitance (in microfarads)
    # A, d, kappa, epsilon don't really matter (kappa at most)
    def __init__(self, C, kappa=1, v_init=0): #A, d=0.01, kappa=1):
        super().__init__(v_init, 0, 0)
        # self.epsilon = kappa * 8.854e-12
        self.__C = C * 1e-06 #self.epsilon * A / d
        self.__Q = self.cpty * self.emf
        self.__k = kappa

        self.__q_hist = np.array([])

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

    def kappa():
        doc = "The dielectric constant."
        def fget(self):
            return self.__k
        def fset(self, value):
            self.__k = value
        def fdel(self):
            del self.__k
        return locals()
    kappa = property(**kappa())

    def q_hist():
        doc = "Charge History."
        def fget(self):
            return self.__q_hist
        def fset(self, value):
            self.__q_hist = value
        def fdel(self):
            del self.__q_hist
        return locals()
    q_hist = property(**q_hist())


class Inductor(Component):
    """
    L: inductance
    """
    def __init__(self, L):
        super().__init__(0, 0, 0) #TODO: has either v_init or i_init (maybe r_init?)
        self.__L = L

    def L():
        doc = "The _L property."
        def fget(self):
            return self.__L
        def fset(self, value):
            self.__L = value
        def fdel(self):
            del self.__L
        return locals()
    L = property(**L())
