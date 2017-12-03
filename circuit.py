import numpy as np
from numpy.linalg import solve
# import scipy as sc
# from scipy.sparse.linalg import spsolve
import matplotlib.pyplot as plt
from components import *
from algorithms import backtracker

class Circuit:
    """
    Graph consisting of Vertices and Edges G(V, E)
    Vertices are Components and Edges are Wires
    """
    def __init__(self, V, E, dt=0.01, n=100):
        self.vertices = V
        self.edges = E

        self.t_step = dt
        self.num_steps = n

        self.update_comp_cxns() # necessary when loading from file

        if self.validate():
            
            if not self.contains([Capacitor]):
                self.t_step = 0
                self.num_steps = 1
                self.t_hist = np.array([1])
            else:
                self.t_hist = np.linspace(0.0, self.t_step*self.num_steps, self.num_steps)

            self.add_nulls()
            self.add_junctions()

            self.print_circuit_data(ignore=[])

            for _ in range(self.num_steps):
                self.run()

            self.print_circuit_data()
            self.graph_circuit_data()
            # self.graph_circuit_data([DC_Battery], 1)

    @property
    def lenv(self):
        return len(self.vertices)

    @property
    def edge_tuples(self):
        """Reformats the edges for ease-of-use with some algorithms"""
        return list(map(lambda e: e.pair, self.edges))

    def add_component(self, c, wire, args=[]):
        # create the new component
        new_comp = c(*args)
        new_comp.add_connection(wire.start)
        new_comp.add_connection(wire.end)
        self.vertices = np.append(self.vertices, new_comp)

        self.split_wire(wire, self.lenv-1)

    def split_wire(self, wire, new_conn):
        # configure the old components' connections
        self.vertices[wire.start].change_connection(wire.end, new_conn)
        self.vertices[wire.end].change_connection(wire.start, new_conn)

        # create the new wires
        self.edges = np.append(self.edges, Wire(wire.start, new_conn))
        self.edges = np.append(self.edges, Wire(new_conn, wire.end))

        # delete the old wire
        self.edges = np.delete(self.edges, np.where(self.edges == wire))

    def add_junctions(self):
        """
        Inserts a junction into each wire to serve as a node and to avoid
        2-component circuits from being labelled invalid
        """
        start_len = len(self.edges)
        for w in self.edges[start_len::-1]:
            if not self.connects_to(w, Junction):
                self.add_component(Junction, w, [2])

        # make the last Junction into a Ground node
        if isinstance(self.vertices[-1], Junction):
            self.vertices[-1].is_ground = True
        else:
            self.add_ground()

        # update components' connections to match the new wires
        self.update_comp_cxns()

        # show the circuit with wires
        # self.print_circuit_data([], w=True)

    def add_nulls(self):
        """Adds Null_Components to the Circuit so that no two Junctions are
        connected"""
        for w in self.edges:
            if isinstance(self.vertices[w.start], Junction) and \
               isinstance(self.vertices[w.end], Junction):
                self.add_component(Null_Component, w)

        self.update_comp_cxns()

    def add_ground(self):
        """add Ground junction to the Circuit. Currently very unoptimized :("""
        self.add_component(Null_Component, self.edges[-1])
        self.add_junctions()

    def validate(self):
        """
        Check that a valid circuit has been made.
        Criteria for a valid circuit:
        * at least one closed loop with:
            * non-zero resistance
                * greedy to check this
            * at least one source of emf
                * doesn't have be a battery: could be a capacitor or an inductor
        * recursive backtracking that there is a closed loop around the emf source
        * if there are components with less than 2 connections, immediately tell
        the user to complete the circuit

        How to accomplish this?
        1. Locate all emf sources (batteries, capacitors, inductors)
        2. For each, keep calculating loops until a closed loop with non-zero
        equivalent resistance is found
            * When found, break and return True
            * If not found, the circuit is not valid
        """
        for i in range(self.lenv):
            # add isinstance(comp, Inductor)
            comp = self.vertices[i]
            if isinstance(comp, DC_Battery) or isinstance(comp, Capacitor):
                if backtracker(self, i, i, [], self.edge_tuples) > 0:
                    print('valid')
                    # reset total_res
                    global total_res
                    total_res = 0
                    return True # circuit is valid
        print("Circuit is not valid")
        return False # circuit is not valid

    def run(self):
        # this is where all the nodal analysis will take place

        # self.print_circuit_data([], True)

        # set up the matrices
        m_size = self.lenv - 1
        A = np.zeros((m_size, m_size))
        b = np.zeros((m_size, 1))

        # loop through all the nodes and components to fill the matrices
        for i in range(m_size): # will go over every component except for the ground node
            comp = self.vertices[i]
            if isinstance(comp, Junction):
                # fill in the currents
                # current into element: -1
                # current out of element: 1
                for conn in comp.cxns:
                    A[i, conn] = self.get_curr_dir(i, conn)
            else:
                # voltages
                v_drop = -1.

                if type(comp) in [DC_Battery, Capacitor]:
                    b[i] = comp.emf
                    v_drop = 1.
                elif type(comp) in [Resistor, Light_Bulb, Multimeter]:
                    A[i, i] = comp.res

                c1 = comp.cxns[0]
                c2 = comp.cxns[1]
                if not (isinstance(self.vertices[c1], Junction) and self.vertices[c1].is_ground):
                    A[i, c1] = -1. * v_drop
                if not(isinstance(self.vertices[c2], Junction) and self.vertices[c2].is_ground):
                    A[i, c2] = 1. * v_drop


        x = solve(A, b)

        # x = spsolve(A, b) #scipy sparse matrix solver
        # print(x)

        # equate values of x with the components
        for i in range(len(x)):
            comp = self.vertices[i]
            if isinstance(comp, Junction):
                comp.emf = x[i]
            else:
                comp.curr = x[i]
                comp.i_hist = np.append(comp.i_hist, x[i])

        # complete calculations
        for i in range(self.lenv):
            comp = self.vertices[i]

            if isinstance(comp, Junction):
                for conn in comp.cxns:
                    comp.curr += self.vertices[conn].curr * self.get_curr_dir(i, conn)
                comp.i_hist = np.append(comp.i_hist, comp.curr)
            elif isinstance(comp, Capacitor):
                # print(comp.emf, comp.curr)

                comp.emf += comp.curr * self.t_step / comp.cpty
            elif type(comp) in [Resistor, Light_Bulb]:
                comp.emf = comp.curr * comp.res
            else:
                pass

            comp.v_hist = np.append(comp.v_hist, comp.emf)

        # update multimeter readings
        for c in self.vertices:
            if isinstance(c, Multimeter):
                c.calc_reading(self)

        return 0
    
    def contains(self, types):
        for c in self.vertices:
            if type(c) in types:
                return True
        return False

    def connects_to(self, wire, comp_type):
        return isinstance(self.vertices[wire.start], comp_type) or \
               isinstance(self.vertices[wire.end], comp_type)

    def get_curr_dir(self, node_name, comp_name):
        if self.vertices[comp_name].cxns[0] == node_name:
           return 1
        elif self.vertices[comp_name].cxns[1] == node_name:
           return -1
        else:
           raise ValueError("Components not connected")

    def print_circuit_data(self, ignore=[Junction, Null_Component], w=False):
        print("============")
        print("Circuit Data")
        print("============")
        for i in range(self.lenv):
            c = self.vertices[i]
            if not type(c) in ignore:
                print(i, type(c), 'I:', c.curr, 'V:', c.emf, 'R:', c.res)#, c.cxns)

        print("============")

        if w:
            for wire in self.edges:
                print("[{0}, {1}]".format(wire.start, wire.end))

    def graph_circuit_data(self, comps=[Capacitor], vir=0):
        """
        Graph data of certain components
        params:
            comps: list. types to graph
            viq: int. Voltage (0), Current (1), Resistance (2)
        """
        #TODO: Charge for Capacitors
        #TODO: make subplots
        for c in self.vertices:
            if type(c) in comps:
                plt.plot(self.t_hist, [c.v_hist, c.i_hist, c.r_hist][vir])

        plt.xlabel("Time (s)")
        plt.ylabel(["Voltage (V)", "Current (I)", "Resistance ($\Omega$)"][vir])
        plt.show()

    def update_comp_cxns(self):
        for i in range(self.lenv):
            self.vertices[i].update_connections(i, self.edges)
