import numpy as np
from enum import Enum


class Component:
    """
    emf: voltage drop across the component
    curr: the current through the component
    res: resistance of the component
    """
    def __init__(self, V_o, I_o, R_o, num_cxns=2):
        self.emf = V_o
        self.curr = I_o
        self.res = R_o
        self.cxns = np.ones(num_cxns, dtype='int') * -1

        self.len_conn = num_cxns

        self.v_hist = np.array([])
        self.i_hist = np.array([])
        self.r_hist = np.array([])

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
    def __init__(self, state=State.ON): #probably not the best use of enums
        super().__init__(self, 0, 0, 0)
        self.state = state


class Meter_Type(Enum):
    AMMETER = 0
    VOLTMETER = 1
    OHMMETER = 2


class Multimeter(Component):
    def __init__(self, meter_type=Meter_Type.VOLTMETER):
        super().__init__(0, 0, 0)
        self.meter_type = meter_type
        self.reading = -1.

    def calc_reading(self, Circuit):
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
        self.cpty = C * 1e-06 #self.epsilon * A / d
        self.chg = self.cpty * self.emf
        self.kappa = kappa

        self.q_hist = np.array([])


class Inductor(Component):
    """
    L: inductance
    """
    def __init__(self, L):
        super().__init__(0, 0, 0) #TODO: has either v_init or i_init (maybe r_init?)
        self.L = L
