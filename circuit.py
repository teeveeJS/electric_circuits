import numpy as np
from numpy.linalg import solve
from components import *
from algorithms import backtracker, get_neighbor_edges

class Circuit:
    """
    Graph consisting of Vertices and Edges G(V, E)
    Vertices are Components and Edges are Wires
    """
    def __init__(self, V, E):
        self.__vertices = V
        self.__edges = E

        if self.validate():
            self.run()

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

    @property
    def adjcy_matrix(self):
        A = np.zeros((self.lenv, self.lenv))

        for e in self.edge_tuples:
            A[e[0], e[1]] = 1
            A[e[1], e[0]] = 1 # the connection goes both ways

        return A

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
                new_junction = Junction(i_new, 2)
                new_junction.add_connection(w.start)
                new_junction.add_connection(w.end)
                self.vertices = np.append(self.vertices, new_junction)

                self.split_wire(w, i_new)

        # make the last Junction into a Ground node
        self.vertices[-1].is_ground = True

    def add_nulls(self):
        """Adds Null_Components to the Circuit so that no two Junctions are
        connected"""
        for w in self.edges:
            if isinstance(self.vertices[w.start], Junction) and \
               isinstance(self.vertices[w.end], Junction):
                i_new = self.lenv
                new_null_comp = Null_Component(i_new)
                new_null_comp.add_connection(w.start)
                new_null_comp.add_connection(w.end)
                self.vertices = np.append(self.vertices, new_null_comp)

                self.split_wire(w, i_new)

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
        for comp in self.vertices:
            # add isinstance(comp, Inductor)
            if isinstance(comp, DC_Battery) or isinstance(comp, Capacitor):
                if backtracker(self, comp.name, comp.name, [], self.edge_tuples) > 0:
                    print('valid')
                    # reset total_res
                    global total_res
                    total_res = 0
                    return True # circuit is valid
        print("Circuit is not valid")
        return False # circuit is not valid

    def run(self):
        # this is where all the nodal analysis will take place

        # this has to be called first so that the ground node is the last element
        # in self.vertices
        self.add_nulls()
        self.add_junctions()

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
                # drop in current
                # 0 for all components except capacitors and inductors
                if isinstance(self.vertices[conn], Capacitor): #\
                   # or isinstance(self.vertices[conn], Inductor):
                    b[i] = self.vertices[conn].curr_consumption()
                else:
                    b[i] = 0. # redundant; b already initialized to 0's
            else:
                # voltages
                v_drop = -1.

                if isinstance(comp, DC_Battery):
                    b[i] = comp.emf
                    v_drop = 1.
                elif isinstance(comp, Resistor) or isinstance(comp, Light_Bulb):
                    b[i] = 0.
                    A[i, i] = comp.res
                elif isinstance(comp, Capacitor):
                    # TODO
                    pass


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
            elif isinstance(comp, Capacitor):
                pass
            else:
                comp.curr = x[i]

        # set the emf of the last component (ground) to 0
        self.vertices[-1].emf = 0 #though it should already be 0 through initialization

        # complete calculations
        for i in range(self.lenv):
            comp = self.vertices[i]
            if isinstance(comp, Junction):
                for conn in comp.cxns:
                    comp.curr += self.vertices[conn].curr * self.get_curr_dir(i, conn)
            elif isinstance(comp, Capacitor):
                pass
            elif isinstance(comp, Resistor) or isinstance(comp, Light_Bulb):
                comp.emf = comp.curr * comp.res
            else:
                pass


        self.print_circuit_data()

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

    def print_circuit_data(self):
        print("============")
        print("Circuit Data")
        print("============")
        for c in self.vertices:
           if not (isinstance(c, Junction) or isinstance(c, Null_Component)):
               print(c.name, type(c), 'I:', c.curr, 'V:', c.emf)

        print("============")
