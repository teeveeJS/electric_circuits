import numpy as np
from numpy.linalg import solve
import scipy as sc
from scipy.sparse.linalg import spsolve
import matplotlib.pyplot as plt
from components import *
from algorithms import backtracker

class Circuit:
    """
    Graph consisting of Vertices and Edges G(V, E)
    Vertices are Components and Edges are Wires
    """
    def __init__(self, V, E):
        self.__vertices = V
        self.__edges = E

        self.t_step = 0.01
        self.num_steps = 100
        self.t_hist = np.linspace(0.0, self.t_step*self.num_steps, self.num_steps)

        self.update_comp_cxns()

        if self.validate():

            # this has to be called first so that the ground node is the last element
            # in self.vertices
            self.add_nulls()
            self.add_junctions()

            self.print_circuit_data()

            for _ in range(self.num_steps):
                self.run()

            self.print_circuit_data()
            self.graph_circuit_data()

    def vertices():
        doc = "Vertices (components) of the Circuit: an array of Components"
        def fget(self):
            return self.__vertices
        def fset(self, value):
            self.__vertices = value
        def fdel(self):
            del self.__vertices
        return locals()
    vertices = property(**vertices())

    def edges():
        doc = "Edges (connections) of the Circuit: an array of Wires"
        def fget(self):
            return self.__edges
        def fset(self, value):
            self.__edges = value
        def fdel(self):
            del self.__edges
        return locals()
    edges = property(**edges())

    @property
    def lenv(self):
        return len(self.vertices)

    @property
    def edge_tuples(self):
        """Reformats the edges for ease-of-use with some algorithms"""
        return list(map(lambda e: e.pair, self.edges))

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
                # create the new component
                i_new = self.lenv
                new_junction = Junction(2)
                new_junction.add_connection(w.start)
                new_junction.add_connection(w.end)

                # print('adding junction', i_new, w.start, w.end)
                self.vertices = np.append(self.vertices, new_junction)

                self.split_wire(w, i_new)

        # make the last Junction into a Ground node
        self.vertices[-1].is_ground = True

        self.update_comp_cxns()



        self.print_circuit_data([], w=True)

    def add_nulls(self):
        """Adds Null_Components to the Circuit so that no two Junctions are
        connected"""
        for w in self.edges:
            if isinstance(self.vertices[w.start], Junction) and \
               isinstance(self.vertices[w.end], Junction):
                i_new = self.lenv
                new_null_comp = Null_Component()
                new_null_comp.add_connection(w.start)
                new_null_comp.add_connection(w.end)
                self.vertices = np.append(self.vertices, new_null_comp)

                self.split_wire(w, i_new)

        self.update_comp_cxns()

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
        b = np.zeros(m_size)

        # loop through all the nodes and components to fill the matrices
        # fill in the currents
        # possible problem: what if there are junctions connected to each other?
        for i in range(m_size): # will go over every component except for the ground node
            comp = self.vertices[i]
            if isinstance(comp, Junction):
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
                elif type(comp) in [Resistor, Light_Bulb]:
                    b[i] = 0.
                    A[i, i] = comp.res


                c1 = comp.cxns[0]
                c2 = comp.cxns[1]
                if not (isinstance(self.vertices[c1], Junction) and self.vertices[c1].is_ground):
                    A[i, c1] = -1. * v_drop
                if not(isinstance(self.vertices[c2], Junction) and self.vertices[c2].is_ground):
                    A[i, c2] = 1. * v_drop

        x = solve(A, b)
        # print(x)

        # equate values of x with the components
        for i in range(len(x)):
            comp = self.vertices[i]
            if isinstance(comp, Junction):
                comp.emf = x[i]
            else:
                comp.curr = x[i]

                # reverse current direction if necessary
                # if comp.curr < 0:
                #     comp.curr *= -1
                #     comp.cxns = comp.cxns[::-1]

        # complete calculations
        for i in range(self.lenv):
            comp = self.vertices[i]
            if isinstance(comp, Junction):
                for conn in comp.cxns:
                    comp.curr += self.vertices[conn].curr * self.get_curr_dir(i, conn)
            elif isinstance(comp, Capacitor):
                comp.v_hist = np.append(comp.v_hist, comp.emf)

                # print(comp.emf, comp.curr)

                comp.emf += comp.curr * self.t_step / comp.cpty
            elif type(comp) in [Resistor, Light_Bulb]:
                comp.emf = comp.curr * comp.res
            else:
                pass

        return 0

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
                print(i, type(c), 'I:', c.curr, 'V:', c.emf)#, c.cxns)

        print("============")

        if w:
            for wire in self.edges:
                print("[{0}, {1}]".format(wire.start, wire.end))

    def graph_circuit_data(self, comps=[Capacitor], viq=0):
        """
        Graph data of certain components
        params:
            comps: list. types to graph
            viq: int. Voltage (0), Current (1), Charge (2) [only for capacitors]
        """
        #TODO: make subplots
        for c in self.vertices:
            if type(c) in comps:
                plt.plot(self.t_hist, [c.v_hist, c.i_hist, c.q_hist][viq])
        plt.show()

    def update_comp_cxns(self):
        for i in range(self.lenv):
            self.vertices[i].update_connections(i, self.edges)
