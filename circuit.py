import numpy as np
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

        self.add_junctions()

        self.validate()

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
    def edge_tuples(self):
        """Reformats the edges for ease-of-use with some algorithms"""
        return list(map(lambda e: e.pair, self.edges))

    @property
    def adjcy_matrix(self):
        A = np.zeros((len(self.vertices), len(self.vertices)))

        for e in self.edge_tuples:
            A[e[0], e[1]] = 1
            A[e[1], e[0]] = 1 # the connection goes both ways

        return A

    def add_junctions(self):
        """
        Inserts a junction into each wire to serve as a node and to avoid
        2-component circuits from being labelled invalid
        """
        start_len = len(self.edges)
        for w in self.edges[start_len::-1]:
            if not self.connects_to(w, Junction):
                # create the new component
                i_new = len(self.vertices)
                new_junction = Junction(i_new, 2)
                new_junction.add_connection(w.start)
                new_junction.add_connection(w.end)
                self.vertices = np.append(self.vertices, new_junction)
                # configure the old component's connections
                self.vertices[w.start].change_connection(w.end, i_new)
                self.vertices[w.end].change_connection(w.start, i_new)
                # create the new wires
                self.edges = np.append(self.edges, Wire(w.start, i_new))
                self.edges = np.append(self.edges, Wire(i_new, w.end))
                # delete the old wire
                self.edges = np.delete(self.edges, np.where(self.edges == w))

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
                if backtracker(self, comp.name) > 0:
                    print('valid')
                    # reset total_res
                    global total_res
                    total_res = 0
                    return True # circuit is valid

        return False # circuit is not valid

    def run(self):
        # this is where all the nodal analysis will take place
        # self.add_ground()

        # TODO: calculate equipotential regions. until then, each Wire is a node


        # set up the matrices
        matr_size = len(self.edges) + len(self.vertices)
        A = np.array((matr_size, matr_size))
        b = np.array((1, matr_size))

        # loop through all the nodes and components to fill the matrices


        return None

    def add_component(self, component):
        self.vertices = np.insert(self.vertices, len(self.vertices), component)
        return None

    def add_ground(self):
        # add a Ground to the circuit
        ground = Ground(len(self.vertices))
        self.add_component(ground)
        # the circuit needs to be broken open so that the Ground can be connected
        break_edge = None
        for comp in self.vertices:
            # simply place the Ground next to the first found emf source
            if isinstance(comp, DC_Battery) or isinstance(comp, Capacitor):
                break_edge = get_neighbor_edges(self, comp.name)[0]
                break
        # delete break_edge from self.edges
        # then form two new Wires to self.edges with Ground inserted in between
        for i in range(len(self.edges)):
            if np.array_equal(self.edges[i], break_edge):
                self.edges = np.delete(self.edges, i, 0)
                break

        print(self.edge_tuples)

        self.edges = np.insert(self.edges, len(self.edges), Wire(break_edge[0], ground.name), 0)
        self.edges = np.insert(self.edges, len(self.edges), Wire(break_edge[1], ground.name), 0)

        return None

    def connects_to(self, wire, comp_type):
        return isinstance(self.vertices[wire.start], comp_type) or \
               isinstance(self.vertices[wire.end], comp_type)
