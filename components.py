import numpy as np
from enum import Enum


class Component:
    """
    The base class that holds the basic characteristics of the electric
    components.
    """    
    def __init__(self, V_o, I_o, R_o, num_cxns=2):
        """
        emf: voltage drop across the component
        curr: the current through the component
        res: resistance of the component
        num_cxns: optional. the number of connections the component has
        """
        self.emf = V_o
        self.curr = I_o
        self.res = R_o
        self.cxns = np.ones(num_cxns, dtype='int') * -1

        self.len_conn = num_cxns
        
        # for graphing
        self.v_hist = np.array([])
        self.i_hist = np.array([])
        self.r_hist = np.array([])

    def change_connection(self, old_c, new_c):
        """Replaces (the first occurrence of) old_c with new_c in self.cxns"""
        for i in range(self.len_conn):
            if self.cxns[i] == old_c:
                self.cxns[i] = new_c
                break

    def add_connection(self, cxn):
        """Adds a connection. i.e. replaces an unused connection (-1) with cxn"""
        self.change_connection(-1, cxn)

    def rm_connection(self, cxn):
        """Removes a connection. Replaces cxn with -1"""
        self.change_connection(cxn, -1)

    def update_connections(self, name, wires):
        """Loops through all elements of wires and updates whatever connections
        had been changed in class Circuit"""
        for w in wires:
            if w.start == name:
                self.add_connection(w.end)
            elif w.end == name:
                self.add_connection(w.start)

    @property
    def is_fully_connected(self):
        """Checks if all the component's ends have been connected"""
        return not (-1 in self.cxns)

    @property
    def power(self):
        """Power dissipated by the element"""
        return self.curr * self.emf


class Wire:
    """Wires are used to connect components to each other.
    Have no physical properties; assumed to be ideal"""
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.pair = (self.start, self.end)


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
    """When OFF, current cannot flow through"""
    def __init__(self, state=State.ON): #probably not the best use of enums
        super().__init__(self, 0, 0, 0)
        self.state = state


class Meter_Type(Enum):
    AMMETER = "A"
    VOLTMETER = "V"
    OHMMETER = "Ohms"


class Multimeter(Component):
    """Used for measuring properties of a circuit at certain points"""
    def __init__(self, meter_type=Meter_Type.VOLTMETER):
        if meter_type == Meter_Type.VOLTMETER:
            R = 1e+10 # voltmeters have "infinite" resistance
        else:
            R = 0
        super().__init__(0, 0, R)
        self.meter_type = meter_type
        self.reading = -1.
        self.reading_hist = np.array([])

    def calc_reading(self, Circuit):
        """
        Calculates the value to be displayed
        * current: current flowing out of the previous components
        * voltage: total voltage drop of the components in between the two ends
        * resistance: the equivalent resistance of the components in between
        """
        if self.meter_type == Meter_Type.VOLTMETER:
            self.reading = self.emf
        elif self.meter_type == Meter_Type.AMMETER:
            self.reading = self.curr
        elif self.meter_type == Meter_Type.OHMMETER:
            pass #TODO

        print("Multimeter: {0:0.2f} {1}".format(self.reading, self.meter_type.value))
        self.reading_hist = np.append(self.reading_hist, self.reading)
        return self.reading


class DC_Battery(Component):
    """Direct Current emf source"""
    def __init__(self, V=3):
        super().__init__(V, 0, 0)


class Resistor(Component):
    """Circuit elements that dissipate power"""
    def __init__(self, R=5):
        super().__init__(0, 0, R)


class Light_Bulb(Resistor):
    """
    A special resisitor that works at a specific wattage
    state: whether the bulb is ON or OFF
    wattage: the required power for the bulb to function

    NOTE: better implementation when GUI
    """
    def __init__(self, R, W, state=State.OFF):
        super().__init__(0, 0, R)
        self.state = state
        self.wattage = W

    def update_state(self):
        if self.power == self.wattage:
            self.state = State.ON
        else:
            self.state = State.OFF


class Capacitor(Component):
    """
    Parallel-plate capacitor
    cpty: capacitance
    chg: charge of the capacitor
    kappa: the dielectric constant (1 in vacuum)
    """
    def __init__(self, C, v_init=0, kappa=1):
        # set a bound on the capacitor's initial voltage
        if v_init < 1e-02:
            v_init = 0
        super().__init__(v_init, 0, 0)
        self.cpty = C * 1e-06
        self.chg = self.cpty * self.emf
        self.kappa = kappa

        self.q_hist = np.array([])


class Inductor(Component):
    """
    Work in progress
    L: inductance
    """
    def __init__(self, L):
        # L given in microhenries
        super().__init__(0, 0, 0) #TODO: has either v_init or i_init (maybe r_init?)
        self.L = L * 1e-06
